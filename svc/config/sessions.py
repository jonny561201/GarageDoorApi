import threading

from svc.config.singleton import Singleton


@Singleton
class Session:
    def __init__(self):
        self._timers = {}
        self._lock = threading.Lock()

    def set_timer(self, door_id, timer):
        with self._lock:
            existing = self._timers.get(door_id)
            if existing is not None:
                existing.cancel()
            self._timers[door_id] = timer

    def clear_timer(self, door_id):
        with self._lock:
            existing = self._timers.pop(door_id, None)
        if existing is None:
            return False
        existing.cancel()
        return True
