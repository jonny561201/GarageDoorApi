from svc.db.methods.user_credentials import UserDatabaseManager


def get_sump_level(user_id):
    with UserDatabaseManager() as database:
        depth = database.get_current_sump_level_by_user(user_id)
        return {'currentDepth': depth, 'userId': user_id}
