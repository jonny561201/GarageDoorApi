from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.jwt_utils import is_jwt_valid


def get_sump_level(user_id, bearer_token):
    is_jwt_valid(bearer_token)
    with UserDatabaseManager() as database:
        depth = database.get_current_sump_level_by_user(user_id)
        return {'currentDepth': depth, 'userId': user_id}
