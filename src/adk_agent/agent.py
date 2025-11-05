# from google.adk.agents.llm_agent import Agent
# import datetime

# tools = []

# def get_utc_time():
#     return datetime.datetime.now(datetime.UTC).strftime("%c")

# def get_tools():
#     return [func.__name__ for func in tools if func.__name__ != "get_tools"]

# tools = []
# tools.append(get_utc_time)
# # tools.append(get_weather)
# tools.append(get_tools)

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
#     tools=tools
# )

from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

