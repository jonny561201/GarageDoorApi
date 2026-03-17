from svc.config.settings_state import Settings
from svc.utilities.gpio_utils import get_garage_coordinates


def test_get_garage_coordinates__should_return_settings_coords():
    instance = Settings.get_instance()
    instance.Coordinates._settings = {'latitude': 10.0, 'longitude': 20.0}

    actual = get_garage_coordinates()

    assert actual.latitude == 10.0
    assert actual.longitude == 20.0