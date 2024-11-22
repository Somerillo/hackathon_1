# This script uses the OpenWeather API to get the current weather data
# For the moment it is anexclusive service for Ashkelon city - Israel
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
        self.pollution_mgr = self.owm.airpollution_manager()
        self.geocoding_mgr = self.owm.geocoding_manager()

    def retrieve_weather(self):
        try:
            observation = self.mgr.weather_at_place(self.city)
            # observation = self.mgr.weather_at_id(self.city)
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
            sunrise_time = datetime.fromtimestamp(weather.sunrise_time())
            sunset_time = datetime.fromtimestamp(weather.sunset_time())
            return {
                "temperature": weather.temperature("celsius")["temp"],
                "humidity": weather.humidity,
                "status": weather.status,
                "description": weather.detailed_status,
                "wind": weather.wind(),
                "reference_time": weather.reference_time("iso"),
                "sunrise": sunrise_time.strftime('%H:%M:%S'),
                "sunset": sunset_time.strftime('%H:%M:%S')
            }
        return None

    def retrieve_geocoding(self):
        """
        this one is needed to get the AQI, for it works only with the geolocation data
        """
        try:
            location = self.geocoding_mgr.geocode(self.city)
            return location
        except Exception as e:
            print(f"mistakes were made to get geolocation: {e}")
            return None

    def get_air_quality_data(self):
        """
        gets the air quality index
        """
        try:
            location = self.retrieve_geocoding()
            if not location:
                print("location couldn't be fetched")
                return None

            air_quality = self.pollution_mgr.air_quality_at_coords(
                location[0].lat, location[0].lon)
            
            return air_quality.aqi if air_quality else None

        except Exception as e:
            print(f"some error occurred while retrieving air quality: {e}")
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
# print(weather_instances.get_air_quality_data())
# print(weather_instances.get_all_data())