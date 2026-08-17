from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge by using google search tool to ground your answers',
    tools=[GoogleSearchTool()]
)
