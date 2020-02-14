def map_light_groups(api_response, group_state):
    return [__map_group(k, v) for k, v in api_response.items()]


def __map_group(group_id, group):
    return {'groupId': group_id, 'groupName': group['name']}
