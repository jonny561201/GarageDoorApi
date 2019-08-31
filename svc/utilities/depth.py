SPEED_OF_SOUND = 34300


def get_depth_by_intervals(start, stop):
    interval = stop - start

    distance = (interval * SPEED_OF_SOUND) / 2

    return distance
