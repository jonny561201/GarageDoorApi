def map_light_groups(api_response, group_state):
    return [__map_group(k, v, group_state) for k, v in api_response.items()]


def __map_group(group_id, group, group_state):
    id_state = group_state[group_id]['action']['on']
    return {'groupId': group_id, 'groupName': group['name'], 'on': id_state}
