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

def get_currency(source_currency, target_currency):
    """_summary_

    Args:
        source_currency (string): source currenct to 
        target_currency (string): target currency to find exchange for

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
    description='A helpful assistant for answering foregin exchange questions.',
    instruction='Answer foreign exchange by using the tool get_currency',
    tools=[FunctionTool(get_currency)]
)
