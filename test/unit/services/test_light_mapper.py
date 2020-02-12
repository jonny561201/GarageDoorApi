from svc.services.light_mapper import map_light_groups


def test_map_light_groups__should_map_group_ids_into_list():
    response = {'1': {'name': 'Test'}, '2': {'name': 'other'}}

    actual = map_light_groups(response)

    assert len(actual) == 2
    assert actual[0]['groupId'] == '1'
    assert actual[1]['groupId'] == '2'


def test_map_light_groups__should_map_group_name():
    response = {
        "1": {
            "devicemembership": [],
            "etag": "ab5272cfe11339202929259af22252ae",
            "hidden": False,
            "name": "Living Room"
        }
    }

    actual = map_light_groups(response)

    assert actual[0]['groupName'] == 'Living Room'
