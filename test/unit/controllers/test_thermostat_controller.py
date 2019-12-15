import os
import uuid

import jwt
from mock import patch, ANY

from svc.constants.home_automation import HomeAutomation
from svc.controllers.thermostat_controller import get_user_temp, set_user_temperature


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
        self.PREFERENCE = {'city': 'Des Moines', 'temp_unit': 'metric', 'is_fahrenheit': True}
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

        assert actual == {'currentTemp': expected_temp, 'isFahrenheit': False}

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

    def test_get_user_temp__should_call_api_requests_with_unit(self, mock_user, mock_file, mock_jwt, mock_db, mock_weather):
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = self.PREFERENCE
        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_weather.assert_called_with(ANY, 'metric', ANY)

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


@patch('svc.controllers.thermostat_controller.Hvac')
@patch('svc.controllers.thermostat_controller.is_jwt_valid')
class TestThermostatSetController:
    BEARER_TOKEN = 'fake bearer'
    DESIRED_TEMP = 32.0

    def setup_method(self):
        self.REQUEST = {'mode': HomeAutomation.HEATING_MODE, 'desiredTemp': self.DESIRED_TEMP}

    def test_set_user_temperature__should_call_is_jwt_valid(self, mock_jwt, mock_hvac):
        set_user_temperature(self.REQUEST, self.BEARER_TOKEN)

        mock_jwt.assert_called_with(self.BEARER_TOKEN)

    def test_set_user_temperature__should_create_hvac_class_with_mode(self, mock_jwt, mock_hvac):
        set_user_temperature(self.REQUEST, self.BEARER_TOKEN)

        mock_hvac.assert_called_with(ANY, HomeAutomation.HEATING_MODE)
