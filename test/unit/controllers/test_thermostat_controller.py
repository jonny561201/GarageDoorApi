import uuid

import jwt
from mock import patch

from svc.controllers.thermostat_controller import get_user_temp
from svc.db.models.user_information_model import UserPreference


@patch('svc.controllers.thermostat_controller.UserDatabaseManager')
@patch('svc.controllers.thermostat_controller.is_jwt_valid')
@patch('svc.controllers.thermostat_controller.read_temperature_file')
@patch('svc.controllers.thermostat_controller.get_user_temperature')
class TestThermostatController:
    JWT_TOKEN = jwt.encode({}, 'JWT_SECRET', algorithm='HS256').decode('UTF-8')
    USER_ID = uuid.uuid4().hex

    def test_get_user_temp__should_call_read_temperature_file(self, mock_user, mock_file, mock_jwt, mock_db):
        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_file.assert_called()

    def test_get_user_temp__should_call_get_user_temperature(self, mock_user, mock_file, mock_jwt, mock_db):
        preference = UserPreference()
        preference.is_fahrenheit = True
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = preference
        temp_text = 'fake response'
        mock_file.return_value = temp_text

        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_user.assert_called_with(temp_text, True)

    def test_get_user_temp__should_call_is_jwt_valid(self, mock_user, mock_file, mock_jwt, mock_db):
        temp_text = 'fake response'
        mock_file.return_value = temp_text

        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_jwt.assert_called_with(self.JWT_TOKEN)

    def test_get_user_temp__should_return_response_from_get_user_temperature(self, mock_user, mock_file, mock_jwt,
                                                                             mock_db):
        preference = UserPreference()
        preference.is_fahrenheit = False
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = preference
        expected_temp = 23.45
        mock_user.return_value = expected_temp

        actual = get_user_temp(self.USER_ID, self.JWT_TOKEN)

        assert actual == {'currentTemp': expected_temp, 'isFahrenheit': False}

    def test_get_user_temp__should_call_get_preferences_by_user(self, mock_user, mock_file, mock_jwt, mock_db):
        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_db.return_value.__enter__.return_value.get_preferences_by_user.assert_called_with(self.USER_ID)

    def test_get_user_temp__should_call_get_user_temperature_with_user_id(self, mock_user, mock_file, mock_jwt,
                                                                          mock_db):
        preference = UserPreference()
        expected_text = 'fake text'
        preference.is_fahrenheit = True
        mock_db.return_value.__enter__.return_value.get_preferences_by_user.return_value = preference
        mock_file.return_value = expected_text

        get_user_temp(self.USER_ID, self.JWT_TOKEN)

        mock_user.assert_called_with(expected_text, True)
