class Mime:
    JSON = 'application/json'
    HTML = 'text/html'
    TEXT = 'text/plain'
    XML = 'application/xml'
    JPG = 'image/jpeg'
    PNG = 'image/png'


class Garage:
    OPEN = True
    CLOSED = False
    QUEUE = 'home-automation-garage'


class Timing:
    FIVE_SECONDS = 5
    TEN_SECONDS = 10
    FIFTEEN_SECONDS = 15
    THIRTY_SECONDS = 30
    ONE_MINUTE = 60
    FIVE_MINUTES = 300
    TEN_MINUTE = 600


class Automation:
    APP_NAME = "Soaring Leaf Home Automation"
    TIMING = Timing
    GARAGE = Garage
