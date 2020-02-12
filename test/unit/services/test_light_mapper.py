from svc.services.light_mapper import map_light_groups


def test_map_light_groups__should_return_items_in_list():
    response = {'1': {}, '2': {}}

    actual = map_light_groups(response)

    assert len(actual) == 2
    assert actual[0]['groupId'] == '1'
    assert actual[1]['groupId'] == '2'
