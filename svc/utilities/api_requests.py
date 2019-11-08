import json

import requests


def get_weather_by_city(city, unit_preference):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    args = {'q': city,
            'units': unit_preference}
    response = requests.get(base_url, params=args)
    response_content = json.loads(response.data)

    return {'temp': response_content['main'].get('temp', 0.0)}
