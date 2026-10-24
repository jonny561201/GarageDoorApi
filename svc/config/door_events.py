import threading

from svc.config.singleton import Singleton


@Singleton
class DoorEvents:
    def __init__(self):
        self._version = 0
        self._condition = threading.Condition()

    def notify(self):
        with self._condition:
            self._version += 1
            self._condition.notify_all()

    def current_version(self):
        with self._condition:
            return self._version

    def wait_for_change(self, seen_version, timeout):
        with self._condition:
            if self._version == seen_version:
                self._condition.wait(timeout)
            return self._version if self._version != seen_version else None
