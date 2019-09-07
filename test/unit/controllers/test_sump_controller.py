import uuid

from mock import patch

from svc.controllers.sump_controller import get_sump_level


@patch('svc.controllers.sump_controller.is_jwt_valid')
@patch('svc.controllers.sump_controller.UserDatabaseManager')
def test_get_sump_level__should_call_get_current_sump_level_by_user(mock_database,mock_jwt):
    user_id = uuid.uuid4().hex
    bearer_token = 'abdsadf2345'
    get_sump_level(user_id, bearer_token)

    mock_database.return_value.__enter__.return_value.get_current_sump_level_by_user.assert_called_with(user_id)


@patch('svc.controllers.sump_controller.is_jwt_valid')
@patch('svc.controllers.sump_controller.UserDatabaseManager')
def test_get_sump_level__should_return_response_with_distance(mock_database, mock_jwt):
    distance = 3.14159
    bearer_token = 'asdflkhsad98778236'
    user_id = 'fake12354'
    mock_database.return_value.__enter__.return_value.get_current_sump_level_by_user.return_value = distance

    actual = get_sump_level(user_id, bearer_token)

    assert actual == {'currentDepth': distance, 'userId': user_id}


@patch('svc.controllers.sump_controller.is_jwt_valid')
@patch('svc.controllers.sump_controller.UserDatabaseManager')
def test_get_sump_level__should_call_is_jwt_valid(mock_database, mock_jwt):
    user_id = 'fake1234'
    bearer_token = 'lkhasdhlufiou0892390784'

    get_sump_level(user_id, bearer_token)

    mock_jwt.assert_called_with(bearer_token)


@patch('svc.controllers.sump_controller.is_jwt_valid')
@patch('svc.controllers.sump_controller.UserDatabaseManager')
def test_get_sump_level__should_call_get_average_sump_level_by_user(mock_database, mock_jwt):
    user_id = 'fake1234'
    bearer_token = 'lkhasdhlufiou0892390784'

    get_sump_level(user_id, bearer_token)

    mock_database.return_value.__enter__.return_value.get_average_sump_level_by_user.assert_called_with(user_id)
