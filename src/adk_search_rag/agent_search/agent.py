from google.adk.agents.llm_agent import Agent
from google.adk.tools import VertexAiSearchTool

from dotenv import load_dotenv
import os

load_dotenv()
DATA_STORE_ID = os.getenv("DATA_STORE_ID")


search_tool = VertexAiSearchTool(data_store_id=DATA_STORE_ID)

if DATA_STORE_ID is None:
    print("Unable to load DATA_STORE_ID from .env file. Please verify DATA_STORE_ID is set!")
    exit()

root_agent = Agent(
    model='gemini-flash-latest',
    name='root_agent',
    description='Enterprise document search assistant with Agent Search capabilities.',
    instruction='Answer user questions. Use the search tool to answer questions relating to expenses. Always cite sources when available. If the query is not found in the expense policy politely inform the user.'
)
