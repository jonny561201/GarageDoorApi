from mock import patch

from svc.utilities.hvac import run_temperature_program


@patch('svc.utilities.hvac.read_temperature_file')
class TestHvac:
    DESIRED_TEMP = 32.9

    def test_run_temperature_program__should_make_call_to_read_temperature_file(self, mock_temp):
        run_temperature_program(self.DESIRED_TEMP)
        mock_temp.assert_called()
