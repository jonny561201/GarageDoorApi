import socket

from mock import patch, MagicMock

from svc.utilities.mdns_registration import MdnsRegistration


class TestMdnsRegistration:
    PORT = 5001

    def setup_method(self):
        self.mdns = MdnsRegistration(self.PORT)

    @patch('svc.utilities.mdns_registration._get_local_ip')
    @patch('svc.utilities.mdns_registration.Zeroconf')
    @patch('svc.utilities.mdns_registration.ServiceInfo')
    def test_register__should_create_service_info_with_ip_and_port(self, mock_info, mock_zeroconf, mock_ip):
        mock_ip.return_value = '192.168.1.50'
        mock_zeroconf.return_value = MagicMock()

        self.mdns.register()

        mock_info.assert_called_once_with(
            type_=MdnsRegistration.SERVICE_TYPE,
            name=MdnsRegistration.SERVICE_NAME,
            addresses=[socket.inet_aton('192.168.1.50')],
            port=self.PORT,
            properties={'service': 'garage-door'},
        )

    @patch('svc.utilities.mdns_registration._get_local_ip')
    @patch('svc.utilities.mdns_registration.Zeroconf')
    @patch('svc.utilities.mdns_registration.ServiceInfo')
    def test_register__should_register_service_with_zeroconf(self, mock_info, mock_zeroconf, mock_ip):
        mock_ip.return_value = '192.168.1.50'
        mock_zc_instance = MagicMock()
        mock_zeroconf.return_value = mock_zc_instance

        self.mdns.register()

        mock_zc_instance.register_service.assert_called_once_with(mock_info.return_value)

    def test_unregister__should_unregister_and_close(self):
        mock_zc = MagicMock()
        mock_info = MagicMock()
        self.mdns._zeroconf = mock_zc
        self.mdns._service_info = mock_info

        self.mdns.unregister()

        mock_zc.unregister_service.assert_called_once_with(mock_info)
        mock_zc.close.assert_called_once()

    def test_unregister__should_clear_instance_state(self):
        self.mdns._zeroconf = MagicMock()
        self.mdns._service_info = MagicMock()

        self.mdns.unregister()

        assert self.mdns._zeroconf is None
        assert self.mdns._service_info is None

    def test_unregister__should_not_fail_when_not_registered(self):
        self.mdns.unregister()
