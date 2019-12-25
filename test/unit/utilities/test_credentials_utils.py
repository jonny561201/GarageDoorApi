import base64

import pytest
from werkzeug.exceptions import BadRequest

from svc.utilities.credentials_utils import extract_credentials


def test_extract_credentials__should_return_valid_credentials():
    user = "user"
    pword = "password"
    creds = "%s:%s" % (user, pword)
    encoded_token = base64.b64encode(creds.encode())
    bearer_token = "Basic %s" % encoded_token.decode('UTF-8')

    actual_user, actual_pass = extract_credentials(bearer_token)

    assert actual_pass == pword
    assert actual_user == user


def test_extract_credentials__should_return_valid_credentials_when_missing_basic():
    user = "user"
    pword = "password"
    creds = "%s:%s" % (user, pword)
    encoded_token = base64.b64encode(creds.encode())
    bearer_token = encoded_token.decode('UTF-8')

    actual_user, actual_pass = extract_credentials(bearer_token)

    assert actual_pass == pword
    assert actual_user == user


def test_extract_credentials__should_throw_bad_request_when_no_token():
    with pytest.raises(BadRequest):
        extract_credentials(None)


def test_extract_credentials__should():
    with pytest.raises(BadRequest):
        extract_credentials("")
