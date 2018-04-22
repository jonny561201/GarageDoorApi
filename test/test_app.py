from app import garage_door_status


def test_garage_door_status__should_return_success_status_code():
    actual = garage_door_status()

    assert actual.status_code == 200


def test_garage_door_status__should_return_success_header():
    expected_headers = 'text/json'

    actual = garage_door_status()

    assert actual.content_type == expected_headers


def test_garage_door_status__should_return_response_body():
    expected_body = '{"garageStatus": true}'

    actual = garage_door_status()

    assert actual.data == expected_body

