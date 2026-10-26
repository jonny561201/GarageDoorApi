class Mime:
    JSON = 'application/json'
    EVENT_STREAM = 'text/event-stream'


class Garage:
    QUEUE = 'home-automation-garage'
    FIRST_STATUS_PIN = 11
    FIRST_UPDATE_PIN = 31
    SECOND_STATUS_PIN = 12
    SECOND_UPDATE_PIN = 33
    DOOR_IDS = ['1', '2']
    WATCH_INTERVAL_SECONDS = 1
    RECONNECT_SECONDS = 5
    STREAM_HEARTBEAT_SECONDS = 20
