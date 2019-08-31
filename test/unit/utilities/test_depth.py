from svc.utilities.depth import get_depth_by_intervals


def test_get_depth_by_intervals__should_calculate_distance_with_times():
    start_time = 1567284125516
    stop_time = 1567284128379

    actual = get_depth_by_intervals(start_time, stop_time)

    assert actual == 49100450.0
