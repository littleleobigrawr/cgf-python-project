import requests
import pprint
from tabulate import tabulate
from datetime import datetime
from config import api_key


# This will remove any special characters from the user input
def remove_special_characters(clean_city_name):
    special_characters = '!@#$%^&*()|[]{};:,./<>?`~-=_+'
    clean_city_name = ''.join(char for char in clean_city_name if char not in special_characters)
    return clean_city_name


def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


city_name = input('Please enter your city: ')
city_name = remove_special_characters(city_name)

city_name = city_name[:30]


geo_location_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={api_key}'

response = requests.get(geo_location_url)

geo_location_response = response.json()

geo_location = geo_location_response[0]

lat = (geo_location['lat'])
lon = (geo_location['lon'])

weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

response = requests.get(weather_url)

weather_response = response.json()

weather = weather_response

weather_name = weather['name']
weather_main = weather['weather'][0]['main']
weather_description = weather['weather'][0]['description']
weather_humidity = weather['main']['humidity']
weather_temperature = weather['main']['temp']

celcius_temp = weather_temperature - 273.15

weather_conditions = {
    "Clouds": "☁️It's cloudy today! Pack a warm jacket",
    "Rain": "🌧️Grab an umbrella before you leave the house",
    "Sunny": "☀️Sunglasses and suncream today",
    "Clear Sky": "It's a clear sky today"
}

weather_data = {
    'Main': weather_main,
    'Description': weather_description,
    'Humidity %': weather_humidity,
    'Temperature (ºC)': celcius_temp
}

with open('weather_data.txt', 'a+') as weather_output:
    weather_output.write(f"\nSearched Time: {get_current_datetime()}\n")
    weather_output.write(f"Weather Data in {weather_name}:\n")
    for key, value in weather_data.items():
        weather_output.write(f"{key}: {value}\n")
    for conditions, message in weather_conditions.items():
        if weather_main.lower() == conditions.lower():
            print(message)
            break

print(tabulate([weather_data], headers='keys', tablefmt='grid'))
