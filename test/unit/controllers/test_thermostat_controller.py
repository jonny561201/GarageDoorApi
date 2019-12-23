import json
import os
import uuid

import jwt
from mock import patch, ANY

from svc.constants.home_automation import Automation
from svc.constants.hvac_state import HvacState
from svc.controllers.thermostat_controller import get_user_temp, set_user_temperature
from svc.utilities.event import MyThread


@patch('svc.controllers.thermostat_controller.get_weather')
@patch('svc.controllers.thermostat_controller.UserDatabaseManager')
@patch('svc.controllers.thermostat_controller.is_jwt_valid')
@patch('svc.controllers.thermostat_controller.read_temperature_file')
@patch('svc.controllers.thermostat_controller.get_user_temperature')
class TestThermostatGetController:
    JWT_TOKEN = jwt.encode({}, 'JWT_SECRET', algorithm='HS256').decode('UTF-8')
    USER_ID = uuid.uuid4().hex
    APP_ID = 'fake app id'
    PREFERENCE = None

    def setup_method(self):
        self.PREFERENCE = {'city': 'Des Moines', 'temp_unit': 'celsius', 'is_fahrenheit': True}
        os.environ.update({'WEATHER_APP_ID': self.APP_ID})

    def teardown_method(self):
        os.environ.pop('WEATHER_APP_ID')

    def test_get_user_temp__should_call_read_temperature_file(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_file.assert_called()

    def test_get_user_temp__should_call_get_user_temperature(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE
        temp_text = 'fake response'
        mock_file.return_value = temp_text

        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_user.assert_called_with(temp_text, True)

    def test_get_user_temp__should_call_is_jwt_valid(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        temp_text = 'fake response'
        mock_file.return_value = temp_text

        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_jwt.assert_called_with(self.JWT_TOKEN)

    def test_get_user_temp__should_return_response_from_get_user_temperature(self, mock_user, mock_file, mock_jwt,
                                                                             mock_db, mock_weather):
        self.PREFERENCE['is_fahrenheit'] = False
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE
        expected_temp = 23.45
        mock_user.return_value = expected_temp

        actual = get_user_temp(self.USER_ID, self.JWT_TOKEN)

        assert actual['currentTemp'] == expected_temp
        assert actual['isFahrenheit'] is False

    def test_get_user_temp__should_call_get_preferences_by_user(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_db.return_value.__enter__.return_value.get_preferences_by_user.assert_called_with(self.USER_ID)

    def test_get_user_temp__should_call_get_user_temperature_with_user_id(self, mock_user, mock_file, mock_jwt,
                                                                          mock_db, mock_weather):
        expected_text = 'fake text'
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE
        mock_file.return_value = expected_text

        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_user.assert_called_with(expected_text, True)

    def test_get_user_temp__should_call_api_requests_with_city(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE
        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_weather.assert_called_with('Des Moines', ANY, ANY)

    def test_get_user_temp__should_call_api_requests_with_unit_metric(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE
        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_weather.assert_called_with(ANY, 'metric', ANY)

    def test_get_user_temp__should_call_api_requests_with_unit_imperial(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        self.PREFERENCE['temp_unit'] = 'fahrenheit'
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE
        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_weather.assert_called_with(ANY, 'imperial', ANY)

    def test_get_user_temp__should_call_api_requests_with_app_id(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_weather.assert_called_with(ANY, ANY, self.APP_ID)

    def test_get_user_temp__should_consolidate_weather_response_with_thermostat_data(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        expected_temp = 56.3
        mock_weather.return_value = {'temp': expected_temp}
        mock_user.return_value = 23.3
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE

        actual = get_user_temp(self.USER_ID, self.JWT_TOKEN)

        assert actual['temp'] == expected_temp

    def test_get_user_temp__should_return_thermostat_temps_in_celsius(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        self.PREFERENCE['is_fahrenheit'] = False
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE

        actual = get_user_temp(self.USER_ID, self.JWT_TOKEN)

        assert actual['minThermostatTemp'] == 10.0
        assert actual['maxThermostatTemp'] == 32.0

    def test_get_user_temp__should_return_thermostat_temps_in_fahrenheit(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        self.PREFERENCE['is_fahrenheit'] = True
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE

        actual = get_user_temp(self.USER_ID, self.JWT_TOKEN)

        assert actual['minThermostatTemp'] == 50.0
        assert actual['maxThermostatTemp'] == 90.0


@patch('svc.controllers.thermostat_controller.convert_to_celsius')
@patch('svc.controllers.thermostat_controller.is_jwt_valid')
class TestThermostatSetController:
    BEARER_TOKEN = 'fake bearer'
    DESIRED_CELSIUS_TEMP = 24.0
    DESIRED_FAHRENHEIT_TEMP = 68.9
    STATE = None

    def setup_method(self):
        self.STATE = HvacState.get_instance()
        self.STATE.ACTIVE_THREAD = MyThread(None, None, 0)
        self.REQUEST = json.dumps({'mode': Automation.HEATING_MODE, 'isFahrenheit': False, 'desiredTemp': self.DESIRED_CELSIUS_TEMP}).encode('UTF-8')

    def test_set_user_temperature__should_call_is_jwt_valid(self, mock_jwt, mock_convert):
        set_user_temperature(self.REQUEST, self.BEARER_TOKEN)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)

    def test_set_user_temperature__should_convert_fahrenheit_to_celsius(self, mock_jwt, mock_convert):
        request = json.dumps({'mode': Automation.COOLING_MODE, 'isFahrenheit': True, 'desiredTemp': self.DESIRED_FAHRENHEIT_TEMP}).encode('UTF-8')
        set_user_temperature(request, self.BEARER_TOKEN)

        mock_convert.assert_called_with(self.DESIRED_FAHRENHEIT_TEMP)

    def test_set_user_temperature__should_set_desired_temp(self, mock_jwt, mock_convert):
        set_user_temperature(self.REQUEST, self.BEARER_TOKEN)

        assert self.STATE.DESIRED_TEMP == self.DESIRED_CELSIUS_TEMP
        mock_convert.assert_not_called()

    @patch('svc.controllers.thermostat_controller.MyThread')
    def test_set_user_temperature__should_create_thread_when_none(self, mock_thread, mock_jwt, mock_convert):
        self.STATE.ACTIVE_THREAD = None
        self.STATE.STOP_EVENT = None
        set_user_temperature(self.REQUEST, self.BEARER_TOKEN)

        assert self.STATE.ACTIVE_THREAD is not None
        assert self.STATE.STOP_EVENT is not None

    def test_set_user_temperature__should_set_mode(self, mock_jwt, mock_convert):
        set_user_temperature(self.REQUEST, self.BEARER_TOKEN)
        assert self.STATE.MODE == Automation.HEATING_MODE
