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
