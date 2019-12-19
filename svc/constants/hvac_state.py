class HvacState:
    __instance = None
    DESIRED_TEMP = None
    MODE = None
    ACTIVE_THREAD = None
    STOP_EVENT = None

    def __init__(self):
        if HvacState.__instance is not None:
            raise Exception
        else:
            HvacState.__instance = self

    @staticmethod
    def get_instance():
        if HvacState.__instance is None:
            HvacState.__instance = HvacState()
        return HvacState.__instance

