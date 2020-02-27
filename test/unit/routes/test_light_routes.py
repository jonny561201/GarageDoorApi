import json

from mock import patch

from svc.routes.light_routes import get_assigned_light_groups, set_assigned_light_group, get_lights_assigned_to_group, \
    set_light_state


@patch('svc.routes.light_routes.request')
@patch('svc.routes.light_routes.light_controller')
class TestLightRoutes:

    def test_get_assigned_light_groups__should_call_get_assigned_lights(self, mock_controller, mock_request):
        bearer_token = 'not real'
        mock_request.headers = {'Authorization': bearer_token}
        mock_controller.get_assigned_light_groups.return_value = {}

        get_assigned_light_groups()

        mock_controller.get_assigned_light_groups.assert_called_with(bearer_token)

    def test_get_assigned_light_groups__should_return_success_status_code(self, mock_controller, mock_request):
        mock_controller.get_assigned_light_groups.return_value = {}
        actual = get_assigned_light_groups()

        assert actual.status_code == 200

    def test_get_assigned_light_groups__should_return_success_headers(self, mock_controller, mock_request):
        mock_controller.get_assigned_light_groups.return_value = {}
        actual = get_assigned_light_groups()

        assert actual.content_type == 'text/json'

    def test_get_assigned_light_groups__should_response_from_controller(self, mock_controller, mock_request):
        result = {'response': 'not important'}
        mock_controller.get_assigned_light_groups.return_value = result
        actual = get_assigned_light_groups()

        assert json.loads(actual.data) == result

    def test_set_assigned_light_group__should_call_light_controller(self, mock_controller, mock_request):
        bearer_token = 'fakeBearer'
        request_data = '{"on": "False", "groupId": 1}'
        mock_request.headers = {'Authorization': bearer_token}
        mock_request.data = request_data.encode()

        set_assigned_light_group()

        mock_controller.set_assigned_light_groups.assert_called_with(bearer_token, json.loads(request_data))

    def test_set_assigned_light_group__should_return_success_status_code(self, mock_controller, mock_request):
        mock_request.data = '{}'.encode('UTF-8')
        actual = set_assigned_light_group()

        assert actual.status_code == 200

    def test_set_assigned_light_group__should_return_success_headers(self, mock_controller, mock_request):
        mock_request.data = '{}'.encode('UTF-8')
        actual = set_assigned_light_group()

        assert actual.content_type == 'text/json'

    def test_get_lights_assigned_to_group__should_call_light_controller(self, mock_controller, mock_request):
        group_id = '5'
        mock_controller.get_assigned_lights.return_value = {}
        bearer_token = 'fakeBearerToken'
        mock_request.headers = {'Authorization': bearer_token}
        get_lights_assigned_to_group(group_id)

        mock_controller.get_assigned_lights.assert_called_with(bearer_token, group_id)

    def test_get_lights_assigned_to_group__should_return_success_status_code(self, mock_controller, mock_request):
        group_id = '3'
        mock_controller.get_assigned_lights.return_value = {}
        actual = get_lights_assigned_to_group(group_id)

        assert actual.status_code == 200

    def test_get_lights_assigned_to_group__should_return_success_headers(self, mock_controller, mock_request):
        group_id = '3'
        mock_controller.get_assigned_lights.return_value = {}
        actual = get_lights_assigned_to_group(group_id)

        assert actual.content_type == 'text/json'

    def test_get_lights_assigned_to_group__should_return_response(self, mock_controller, mock_request):
        group_id = '5'
        expected_response = {'test': 'fake'}
        mock_controller.get_assigned_lights.return_value = expected_response
        actual = get_lights_assigned_to_group(group_id)

        assert json.loads(actual.data) == expected_response

    def test_set_light_state__should_call_light_controller(self, mock_controller, mock_requests):
        bearer_token = 'fakeBearerToken'
        mock_requests.headers = {'Authorization': bearer_token}
        request = '{"on": "False", "brightness": 133, "lightId": "3"}'
        mock_requests.data = request.encode()
        set_light_state()

        mock_controller.set_assigned_light.assert_called_with(bearer_token, json.loads(request))

    def test_set_light_state__should_return_success_status_code(self, mock_controller, mock_request):
        mock_request.data = '{}'.encode('UTF-8')
        actual = set_light_state()

        assert actual.status_code == 200

    def test_set_light_state__should_return_success_headers(self, mock_controller, mock_request):
        mock_request.data = '{}'.encode('UTF-8')
        actual = set_light_state()

        assert actual.content_type == 'text/json'
