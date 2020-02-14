import json

from mock import patch, ANY
from requests import Response

from svc.constants.home_automation import Automation
from svc.utilities.api_utils import get_weather_by_city, get_light_api_key, get_light_groups, set_light_groups, \
    get_light_group_state


@patch('svc.utilities.api_utils.requests')
class TestWeatherApiRequests:
    CITY = 'Des Moines'
    UNIT_PREFERENCE = 'imperial'
    URL = 'https://api.openweathermap.org/data/2.5/weather'
    APP_ID = 'ab30xkd0'
    PARAMS = None
    RESPONSE = None
    RESPONSE_CONTENT = None

    def setup_method(self):
        self.RESPONSE = Response()
        self.RESPONSE.status_code = 200
        self.RESPONSE_CONTENT = {'main': {}, 'weather': [{}]}
        self.PARAMS = {'q': self.CITY, 'units': self.UNIT_PREFERENCE, 'APPID': self.APP_ID}

    def test_get_weather_by_city__should_call_requests_get(self, mock_requests):
        self.RESPONSE._content = json.dumps(self.RESPONSE_CONTENT)
        mock_requests.get.return_value = self.RESPONSE

        get_weather_by_city(self.CITY, self.UNIT_PREFERENCE, self.APP_ID)

        mock_requests.get.assert_called_with(self.URL, params=self.PARAMS)

    def test_get_weather_by_city__should_use_provided_city_location_in_url(self, mock_requests):
        city = 'London'
        self.RESPONSE._content = json.dumps(self.RESPONSE_CONTENT)
        mock_requests.get.return_value = self.RESPONSE

        get_weather_by_city(city, self.UNIT_PREFERENCE, self.APP_ID)

        self.PARAMS['q'] = city
        mock_requests.get.assert_called_with(self.URL, params=self.PARAMS)

    def test_get_weather_by_city__should_use_provided_app_id_in_url(self, mock_requests):
        app_id = 'fake app id'
        self.RESPONSE._content = json.dumps(self.RESPONSE_CONTENT)
        mock_requests.get.return_value = self.RESPONSE

        get_weather_by_city(self.CITY, self.UNIT_PREFERENCE, app_id)

        self.PARAMS['APPID'] = app_id
        mock_requests.get.assert_called_with(self.URL, params=self.PARAMS)

    def test_get_weather_by_city__should_call_api_using_unit_preference_in_params(self, mock_requests):
        self.RESPONSE._content = json.dumps(self.RESPONSE_CONTENT)
        mock_requests.get.return_value = self.RESPONSE
        unit = 'metric'
        self.PARAMS['units'] = unit

        get_weather_by_city(self.CITY, unit, self.APP_ID)

        mock_requests.get.assert_called_with(self.URL, params=self.PARAMS)

    def test_get_weather_by_city__should_return_status_code_and_content(self, mock_requests):
        expected_content = json.dumps(self.RESPONSE_CONTENT)
        self.RESPONSE._content = expected_content
        mock_requests.get.return_value = self.RESPONSE

        status, content = get_weather_by_city(self.CITY, 'metric', self.APP_ID)

        assert status == 200
        assert content == expected_content


@patch('svc.utilities.api_utils.requests')
class TestLightApiRequests:
    USERNAME = 'fake username'
    PASSWORD = 'fake password'
    BASE_URL = 'http://192.168.1.139:8080/api'
    API_KEY = 'fake api key'

    def test_get_light_api_key__should_call_requests_with_url(self, mock_requests):
        get_light_api_key(self.USERNAME, self.PASSWORD)

        mock_requests.post.assert_called_with(self.BASE_URL, data=ANY, headers=ANY)

    def test_get_light_api_key__should_call_requests_with_device_type(self, mock_requests):
        get_light_api_key(self.USERNAME, self.PASSWORD)

        body = json.dumps({'devicetype': Automation().APP_NAME})
        mock_requests.post.assert_called_with(ANY, data=body, headers=ANY)

    def test_get_light_api_key__should_provide_username_and_pass_as_auth_header(self, mock_requests):
        get_light_api_key(self.USERNAME, self.PASSWORD)

        headers = {'Authorization': 'Basic ' + 'ZmFrZSB1c2VybmFtZTpmYWtlIHBhc3N3b3Jk'}
        mock_requests.post.assert_called_with(ANY, data=ANY, headers=headers)

    def test_get_light_api_key__should_return_api_key_response(self, mock_requests):
        response = Response()
        response._content = json.dumps([{'success': {'username': self.API_KEY}}]).encode('UTF-8')
        mock_requests.post.return_value = response

        actual = get_light_api_key(self.USERNAME, self.PASSWORD)

        assert actual == self.API_KEY

    def test_get_light_groups__should_call_groups_url(self, mock_requests):
        expected_url = self.BASE_URL + '/%s/groups' % self.API_KEY
        get_light_groups(self.API_KEY)

        mock_requests.get.assert_called_with(expected_url)

    def test_get_light_groups__should_return_a_list_of_light_groups(self, mock_requests):
        api_response = {
            "1": {
                "devicemembership": [],
                "etag": "ab5272cfe11339202929259af22252ae",
                "hidden": False,
                "name": "Living Room"
            }
        }
        mock_response = Response()
        mock_response._content = json.dumps(api_response).encode('UTF-8')
        mock_requests.get.return_value = mock_response
        actual = get_light_groups(self.API_KEY)

        assert actual['1']['etag'] == 'ab5272cfe11339202929259af22252ae'

    def test_set_light_groups__should_call_state_url(self, mock_requests):
        group_id = 1
        expected_url = self.BASE_URL + '/%s/groups/%s/action' % (self.API_KEY, group_id)
        set_light_groups(self.API_KEY, group_id, True)

        mock_requests.put.assert_called_with(expected_url, data=ANY)

    def test_set_light_groups__should_call_state_with_on_off_set(self, mock_requests):
        state = False
        set_light_groups(self.API_KEY, 2, state)

        expected_request = {'on': state}
        mock_requests.put.assert_called_with(ANY, data=expected_request)

    def test_set_light_groups__should_call_state_with_dimmer_value(self, mock_requests):
        state = True
        brightness = 233
        set_light_groups(self.API_KEY, 1, state, brightness)

        expected_request = {'on': state, 'bri': brightness}
        mock_requests.put.assert_called_with(ANY, data=expected_request)

    def test_set_light_groups__should_call_state_with_on_set_true_if_dimmer_value(self, mock_requests):
        brightness = 155
        set_light_groups(self.API_KEY, 1, False, brightness)

        expected_request = {'on': True, 'bri': brightness}
        mock_requests.put.assert_called_with(ANY, data=expected_request)

    def test_get_light_group_state__should_call_url(self, mock_requests):
        group_id = '1'
        url = self.BASE_URL + '/%s/groups/%s' % (self.API_KEY, group_id)

        get_light_group_state(self.API_KEY, group_id)

        mock_requests.get.assert_called_with(url)
        
    def test_get_light_group_state__should_return_group_response(self, mock_requests):
        group_id = '2'
        response = Response()
        response_content = {'field': 'DoesntMatter'}
        response._content = json.dumps(response_content).encode('UTF-8')
        mock_requests.get.return_value = response
        
        actual = get_light_group_state(self.API_KEY, group_id)
        
        assert actual == response_content
