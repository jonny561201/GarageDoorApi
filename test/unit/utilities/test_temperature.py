import pytest
from werkzeug.exceptions import Conflict

from svc.utilities.temperature import get_user_temperature, convert_to_fahrenheit, convert_to_celsius


def test_get_user_temperature__should_return_temperature_in_celsius():
    temp_text = ['72 01 4b 46 7f ff 0e 10 57 : crc=57 YES',
                 '72 01 4b 46 7f ff 0e 10 57 t=23125']
    actual = get_user_temperature(temp_text, False)

    assert actual == 23.12


def test_get_user_temperature__should_return_temperature_in_fahrenheit():
    temp_text = ['72 01 4b 46 7f ff 0e 10 57 : crc=57 YES',
                 '72 01 4b 46 7f ff 0e 10 57 t=12451']
    actual = get_user_temperature(temp_text, True)

    assert actual == 54.41


def test_get_user_temperature__should_throw_conflict_when_error_reading_temp():
    temp_text = ['72 01 4b 46 7f ff 0e 10 57 : crc=57 NOPE']
    with pytest.raises(Conflict):
        get_user_temperature(temp_text, False)


def test_get_user_temperature__should_throw_conflict_when_no_temp_text_found():
    temp_text = ['72 01 4b 46 7f ff 0e 10 57 : crc=57 YES',
                 '72 01 4b 46 7f ff 0e 10 57']
    with pytest.raises(Conflict):
        get_user_temperature(temp_text, False)


def test_convert_to_fahrenheit__should_convert_zero():
    actual = convert_to_fahrenheit(0.0)

    assert actual == 32.0


def test_convert_to_fahrenheit__should_convert_positive_number():
    actual = convert_to_fahrenheit(24.0)

    assert actual == 75.2


def test_convert_to_fahrenheit__should_convert_negative_number():
    actual = convert_to_fahrenheit(-20.0)

    assert actual == -4.0


def test_convert_to_celsius__should_convert_zero():
    actual = convert_to_celsius(32.0)

    assert actual == 0.0
