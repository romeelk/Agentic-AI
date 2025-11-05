from google.adk.agents.llm_agent import Agent
from weather import weather_client
import json


# class WeatherClient:
#     def __init__(self,api_key):
#         self.api_key = api_key
        
#     def get_weather_by_city(self, city:str)->str:
#         forecast = {
#             "city":city,
#             "forecast":"Sunny with cloudy intervals"
#         }
#         return json.dumps(forecast)

weather_client = weather_client.WeatherClient("fakeapi_key")


root_agent = Agent(
    model='gemini-2.5-flash',
    name='weather_agent',
    description='A helpful assistant that can use a weather tool to provide weather forecasest for a city',
    instruction='Answer user questions to the best of your knowledge',
    tools=[weather_client.get_weather_by_city]
)
