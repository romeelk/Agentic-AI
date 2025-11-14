from google.adk.agents.llm_agent import Agent
from .weather import weather_client
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("OPEN_WEATHER_API")

weather_client = weather_client.WeatherClient(API_KEY)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='weather_agent',
    description='A helpful assistant that can use a weather tool to provide weather forecasest for a city',
    instruction='Answer user questions to the best of your knowledge',
    tools=[weather_client.get_weather_by_city]
)
