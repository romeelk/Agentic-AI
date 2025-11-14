import json
import random
import requests
import os
from dotenv import load_dotenv
 
class WeatherClient:
    API_URL = "https://api.openweathermap.org/data/2.5/weather"
    def __init__(self,api_key):
        self.api_key = api_key
         
    def get_weather_by_city(self, city:str)->str:
        
        weather_params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(WeatherClient.API_URL, weather_params)
        weather_data = response.json()
        print(weather_data)

        print(response.status_code)
        if response.status_code == 200:
            print("Successfully called weather api")
        else:
            print("Failed to call weather api status code: {}",response.status_code )
        
        if response.status_code == 200:
            forecast = {
                "city": city,
                "forecast": weather_data["weather"][0]["description"]
            }
        elif response.status_code == 404:
            forecast = {"city": "city not found"}
        elif response.status_code in (401, 500):
            forecast = {"error": "cannot respond to your request at this time."}
        else:
            forecast = {"error": f"unexpected status code: {response.status_code}"}
        return json.dumps(forecast)

# First test open weather api call

# CITY="London"
# API_URL="https://api.openweathermap.org/data/2.5/weather"
# weather_params = {
#     "q": CITY,
#     "appid": "1363eb03308a5159b189f7331a3f6024",
#     "units": "metric"
# }
# response = requests.get(API_URL, weather_params)

# if response.status_code == 200:
#     print("Successfully called weather api")
#     print(type(response.json()))
#     weather = response.json()
#     print(weather["weather"][0]["description"])

load_dotenv()
API_KEY = os.environ.get("OPEN_WEATHER_API")
print(API_KEY)
weather_client = WeatherClient(API_KEY)
print(weather_client.get_weather_by_city("london"))