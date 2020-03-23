# from mock import patch
#
# from svc.utilities.gpio_utils import update_garage_door
#
#
# @patch('svc.utilities.gpio_utils.toggle_garage_door')
# @patch('svc.utilities.gpio_utils.is_garage_open')
# def test_update_garage_door__should_toggle_garage_when_open_and_request_close(mock_status, mock_toggle):
#     request = {'garageDoorOpen': False}
#     mock_status.return_value = True
#     update_garage_door(request)
#
#     mock_toggle.assert_called()
#
#
# @patch('svc.utilities.gpio_utils.toggle_garage_door')
# @patch('svc.utilities.gpio_utils.is_garage_open')
# def test_update_garage_door__should_toggle_garage_when_close_and_request_open(mock_status, mock_toggle):
#     request = {'garageDoorOpen': True}
#     mock_status.return_value = False
#     update_garage_door(request)
#
#     mock_toggle.assert_called()
#
#
# @patch('svc.utilities.gpio_utils.toggle_garage_door')
# @patch('svc.utilities.gpio_utils.is_garage_open')
# def test_update_garage_door__should_not_toggle_garage_when_close_and_request_close(mock_status, mock_toggle):
#     request = {'garageDoorOpen': False}
#     mock_status.return_value = False
#     update_garage_door(request)
#
#     mock_toggle.assert_not_called()
#
#
# @patch('svc.utilities.gpio_utils.toggle_garage_door')
# @patch('svc.utilities.gpio_utils.is_garage_open')
# def test_update_garage_door__should_not_toggle_garage_when_open_and_request_open(mock_status, mock_toggle):
#     request = {'garageDoorOpen': True}
#     mock_status.return_value = True
#     update_garage_door(request)
#
#     mock_toggle.assert_not_called()