from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool

[FunctionTool]
def add_numbers(num1,num2):
    """A Agent tool called add_numbers that adds two integers

    Args:
        num1 (int): First integer to add
        num2 (int): Second integer to add

    Returns:
        integer: sum of two integers
    """
    return num1 + num2

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='You are a Maths AI agent. When asked about addition of two numbers use the add_numbers tool',
    tools=[add_numbers]
)
