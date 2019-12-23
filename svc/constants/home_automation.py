class Mode:
    BLOWER = 'blower'
    COOLING = 'cooling'
    HEATING = 'heating'
    OFF = 'off'


class Hvac:
    FURNACE = 'furnace'
    AIR_CONDITIONING = 'ac'
    TURN_OFF = 'off'


class Time:
    ONE_MINUTE = 60
    TEN_MINUTE = 600


class Automation:
    MODE = Mode()
    HVAC = Hvac()
    TIME = Time()
