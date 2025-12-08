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
    """
    Docstring for get_currency
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
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[FunctionTool(get_currency)]
)
