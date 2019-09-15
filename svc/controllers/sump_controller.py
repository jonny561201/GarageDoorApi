from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.jwt_utils import is_jwt_valid


def get_sump_level(user_id, bearer_token):
    is_jwt_valid(bearer_token)
    with UserDatabaseManager() as database:
        depth = database.get_current_sump_level_by_user(user_id)
        average = database.get_average_sump_level_by_user(user_id)

        response = {'currentDepth': depth, 'userId': user_id}
        response.update(average)

        return response


def save_current_level(bearer_token, depth_info):
    is_jwt_valid(bearer_token)
