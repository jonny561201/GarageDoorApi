import atexit
import socket

from zeroconf import ServiceInfo, Zeroconf


class MdnsRegistration:
    SERVICE_TYPE = '_http._tcp.local.'
    SERVICE_NAME = 'garage-door._http._tcp.local.'

    def __init__(self, port):
        self._port = port
        self._zeroconf = None
        self._service_info = None

    def register(self):
        print('registering Mdns Registration')
        ip_address = _get_local_ip()
        self._service_info = ServiceInfo(
            type_=self.SERVICE_TYPE,
            name=self.SERVICE_NAME,
            addresses=[socket.inet_aton(ip_address)],
            port=self._port,
            properties={'service': 'garage-door', 'max_nodes': '2'},
        )
        self._zeroconf = Zeroconf()
        self._zeroconf.register_service(self._service_info)
        atexit.register(self.unregister)

    def unregister(self):
        print('Unregistering Mdns Registration')
        if self._zeroconf is not None and self._service_info is not None:
            self._zeroconf.unregister_service(self._service_info)
            self._zeroconf.close()
            self._zeroconf = None
            self._service_info = None


def _get_local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except OSError:
        return '127.0.0.1'
