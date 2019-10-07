import base64
import json

from mock import patch

from svc.routes.app_routes import app_login



@patch('svc.routes.app_routes.request')
class TestAppRoutes:
    USER = 'user_name'
    PWORD = 'password'
    FAKE_JWT_TOKEN = 'fakeJwtToken'.encode('UTF-8')
    CREDS = ('%s:%s' % (USER, PWORD)).encode()
    ENCODED_CREDS = base64.b64encode(CREDS).decode('UTF-8')
    AUTH_HEADER = {"Authorization": "Basic " + ENCODED_CREDS}

    @patch('svc.routes.app_routes.get_login')
    def test_app_login__should_respond_with_success_status_code(self, mock_login, mock_request):
        mock_request.headers = self.AUTH_HEADER
        mock_login.return_value = self.FAKE_JWT_TOKEN

        actual = app_login()

        assert actual.status_code == 200

    @patch('svc.routes.app_routes.get_login')
    def test_app_login__should_respond_with_success_login_response(self, mock_login, mock_request):
        mock_request.headers = self.AUTH_HEADER
        mock_login.return_value = self.FAKE_JWT_TOKEN

        actual = app_login()
        json_actual = json.loads(actual.data)

        assert json_actual['bearerToken'] == self.FAKE_JWT_TOKEN.decode('UTF-8')

    @patch('svc.routes.app_routes.get_login')
    def test_app_login__should_call_get_login(self, mock_login, mock_request):
        mock_request.headers = self.AUTH_HEADER
        mock_login.return_value = self.FAKE_JWT_TOKEN
        app_login()

        expected_bearer = "Basic " + self.ENCODED_CREDS
        mock_login.assert_called_with(expected_bearer)
