from mock import patch

from svc.utilities.depth import get_depth_by_intervals


@patch('svc.utilities.depth.get_sump_pump_times')
def test_get_depth_by_intervals__should_call_get_sump_pump_times(mock_gpio):
    get_depth_by_intervals(None, None)

    mock_gpio.assert_called()
