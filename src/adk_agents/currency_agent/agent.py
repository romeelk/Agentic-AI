from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool
import requests
import json

from google.adk.tools import FunctionTool

STATUS_MESSAGES = {
    422: "invalid currency",
    500: "currency service unavailable",
}
class CurrencyAPIError(Exception):
    """Custom exception for currency API errors"""
    pass

def convert_currency(source_currency, target_currency):
    """Converts the source currecny to the targe currency.
       so that for example $1 = $1.31 (sterling)
    Args:
        source_currency (string): source currency to convert from
        target_currency (string): target currency to conver to

    Raises:
        CurrencyAPIError: currenct API exception when currency api returns error response

    Returns:
        string: JSON string
    """    
    base_url = f"https://hexarate.paikama.co/api/rates/latest/{source_currency}?target={target_currency}"
    
    response = requests.get(base_url,verify=False)
    if response.status_code == 200:
        try:
           
            data = response.json()
            source = data["data"]["base"]
            target = data["data"]["target"]
            rate = data["data"]["mid"]
            return json.dumps({"source":source,"target":target,"rate":rate})
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise CurrencyAPIError(f"Invalid response format: {e}")
    else:
        data = response.json()
        message = data["data"]["message"]
    return json.dumps({"message":message})

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for converting currencies.',
    instruction='Answer foreign exchange currency conversions by using the tool convert_currency. Use your knowledge of currecny codes to answer queries about currency codes.',
    tools=[FunctionTool(convert_currency)]
)
