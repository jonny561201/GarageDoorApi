import base64

from svc.utilities.credentials import extract_credentials


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
