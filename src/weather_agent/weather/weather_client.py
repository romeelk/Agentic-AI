import json
import random

class WeatherClient:
    def __init__(self,api_key):
        self.api_key = api_key
         
    def get_forecast(self)->str:
        forecast = [
            "Sunny intervals with a chance of showers",
            "Rainy with thunderstorms",
            "Cloudy with sunny spells",
        ]
        return random.choice(forecast)
         
    def get_weather_by_city(self, city:str)->str:
        forecast = {
            "city":city,
            "forecast":self.get_forecast()
        }
        return json.dumps(forecast)
