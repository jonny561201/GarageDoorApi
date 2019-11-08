import json

from flask import Response
from mock import patch

from svc.utilities.api_requests import get_weather_by_city


@patch('svc.utilities.api_requests.requests')
class TestApiRequests:
    city = 'Des Moines'
    unit_preference = 'imperial'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = None

    def setup_method(self):
        self.params = {'q': self.city, 'units': self.unit_preference}

    def test_get_weather_by_city__should_call_requests_get(self, mock_requests):
        mock_response = {'main': {}}
        mock_requests.get.return_value = Response(json.dumps(mock_response), 200)

        get_weather_by_city(self.city, self.unit_preference)

        mock_requests.get.assert_called_with(self.url, params=self.params)

    def test_get_weather_by_city__should_use_provided_city_location_in_url(self, mock_requests):
        city = 'London'
        mock_response = {'main': {}}
        mock_requests.get.return_value = Response(json.dumps(mock_response), 200)

        get_weather_by_city(city, self.unit_preference)

        self.params['q'] = city
        mock_requests.get.assert_called_with(self.url, params=self.params)

    def test_get_weather_by_city__should_return_temp_data(self, mock_requests):
        expected_temp = 64.8
        mock_response = {'main': {'temp': expected_temp}}
        mock_requests.get.return_value = Response(json.dumps(mock_response), 200)

        actual = get_weather_by_city(self.city, self.unit_preference)

        assert actual['temp'] == expected_temp

    def test_get_weather_by_city__should_return_default_temp_value_of_zero(self, mock_requests):
        mock_response = {'main': {}}
        mock_requests.get.return_value = Response(json.dumps(mock_response), 200)

        actual = get_weather_by_city(self.city, self.unit_preference)

        assert actual['temp'] == 0.0

    def test_get_weather_by_city__should_return_min_temp_value(self, mock_requests):
        min_temp = 12.34
        response = {'main': {'temp_min': min_temp}}
        mock_requests.get.return_value = Response(json.dumps(response), 200)

        actual = get_weather_by_city(self.city, self.unit_preference)

        assert actual['min_temp'] == min_temp

    def test_get_weather_by_city__should_return_default_min_temp_value(self, mock_requests):
        response = {'main': {}}
        mock_requests.get.return_value = Response(json.dumps(response), 200)

        actual = get_weather_by_city(self.city, self.unit_preference)

        assert actual['min_temp'] == 0.0

    def test_get_weather_by_city__should_return_max_temp_value(self, mock_requests):
        max_temp = 12.87
        response = {'main': {'temp_max': max_temp}}
        mock_requests.get.return_value = Response(json.dumps(response), 200)

        actual = get_weather_by_city(self.city, self.unit_preference)

        assert actual['max_temp'] == max_temp

    def test_get_weather_by_city__should_return_default_max_temp_value(self, mock_requests):
        response = {'main': {}}
        mock_requests.get.return_value = Response(json.dumps(response), 200)

        actual = get_weather_by_city(self.city, self.unit_preference)

        assert actual['max_temp'] == 0.0

    def test_get_weather_by_city__should_call_api_using_unit_preference_in_params(self, mock_requests):
        response = {'main': {}}
        mock_requests.get.return_value = Response(json.dumps(response), 200)
        unit = 'metric'
        self.params['units'] = unit

        get_weather_by_city(self.city, unit)

        mock_requests.get.assert_called_with(self.url, params=self.params)
