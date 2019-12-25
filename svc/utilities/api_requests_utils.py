import requests


def get_weather_by_city(city, unit, app_id):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    args = {'q': city, 'units': unit, 'APPID': app_id}

    response = requests.get(base_url, params=args)

    return response.status_code, response.content
