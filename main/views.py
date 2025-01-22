from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv

from datetime import datetime

# import math


load_dotenv()

# import urllib.request

# and round up values 


# Create your views here.
def home(request):
    '''Display the weather information according to the city input by user'''

    # user get the empty form. to input a city name
    if request.method == 'GET':
        return render(request, 'main/home.html', {})
    

    weather_data = None

    if request.method == 'POST':
        city =request.POST['city']
        # city ='Berlin'

        # Get the API key from the .env file
        WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

        if not WEATHER_API_KEY:
            raise ValueError("API key is missing.")

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'

        try:
            response = requests.get(url)
            print(response)

            if response.status_code == 200:
                print(f"request weather data, successful!")
                data = response.json()
                print(f"weather data:\n\ {data}\n")

                country = data['sys']['country']
                temperature = round(data['main']['temp'])
                # temperature = data['main']['temp']
                description = data['weather'][0]['description']
                # icon = data['weather'][0]['icon']
                humidity = data['main']['humidity']
                # wind_speed = data['wind']['speed']
                wind_speed = round(data['wind']['speed'])

                sunrise = data['sys']['sunrise'] # need to convert value in time
                sunset = data['sys']['sunset'] # need to convert value in time
                clouds = data['clouds']['all'] # need to check percentage and display a reuls type :'cloudy, sunny' etc....

                today = datetime.now()
                print(today)


                weather_data = {
                    'city': city,
                    'country': country,
                    'temperature': temperature,
                    'description': description,
                    # 'icon': icon,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'sunrise': sunrise,
                    'sunset': sunset,
                    'clouds': clouds
                }

                return render(request, 'main/home.html', {'weather_data': weather_data})
            else:
                return render(request, 'main/home.html', {'error': 'Failed to fetch weather data.'})

            # return render(request, 'home.html', {})
        except Exception as e:
            print(f"Error occurred while fetching weather data: {str(e)}")
            return render(request, 'main/home.html', {'error': 'Failed to fetch weather data due to an error.'})
