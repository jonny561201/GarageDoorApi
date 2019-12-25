import os

from mock import patch, ANY

from svc.services.temperature import get_external_temp, get_internal_temp


@patch('svc.services.temperature_service.get_user_temperature')
@patch('svc.services.temperature_service.read_temperature_file')
@patch('svc.services.temperature_service.get_weather')
class TestTemperatureService:
    PREFERENCES = None
    CITY = 'London'
    UNIT = 'celsius'
    APP_ID = 'fake app id'

    def setup_method(self):
        os.environ.update({'WEATHER_APP_ID': self.APP_ID})
        self.PREFERENCES = {'city': self.CITY, 'temp_unit': self.UNIT, 'is_fahrenheit': True}

    def teardown_method(self):
        os.environ.pop('WEATHER_APP_ID')

    def test_get_external_weather__should_call_get_weather_with_city(self, mock_weather, mock_file, mock_temp):
        get_external_temp(self.PREFERENCES)

        mock_weather.assert_called_with(self.CITY, ANY, ANY)

    def test_get_external_weather__should_call_get_weather_with_metric_unit(self, mock_weather, mock_file, mock_temp):
        get_external_temp(self.PREFERENCES)

        mock_weather.assert_called_with(ANY, "metric", ANY)

    def test_get_external_weather__should_call_get_weather_with_imperial_unit(self, mock_weather, mock_file, mock_temp):
        self.PREFERENCES['temp_unit'] = 'fahrenheit'
        get_external_temp(self.PREFERENCES)

        mock_weather.assert_called_with(ANY, "imperial", ANY)

    def test_get_external_weather__should_call_get_weather_with_api_key(self, mock_weather, mock_file, mock_temp):
        get_external_temp(self.PREFERENCES)

        mock_weather.assert_called_with(ANY, ANY, self.APP_ID)

    def test_get_external_weather__should_return_weather_data_from_api_call(self, mock_weather, mock_file, mock_temp):
        response = {'temp': 23.4, 'description': 'Awesome'}
        mock_weather.return_value = response

        actual = get_external_temp(self.PREFERENCES)

        assert actual == response

    def test_get_internal_temp__should_call_read_temperature_file(self, mock_weather, mock_file, mock_temp):
        get_internal_temp(self.PREFERENCES)

        mock_file.assert_called()

    def test_get_internal_temp__should_call_get_user_temperature_with_text_results(self, mock_weather, mock_file, mock_temp):
        temp_text = "2324.455"
        mock_file.return_value = temp_text
        get_internal_temp(self.PREFERENCES)

        mock_temp.assert_called_with(temp_text, ANY)

    def test_get_internal_temp__should_call_get_user_temperature_with_preference_fahrenheit(self, mock_weather, mock_file, mock_temp):
        get_internal_temp(self.PREFERENCES)

        mock_temp.assert_called_with(ANY, self.PREFERENCES['is_fahrenheit'])
