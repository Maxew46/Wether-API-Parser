import datetime as dt
import openmeteo_requests

import requests_cache
from retry_requests import retry

import sqlite3

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)



Minsk = {"name": "Minsk", "latitude": 53.54, "longitude": 27.33}
Grodno = {"name": "Grodno", "latitude": 53.40, "longitude": 23.49}

cities = [Minsk, Grodno]

conn = sqlite3.connect("whether.db")
cursor = conn.cursor()
url = "https://api.open-meteo.com/v1/forecast"


for i in cities:
    
    params = {
	"latitude": i["latitude"],       
    "longitude": i["longitude"], 
	"hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "rain", "snowfall"],
	"timezone": "Europe/Moscow",
    }

    responses = openmeteo.weather_api(url, params=params)
    hourly = responses[0].Hourly()

    temperature = hourly.Variables(0).ValuesAsNumpy()[0]
    relative_humidity = hourly.Variables(1).ValuesAsNumpy()[0]
    wind_speed = hourly.Variables(2).ValuesAsNumpy()[0]
    rain = hourly.Variables(3).ValuesAsNumpy()[0]
    snowfall = hourly.Variables(4).ValuesAsNumpy()[0]

    cursor.execute(
        "INSERT INTO forecast "
        "(city, temperature, wind_speed, relative_humidity, rain, snow, date) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (i["name"], float(temperature), float(wind_speed),
         float(relative_humidity), float(rain), float(snowfall),
         dt.datetime.now().isoformat()),
    )


conn.commit()
conn.close()