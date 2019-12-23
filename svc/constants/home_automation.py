class Mode:
    BLOWER = 'blower'
    COOLING = 'cooling'
    HEATING = 'heating'
    TURN_OFF = 'off'


class Hvac:
    FURNACE = 'furnace'
    AIR_CONDITIONING = 'ac'


class Time:
    ONE_MINUTE = 60
    TEN_MINUTE = 600


class Automation:
    MODE = Mode()
    HVAC = Hvac()
    TIME = Time()
