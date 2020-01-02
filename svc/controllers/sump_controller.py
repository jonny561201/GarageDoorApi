import json

from svc.db.methods.user_credentials import UserDatabaseManager
from svc.utilities.conversion_utils import convert_to_imperial
from svc.utilities.jwt_utils import is_jwt_valid


def get_sump_level(user_id, bearer_token):
    is_jwt_valid(bearer_token)
    with UserDatabaseManager() as database:
        current_data = database.get_current_sump_level_by_user(user_id)
        average_data = database.get_average_sump_level_by_user(user_id)
        preferences = database.get_preferences_by_user(user_id)

        is_imperial = preferences['is_imperial']
        current_distance = convert_to_imperial(current_data['currentDepth'], is_imperial)
        average_distance = convert_to_imperial(average_data['averageDepth'], is_imperial)
        current_data['currentDepth'] = current_distance
        average_data['averageDepth'] = average_distance
        current_data['depthUnit'] = 'in' if is_imperial else 'cm'
        current_data.update(average_data)

        return current_data


def save_current_level(user_id, bearer_token, request):
    is_jwt_valid(bearer_token)
    depth_info = json.loads(request)
    with UserDatabaseManager() as database:
        database.insert_current_sump_level(user_id, depth_info)
