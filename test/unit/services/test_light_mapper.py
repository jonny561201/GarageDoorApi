from svc.services.light_mapper import map_light_groups


def test_map_light_groups__should_map_group_ids_into_list():
    response = {'1': {'name': 'Test'}, '2': {'name': 'other'}}
    group = {'1': {'action': {'on': False}}, '2': {'action': {'on': False}}}

    actual = map_light_groups(response, group)

    assert len(actual) == 2
    assert actual[0]['groupId'] == '1'
    assert actual[1]['groupId'] == '2'


def test_map_light_groups__should_map_group_name():
    group = {'1': {'action': {'on': False}}}
    response = {
        "1": {
            "name": "Living Room"
        }
    }

    actual = map_light_groups(response, group)

    assert actual[0]['groupName'] == 'Living Room'


def test_map_light_groups__should_map_the_group_state():
    response = {
        "1": {
            "name": "Living Room"
        },
        "3": {
            "name": "Dinning Room"
        }
    }
    group_state = {'1': {'action': {'on': False}}, '3': {'action': {'on': True}}}
    actual = map_light_groups(response, group_state)

    assert actual[0]['groupName'] == 'Living Room'
    assert actual[0]['on'] is False
    assert actual[1]['groupName'] == 'Dinning Room'
    assert actual[1]['on'] is True


def test_map_light_groups__should_default_the_group_state():
    response = {
        "1": {
            "name": "Bed Room"
        }
    }
    group_state = {'1': {'action': {}}}
    actual = map_light_groups(response, group_state)

    assert actual[0]['groupName'] == 'Bed Room'
    assert actual[0]['on'] is False
