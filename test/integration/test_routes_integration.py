from svc.manager import create_app


class TestRouteIntegration:
    test_client = None

    def setup_method(self):
        flask_app = create_app('__main__')
        self.test_client = flask_app.test_client()

    def test_health_check__should_return_success(self):
        actual = self.test_client.get('healthCheck')

        assert actual.status_code == 200
        assert actual.data.decode('UTF-8') == 'Success'

    def test_garage_door_status__should_return_unauthorized(self):
        actual = self.test_client.get('garageDoor/status')

        assert actual.status_code == 401
