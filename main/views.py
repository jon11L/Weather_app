from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone

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

        # Get the API key from the .env file
        WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

        if not WEATHER_API_KEY:
            raise ValueError("API key is missing.")

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'

        try:
            response = requests.get(url)
            print(response)

            if response.status_code == 200:
                data = response.json()
                print(f"request weather data, successful!")
                print(f"weather data:\n\ {data}\n")

                country = data['sys']['country']
                temperature = round(data['main']['temp'])
                feels_like = round(data['main']['feels_like'])
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = round(float(data['wind']['speed'])*3.6)
                clouds = data['clouds']['all'] # need to check percentage and display a reuls type :'cloudy, sunny' etc....

                # icon image retrieved by the code given in the response
                icon_code = data['weather'][0]['icon']
                icon = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"


                # time zone data
                timezone_offset = data['timezone'] # in seconds
                city_timezone = timezone(timedelta(seconds=timezone_offset))

                # display today's date accoridng to the timezone
                today = datetime.now(tz=city_timezone).strftime('(%A) %d %b %Y')
                current_time = datetime.now(tz=city_timezone).strftime('%H:%M:%S (%p)')
                
                
                sunrise = datetime.fromtimestamp(data['sys']['sunrise'], tz=city_timezone) #  .strftime('%H:%M:%S ')
                sunset = datetime.fromtimestamp(data['sys']['sunset'], tz=city_timezone) #   .strftime('%H:%M:%S (%p)')
                daylight_duration = sunset - sunrise # .strftime('%H:%M:%S')
                
                # calculate daylight duration in hours and minutes
                daylight_hours = daylight_duration.seconds // 3600
                daylight_minutes = (daylight_duration.seconds % 3600) // 60

                weather_data = {
                    'city': city,
                    'country': country,
                    'temperature': temperature,
                    'feels_like': feels_like,
                    'description': description,
                    'icon': icon,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'sunrise': sunrise.strftime('%H:%M'),
                    'sunset': sunset.strftime('%H:%M'),
                    'clouds': clouds,
                    'today': today,
                    'current_time': current_time,
                    'daylight_hours': daylight_hours,
                    'daylight_minutes': daylight_minutes,
                    
                }

                return render(request, 'main/home.html', {'weather_data': weather_data})
            else:
                return render(request, 'main/home.html', {'error': 'Failed to fetch weather data.'})

        except Exception as e:
            print(f"Error occurred while fetching weather data: {str(e)}")
            return render(request, 'main/home.html', {'error': 'Failed to fetch weather data due to an error.'})
