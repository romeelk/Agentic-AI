import json


class WeatherClient:
    def __init__(self,api_key):
        self.api_key = api_key
        
    def get_weather_by_city(self, city:str)->str:
        forecast = {
            "city":city,
            "forecast":"Sunny with cloudy intervals"
        }
        return json.dumps(forecast)

# client = WeatherClient("test")
# response = client.get_weather_by_city("Test")
# print(response)