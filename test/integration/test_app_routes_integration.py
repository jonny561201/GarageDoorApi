from mock import MagicMock

from svc.manager import app


class TestAppRoutesIntegration:

    def setup_method(self):
        self.TEST_CLIENT = app.test_client()

    def test_get_health__should_return_success(self):
        actual = self.TEST_CLIENT.get('/health')

        assert actual.status_code == 200

    def test_confirm_registration__should_return_success(self):
        app.mdns = MagicMock()

        actual = self.TEST_CLIENT.post('/register')

        assert actual.status_code == 200

    def test_confirm_registration__should_call_unregister(self):
        app.mdns = MagicMock()

        self.TEST_CLIENT.post('/register')

        app.mdns.unregister.assert_called_once()

