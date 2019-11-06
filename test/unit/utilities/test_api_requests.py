import json

from flask import Response
from mock import patch

from svc.utilities.api_requests import get_weather_by_city


@patch('svc.utilities.api_requests.requests')
class TestApiRequests:
    city = 'Des Moines'
    unit_preference = 'imperial'
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Des%20Moines&units=imperial'

    def test_get_weather_by_city__should_call_requests_get(self, mock_requests):
        get_weather_by_city(self.city, self.unit_preference)

        mock_requests.get.assert_called_with(self.url)

    def test_get_weather_by_city__should_return_temp_data(self, mock_requests):
        expected_temp = 64.8
        mock_response = {'main': {'temp': expected_temp}}
        mock_requests.get.return_value = Response(json.dumps(mock_response), 200)

        actual = get_weather_by_city(self.city, self.unit_preference)

        assert actual['temp'] == expected_temp
