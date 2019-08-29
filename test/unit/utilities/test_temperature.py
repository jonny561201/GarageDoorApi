from svc.utilities.temperature import get_temperature


def test_get_temperature__should_return_temperature_in_celsius():
    actual = get_temperature()

    assert actual == 23.13
