import pytest
from mock import patch
from werkzeug.exceptions import Unauthorized

from svc.utilities.api_key_utils import get_generate_api_key, validate_api_key


@patch('svc.utilities.api_key_utils.save_api_key')
@patch('svc.utilities.api_key_utils.get_api_key')
class TestGetGenerateApiKey:
    STORED_KEY = 'existing_fake_key'

    def test_get_generate_api_key__should_return_existing_key_when_found(self, mock_get, mock_save):
        mock_get.return_value = self.STORED_KEY

        actual = get_generate_api_key()

        assert actual == self.STORED_KEY

    def test_get_generate_api_key__should_not_save_when_key_exists(self, mock_get, mock_save):
        mock_get.return_value = self.STORED_KEY

        get_generate_api_key()

        mock_save.assert_not_called()

    def test_get_generate_api_key__should_generate_new_key_when_none_exists(self, mock_get, mock_save):
        mock_get.return_value = None

        actual = get_generate_api_key()

        assert actual is not None
        assert len(actual) == 64

    def test_get_generate_api_key__should_save_generated_key(self, mock_get, mock_save):
        mock_get.return_value = None

        actual = get_generate_api_key()

        mock_save.assert_called_once_with(actual)


@patch('svc.utilities.api_key_utils.get_api_key')
class TestValidateApiKey:
    STORED_KEY = 'valid_api_key'

    def test_validate_api_key__should_not_raise_when_key_matches(self, mock_get):
        mock_get.return_value = self.STORED_KEY

        validate_api_key(self.STORED_KEY)

    def test_validate_api_key__should_raise_unauthorized_when_key_does_not_match(self, mock_get):
        mock_get.return_value = self.STORED_KEY

        with pytest.raises(Unauthorized):
            validate_api_key('wrong_key')

    def test_validate_api_key__should_raise_unauthorized_when_no_stored_key(self, mock_get):
        mock_get.return_value = None

        with pytest.raises(Unauthorized):
            validate_api_key('any_key')

    def test_validate_api_key__should_raise_unauthorized_when_api_key_is_none(self, mock_get):
        mock_get.return_value = self.STORED_KEY

        with pytest.raises(Unauthorized):
            validate_api_key(None)

