class GarageState:
    __instance = None
    DOORS = {1: {'status': None,
                 'open_time': None,
                 'closed_time': None,
                 'stop_event': None,
                 'active_thread': None},
             2: {'status': None,
                 'open_time': None,
                 'closed_time': None,
                 'stop_event': None,
                 'active_thread': None}
             }

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
