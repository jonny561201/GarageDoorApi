from svc.utilities.conversion_utils import convert_to_fahrenheit, convert_to_celsius


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


def test_convert_to_celsius__should_convert_negative_number():
    actual = convert_to_celsius(12.0)

    assert actual == -11.11


def test_convert_to_celsius__should_convert_positive_number():
    actual = convert_to_celsius(50.0)

    assert actual == 10.0