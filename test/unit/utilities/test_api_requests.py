import json

import pytest
from mock import patch
from requests import Response
from werkzeug.exceptions import Unauthorized, BadRequest

from svc.utilities.api_requests import get_weather_by_city


@patch('svc.utilities.api_requests.requests')
class TestApiRequests:
    city = 'Des Moines'
    unit_preference = 'imperial'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    app_id = 'ab30xkd0'
    params = None
    response = None
    response_content = None

    def setup_method(self):
        self.response = Response()
        self.response.status_code = 200
        self.response_content = {'main': {}, 'weather': [{}]}
        self.params = {'q': self.city, 'units': self.unit_preference, 'APPID': self.app_id}

    def test_get_weather_by_city__should_call_requests_get(self, mock_requests):
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        get_weather_by_city(self.city, self.unit_preference, self.app_id)

        mock_requests.get.assert_called_with(self.url, params=self.params)

    def test_get_weather_by_city__should_use_provided_city_location_in_url(self, mock_requests):
        city = 'London'
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        get_weather_by_city(city, self.unit_preference, self.app_id)

        self.params['q'] = city
        mock_requests.get.assert_called_with(self.url, params=self.params)

    def test_get_weather_by_city__should_use_provided_app_id_in_url(self, mock_requests):
        app_id = 'fake app id'
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        get_weather_by_city(self.city, self.unit_preference, app_id)

        self.params['APPID'] = app_id
        mock_requests.get.assert_called_with(self.url, params=self.params)

    def test_get_weather_by_city__should_return_temp_data(self, mock_requests):
        expected_temp = 64.8
        self.response_content['main']['temp'] = expected_temp
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        actual = get_weather_by_city(self.city, self.unit_preference, self.app_id)

        assert actual['temp'] == expected_temp

    def test_get_weather_by_city__should_return_default_temp_value_of_zero(self, mock_requests):
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        actual = get_weather_by_city(self.city, self.unit_preference, self.app_id)

        assert actual['temp'] == 0.0

    def test_get_weather_by_city__should_return_min_temp_value(self, mock_requests):
        min_temp = 12.34
        self.response_content['main']['temp_min'] = min_temp
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        actual = get_weather_by_city(self.city, self.unit_preference, self.app_id)

        assert actual['min_temp'] == min_temp

    def test_get_weather_by_city__should_return_default_min_temp_value(self, mock_requests):
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        actual = get_weather_by_city(self.city, self.unit_preference, self.app_id)

        assert actual['min_temp'] == 0.0

    def test_get_weather_by_city__should_return_max_temp_value(self, mock_requests):
        max_temp = 12.87
        self.response_content['main']['temp_max'] = max_temp
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        actual = get_weather_by_city(self.city, self.unit_preference, self.app_id)

        assert actual['max_temp'] == max_temp

    def test_get_weather_by_city__should_return_default_max_temp_value(self, mock_requests):
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        actual = get_weather_by_city(self.city, self.unit_preference, self.app_id)

        assert actual['max_temp'] == 0.0

    def test_get_weather_by_city__should_return_weather_description(self, mock_requests):
        forecast_description = 'fake forecast'
        self.response_content['weather'][0]['description'] = forecast_description
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        actual = get_weather_by_city(self.city, self.unit_preference, self.app_id)

        assert actual['description'] == forecast_description

    def test_get_weather_by_city__should_return_default_weather_description(self, mock_requests):
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response

        actual = get_weather_by_city(self.city, self.unit_preference, self.app_id)

        assert actual['description'] is None

    def test_get_weather_by_city__should_call_api_using_unit_preference_in_params(self, mock_requests):
        self.response._content = json.dumps(self.response_content)
        mock_requests.get.return_value = self.response
        unit = 'metric'
        self.params['units'] = unit

        get_weather_by_city(self.city, unit, self.app_id)

        mock_requests.get.assert_called_with(self.url, params=self.params)

    def test_get_weather_by_city__should_throw_unauthorized_when_401_returned(self, mock_requests):
        response = Response()
        response.status_code = 401
        mock_requests.get.return_value = response

        with pytest.raises(Unauthorized):
            get_weather_by_city(self.city, self.unit_preference, self.app_id)

    def test_get_weather_by_city__should_throw_bad_request_when_not_ok_status_returned(self, mock_requests):
        response = Response()
        response.status_code = 400
        mock_requests.get.return_value = response

        with pytest.raises(BadRequest):
            get_weather_by_city(self.city, self.unit_preference, self.app_id)
