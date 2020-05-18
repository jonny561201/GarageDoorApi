class DoorState:
    ACTIVE_THREAD = None
    STOP_EVENT = None
    CLOSED_TIME = None
    OPEN_TIME = None
    STATUS = None


class GarageState:
    __instance = None
    DOORS = {'1': DoorState(),
             '2': DoorState()}

    def __init__(self):
        if GarageState.__instance is not None:
            raise Exception
        else:
            GarageState.__instance = self

    @staticmethod
    def get_instance():
        if GarageState.__instance is None:
            GarageState.__instance = GarageState()
        return GarageState.__instance
