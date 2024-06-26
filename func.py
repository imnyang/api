from datetime import datetime
from pytz import timezone, all_timezones
from dotenv import load_dotenv
import os
import requests
import datetime

load_dotenv(verbose=True)

def timestamp_to_string(timestamp, how):
    dt_object = datetime.datetime.fromtimestamp(timestamp)

    time_string = dt_object.strftime(how)

    return time_string

def get_weather(city:str, units:str):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    print(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}")
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}")
    data = r.json()
    return {
        "coord": {
            "lon": data["coord"]["lon"],
            "lat": data["coord"]["lat"]
        },
        "weather": {
            "main": data["weather"][0]["main"],
            "icon": data["weather"][0]["icon"],
            "temp": {
                "temp_now": data["main"]["temp"],
                "temp_feels": data["main"]["feels_like"],
                "temp_min": data["main"]["temp_min"],
                "temp_max": data["main"]["temp_max"],
            },
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "wind": {
                "speed": data["wind"]["speed"],
                "deg": data["wind"]["deg"],
            }
        },
        "sun": {
            "rise": timestamp_to_string(data["sys"]["sunrise"], '%H:%M:%S'),
            "set": timestamp_to_string(data["sys"]["sunset"], '%H:%M:%S'),
        }
    }
