from svc.config.door_events import DoorEvents


class TestDoorEvents:

    def setup_method(self):
        DoorEvents._instance = None
        self.events = DoorEvents.get_instance()

    def test_current_version__should_start_at_zero(self):
        assert self.events.current_version() == 0

    def test_notify__should_increment_version(self):
        self.events.notify()

        assert self.events.current_version() == 1

    def test_wait_for_change__should_return_new_version_when_already_changed(self):
        self.events.notify()

        actual = self.events.wait_for_change(0, 0.01)

        assert actual == 1

    def test_wait_for_change__should_return_none_on_timeout(self):
        actual = self.events.wait_for_change(0, 0.01)

        assert actual is None
