import json

import requests


def get_weather_by_city(city, unit_preference):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    args = {'q': city,
            'units': unit_preference}
    response = requests.get(base_url, params=args)
    response_content = json.loads(response.data)

    current_temp = response_content['main'].get('temp', 0.0)
    min_temp = response_content['main'].get('temp_min', 0.0)
    max_temp = response_content['main'].get('temp_max', 0.0)
    forecast_description = response_content['weather'].get('description')

    temp_response = {'temp': current_temp, 'min_temp': min_temp, 'max_temp': max_temp, 'description': forecast_description}
    return temp_response
