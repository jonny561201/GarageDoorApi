import base64
import json

from mock import patch, ANY

from svc.routes.app_routes import app_login, get_user_preferences_by_user_id, update_user_preferences_by_user_id


@patch('svc.routes.app_routes.request')
class TestAppRoutes:
    USER = 'user_name'
    USER_ID = '123bac34'
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

    @patch('svc.routes.app_routes.get_user_preferences')
    def test_get_user_preferences_by_user_id__should_call_app_controller_with_user_id(self, mock_controller, mock_requests):
        mock_controller.return_value = {}
        get_user_preferences_by_user_id(self.USER_ID)

        mock_controller.assert_called_with(ANY, self.USER_ID)

    @patch('svc.routes.app_routes.get_user_preferences')
    def test_get_user_preferences_by_user_id__should_call_app_controller_with_bearer_token(self, mock_controller, mock_requests):
        mock_requests.headers = {'Authorization': self.FAKE_JWT_TOKEN}
        mock_controller.return_value = {}
        get_user_preferences_by_user_id(self.USER_ID)

        mock_controller.assert_called_with(self.FAKE_JWT_TOKEN, ANY)

    @patch('svc.routes.app_routes.get_user_preferences')
    def test_get_user_preferences_by_user_id__should_return_preference_response(self, mock_controller, mock_requests):
        expected_response = {'unit': 'metric', 'city': 'London'}
        mock_controller.return_value = expected_response

        actual = get_user_preferences_by_user_id(self.USER_ID)

        assert json.loads(actual.data) == expected_response

    @patch('svc.routes.app_routes.get_user_preferences')
    def test_get_user_preferences_by_user_id__should_return_success_status_code(self, mock_controller, mock_requests):
        mock_controller.return_value = {}

        actual = get_user_preferences_by_user_id(self.USER_ID)

        assert actual.status_code == 200

    @patch('svc.routes.app_routes.save_user_preferences')
    def test_update_user_preferences_by_user_id__should_call_app_controller_with_user_id(self, mock_controller, mock_requests):
        update_user_preferences_by_user_id(self.USER_ID)

        mock_controller.assert_called_with(ANY, self.USER_ID, ANY)

    @patch('svc.routes.app_routes.save_user_preferences')
    def test_update_user_preferences_by_user_id__should_call_app_controller_with_bearer_token(self, mock_controller, mock_requests):
        mock_requests.headers = {'Authorization': self.FAKE_JWT_TOKEN}
        update_user_preferences_by_user_id(self.USER_ID)

        mock_controller.assert_called_with(self.FAKE_JWT_TOKEN, ANY, ANY)

    @patch('svc.routes.app_routes.save_user_preferences')
    def test_update_user_preferences_by_user_id__should_call_app_controller_with_request_data(self, mock_controller, mock_requests):
        expected_data = json.dumps({}).encode()
        mock_requests.data = expected_data
        update_user_preferences_by_user_id(self.USER_ID)

        mock_controller.assert_called_with(ANY, ANY, expected_data)

    @patch('svc.routes.app_routes.save_user_preferences')
    def test_update_user_preferences_by_user_id__should_return_success_status_code(self, mock_controller, mock_requests):
        actual = update_user_preferences_by_user_id(self.USER_ID)

        assert actual.status_code == 200

    @patch('svc.routes.app_routes.save_user_preferences')
    def test_update_user_preferences_by_user_id__should_return_success_status_code(self, mock_controller, mock_requests):
        actual = update_user_preferences_by_user_id(self.USER_ID)

        assert actual.content_type == 'text/json'
