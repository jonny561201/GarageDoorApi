from svc.manager import create_app


class TestLightRoutesIntegration:
    TEST_CLIENT = None

    def setup_method(self):
        flask_app = create_app('__main__')
        self.TEST_CLIENT = flask_app.test_client()

    def test_get_all_assigned_lights__should_return_unauthorized_without_header(self):
        actual = self.TEST_CLIENT.get('lights/groups')

        assert actual.status_code == 401
