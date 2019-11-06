import json

import requests


def get_weather_by_city(city, unit_preference):
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Des%20Moines&units=imperial'
    response = requests.get(url)
    response_content = json.loads(response.data)
    return {'temp': response_content['main'].get('temp', 0.0)}
