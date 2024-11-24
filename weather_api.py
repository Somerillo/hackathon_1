# This script uses the OpenWeather API to get the current weather data
# The city can be changed when calling the class if the input format is respected

# Future changes: the code can be modified to retrieve the weather only from geolocation. For that, in the retrieve_weather module
# we must change the observation variable as self.mgr.weather_at_coords(lat, lon). Whatsoever, i'm in DA bootcamp and not in devs bootcamp
# i just want to retrieve the json file data in anyway :)

from pyowm import OWM
from config import my_apy_key
from datetime import datetime


class Get_Weather:
    def __init__(self, api_key, city="Ashkelon,IL"):
        self.city = city
        self.owm = OWM(api_key)
        self.mgr = self.owm.weather_manager()

    def retrieve_weather(self):
        try:
            observation = self.mgr.weather_at_place(self.city)
            return observation.weather
        except Exception as e:
            print(f"an error occurred trying to retrieve the weather: {e}")
            return None

    def get_all_data(self):
        """
        it gets all the relevant weather data, escept for the AQI
        """
        weather = self.retrieve_weather()
        if weather:
            return {
                "temperature": weather.temperature("celsius")["temp"],
                "humidity": weather.humidity,
                "status": weather.status,
                "description": weather.detailed_status,
                "wind": weather.wind()
            }
        return None



## ------------------------------------- Testing the code ------------------------------------- ##

# api_key = my_apy_key

# # cities = ["Ashkelon,IL", "Tel Aviv,IL", "Los Angeles,US"]
# # city = cities[0]
# # weather_instances = Get_Weather(api_key, city)


# weather_instances = Get_Weather(api_key)

# print(weather_instances.get_all_data()["wind"]["speed"])
# print(weather_instances.get_all_data()["temperature"])
# print(weather_instances.get_all_data()["sunrise"])
# print(weather_instances.get_all_data())