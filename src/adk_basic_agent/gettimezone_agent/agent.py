from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool

import datetime
import pytz

tools = []

[FunctionTool]
def get_utc_time():
    return datetime.datetime.now(datetime.UTC).strftime("%c")

[FunctionTool]
def get_country_time_zones():
    zones = pytz.all_timezones
    return zones

[FunctionTool]
def get_country_time_zone(country_timezone_name):
    country_time_zone = pytz.timezone(country_timezone_name)
    return datetime.datetime.now(country_time_zone).strftime("%c")

def get_tools():
    return [func.__name__ for func in tools if func.__name__ != "get_tools"]

tools = []
tools.append(get_utc_time)
tools.append(get_country_time_zones)
tools.append(get_country_time_zone)
tools.append(get_tools)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for providing current time for different world time zones',
    instruction='Answer user questions relating to current time and time in different time zones. Use available tools get_utc_time and get_country_time_zone',
    tools=tools
)

