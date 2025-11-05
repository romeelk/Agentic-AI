from google.adk.agents.llm_agent import Agent
from .weather import weather_client
import json


weather_client = weather_client.WeatherClient("fakeapi_key")

root_agent = Agent(
    model='gemini-2.5-flash',
    name='weather_agent',
    description='A helpful assistant that can use a weather tool to provide weather forecasest for a city',
    instruction='Answer user questions to the best of your knowledge',
    tools=[weather_client.get_weather_by_city]
)
