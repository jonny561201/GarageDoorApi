SPEED_OF_SOUND = 34300


# returns depth in cm
def get_depth_by_intervals(start, stop):
    interval = stop - start

    distance = (interval * SPEED_OF_SOUND) / 2

    return distance
