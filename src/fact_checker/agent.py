from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools.google_search_tool import google_search

GEMINI_MODEL = "gemini-2.5-flash"

fact_reviwer_agent = LlmAgent(
    name="FactChecker",
    model=GEMINI_MODEL,
    instruction="""
    You are a Fact checker agent when given a claim by a user 
    you use google search tool to verify the claim.
    """,
    description="Facts check the users claim using google search.",
    output_key="reviwed_fact",
    tools=[google_search]
)

fact_reviser_agent = LlmAgent(
    name="ReviseFact",
    model=GEMINI_MODEL,
    instruction="""
    You are a Fact revision checker agent when given a claim by a user 
    that has been fact checked by tge FactChecker agent you provide the correct answer.
    You must cite the source of your answer to make it verifiable.
    """,
    description="Corrects the users false claims if proven by using the results of fact_reviwer_agent",
    output_key="revised_fact"
)

# This agent orchestrates the pipeline by running the sub_agents in order.
reviwer_and_revise_agent = SequentialAgent(
    name="ReviewAndRevise",
    sub_agents=[fact_reviwer_agent, fact_reviser_agent],
    description="Executes a sequence of code writing, reviewing, and refactoring.",
)

root_agent = reviwer_and_revise_agent