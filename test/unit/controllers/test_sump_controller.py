import uuid

from mock import patch

from svc.controllers.sump_controller import get_sump_level


@patch('svc.controllers.sump_controller.UserDatabaseManager')
def test_get_sump_level__should_call_get_current_sump_level_by_user(mock_database):
    user_id = uuid.uuid4().hex
    get_sump_level(user_id)

    mock_database.return_value.__enter__.return_value.get_current_sump_level_by_user.assert_called_with(user_id)


@patch('svc.controllers.sump_controller.UserDatabaseManager')
def test_get_sump_level__should_return_response_with_distance(mock_database):
    distance = 3.14159
    user_id = 'fake12354'
    mock_database.return_value.__enter__.return_value.get_current_sump_level_by_user.return_value = distance

    actual = get_sump_level(user_id)

    assert actual == {'currentDepth': distance, 'userId': user_id}
