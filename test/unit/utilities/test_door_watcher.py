from mock import patch

from svc.utilities.door_watcher import poll_doors, start_door_watcher


@patch('svc.utilities.door_watcher.DoorEvents')
@patch('svc.utilities.door_watcher.file_utils')
@patch('svc.utilities.door_watcher.gpio_utils')
class TestPollDoors:

    def test_poll_doors__should_return_current_states(self, mock_gpio, mock_file, mock_events):
        mock_gpio.is_garage_open.side_effect = [True, False]

        actual = poll_doors({'1': True, '2': False})

        assert actual == {'1': True, '2': False}

    def test_poll_doors__should_not_notify_or_update_duration_on_first_poll(self, mock_gpio, mock_file, mock_events):
        mock_gpio.is_garage_open.side_effect = [True, False]

        poll_doors({})

        mock_file.update_door_duration.assert_not_called()
        mock_events.get_instance.return_value.notify.assert_not_called()

    def test_poll_doors__should_update_duration_only_for_changed_door(self, mock_gpio, mock_file, mock_events):
        mock_gpio.is_garage_open.side_effect = [True, False]

        poll_doors({'1': False, '2': False})

        mock_file.update_door_duration.assert_called_once_with('1')

    def test_poll_doors__should_notify_once_when_doors_change(self, mock_gpio, mock_file, mock_events):
        mock_gpio.is_garage_open.side_effect = [True, True]

        poll_doors({'1': False, '2': False})

        mock_events.get_instance.return_value.notify.assert_called_once()

    def test_poll_doors__should_not_notify_when_nothing_changes(self, mock_gpio, mock_file, mock_events):
        mock_gpio.is_garage_open.side_effect = [False, True]

        poll_doors({'1': False, '2': True})

        mock_file.update_door_duration.assert_not_called()
        mock_events.get_instance.return_value.notify.assert_not_called()


@patch('svc.utilities.door_watcher.threading.Thread')
def test_start_door_watcher__should_start_daemon_thread(mock_thread):
    start_door_watcher()

    assert mock_thread.call_args.kwargs['daemon'] is True
    mock_thread.return_value.start.assert_called_once()
