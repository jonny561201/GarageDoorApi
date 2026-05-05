import pytest
from mock import patch, MagicMock
from werkzeug.exceptions import Unauthorized

from svc.controllers import app_controller


@patch('svc.controllers.app_controller.validate_api_key')
@patch('svc.controllers.app_controller.get_generate_api_key')
class TestConfirmRegistration:
    PROVIDED_KEY = 'provided_api_key'
    GENERATED_KEY = 'generated_api_key'

    def setup_method(self):
        self.mdns = MagicMock()

    def test_confirm_registration__should_validate_provided_key(self, mock_generate, mock_validate):
        app_controller.confirm_registration({'api_key': self.PROVIDED_KEY}, self.mdns)

        mock_validate.assert_called_once_with(self.PROVIDED_KEY)

    def test_confirm_registration__should_return_provided_key_when_valid(self, mock_generate, mock_validate):
        actual = app_controller.confirm_registration({'api_key': self.PROVIDED_KEY}, self.mdns)

        assert actual == self.PROVIDED_KEY
        mock_generate.assert_not_called()

    def test_confirm_registration__should_unregister_mdns_when_key_valid(self, mock_generate, mock_validate):
        app_controller.confirm_registration({'api_key': self.PROVIDED_KEY}, self.mdns)

        self.mdns.unregister.assert_called_once()

    def test_confirm_registration__should_propagate_unauthorized_when_key_invalid(self, mock_generate, mock_validate):
        mock_validate.side_effect = Unauthorized()

        with pytest.raises(Unauthorized):
            app_controller.confirm_registration({'api_key': 'wrong'}, self.mdns)

    def test_confirm_registration__should_not_unregister_when_key_invalid(self, mock_generate, mock_validate):
        mock_validate.side_effect = Unauthorized()

        with pytest.raises(Unauthorized):
            app_controller.confirm_registration({'api_key': 'wrong'}, self.mdns)

        self.mdns.unregister.assert_not_called()

    def test_confirm_registration__should_generate_when_body_is_none(self, mock_generate, mock_validate):
        mock_generate.return_value = self.GENERATED_KEY

        actual = app_controller.confirm_registration(None, self.mdns)

        assert actual == self.GENERATED_KEY
        mock_validate.assert_not_called()

    def test_confirm_registration__should_generate_when_body_missing_key(self, mock_generate, mock_validate):
        mock_generate.return_value = self.GENERATED_KEY

        actual = app_controller.confirm_registration({}, self.mdns)

        assert actual == self.GENERATED_KEY
        mock_validate.assert_not_called()

    def test_confirm_registration__should_unregister_after_generating(self, mock_generate, mock_validate):
        mock_generate.return_value = self.GENERATED_KEY

        app_controller.confirm_registration(None, self.mdns)

        self.mdns.unregister.assert_called_once()
