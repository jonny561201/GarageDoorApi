from flask import Response

from app import garage_door_status


def test_garage_door_status__should_return_success_response():
    expected = Response(status=200)

    actual = garage_door_status()

    assert actual.status_code == expected.status_code
