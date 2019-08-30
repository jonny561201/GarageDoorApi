import pytest
from mock import patch

from svc.utilities.temperature import get_temperature
from werkzeug.exceptions import Conflict


@patch('svc.utilities.temperature.read_temperature_file')
def test_get_temperature__should_return_temperature_in_celsius(mock_temp):
    mock_temp.return_value = ['72 01 4b 46 7f ff 0e 10 57 : crc=57 YES',
                              '72 01 4b 46 7f ff 0e 10 57 t=23125']
    actual = get_temperature()

    assert actual == 23.12


@patch('svc.utilities.temperature.read_temperature_file')
def test_get_temperature__should_throw_conflict_when_error_reading_temp(mock_temp):
    mock_temp.return_value = ['72 01 4b 46 7f ff 0e 10 57 : crc=57 NOPE']
    with pytest.raises(Conflict):
        get_temperature()
