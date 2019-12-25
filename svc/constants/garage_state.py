class GarageState:
    __instance = None
    STATUS = None
    OPEN_TIME = None
    CLOSED_TIME = None
    STOP_EVENT = None
    ACTIVE_THREAD = None

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
