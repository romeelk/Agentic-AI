import json
import requests
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class WeatherAPIError(Exception):
    """Custom exception for weather API errors"""
    pass

class WeatherClient:
    API_URL = "https://api.openweathermap.org/data/2.5/weather"

    STATUS_MESSAGES = {
        404: "city not found",
        401: "invalid API key",
        500: "weather service unavailable",
    }
    def __init__(self,api_key):
        self.api_key = api_key
         
    def _fetch_weather(self, city: str) -> requests.Response:
        """Fetch weather data from openweather API."""
        weather_params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.API_URL, weather_params)
        return response
    
    def _parse_response(self,response: requests.Response, city: str)-> str:
        """Parse API response and handle errors."""
        if response.status_code == 200:
            try:
                data = response.json()
                description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                return json.dumps({"city": city, "forecast": description, "temperature":temperature})
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                raise WeatherAPIError(f"Invalid response format: {e}")
        
        # Get error message from mapping or use generic message
        error_msg = self.STATUS_MESSAGES.get(
            response.status_code, 
            f"unexpected status code: {response.status_code}"
        )
        raise WeatherAPIError(error_msg)
        
      
    def get_weather_by_city(self, city:str)->str:
        """Fetch weather for a city with proper error handling."""
        try:
            response = self._fetch_weather(city)
            return self._parse_response(response, city)
        except WeatherAPIError as e:
            logger.error(f"API Error: {e}")
            return json.dumps({"error": str(e)})
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return json.dumps({"error": "unable to reach weather service"})
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return json.dumps({"error": "unexpected error occurred"})