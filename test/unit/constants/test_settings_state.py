from svc.config.settings_state import Settings


class TestSettingsState:
    COORDINATES = {'latitude': 40.123, 'longitude': -93.123}
    VALUES = {'GarageFile': 'other_file.json', 'JwtSecret': 'other_secret', 'Environment': 'test', 'ApiKeyFile': 'test.json'}
    QUEUE = {'Host': 'test_host', 'Port': 1234, 'VHost': 'test_vhost', 'Exchange': 'test_exchange'}

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        self.SETTINGS._settings = self.VALUES
        self.SETTINGS.Coordinates._settings = self.COORDINATES
        self.SETTINGS.Queue._settings = self.QUEUE

    def test_environment__should_return(self):
        assert self.SETTINGS.environment == self.VALUES['Environment']

    def test_environment__should_default_to_local(self):
        self.SETTINGS._settings = None
        assert self.SETTINGS.environment == 'local'

    def test_coordinates__should_return(self):
        assert self.SETTINGS.Coordinates.latitude == self.COORDINATES['latitude']
        assert self.SETTINGS.Coordinates.longitude == self.COORDINATES['longitude']

    def test_coordinates__should_default_when_settings_not_provided(self):
        self.SETTINGS.Coordinates._settings = {}
        assert self.SETTINGS.Coordinates.latitude == 41.621191
        assert self.SETTINGS.Coordinates.longitude == -93.831609

    def test_garage_file__should_return(self):
        assert self.SETTINGS.garage_file == self.VALUES['GarageFile']

    def test_api_key_file__should_return(self):
        assert self.SETTINGS.api_key_file == self.VALUES['ApiKeyFile']

    def test_file_name__should_provide_default(self):
        self.SETTINGS._settings = None
        assert self.SETTINGS.garage_file == 'garageStatus.json'

    def test_queue_host__should_return(self):
        assert self.SETTINGS.Queue.host == self.QUEUE['Host']

    def test_queue_vhost__should_return(self):
        assert self.SETTINGS.Queue.vhost == self.QUEUE['VHost']

    def test_queue_port__should_return(self):
        assert self.SETTINGS.Queue.port == self.QUEUE['Port']

    def test_queue_exchange__should_return(self):
        assert self.SETTINGS.Queue.exchange == self.QUEUE['Exchange']
