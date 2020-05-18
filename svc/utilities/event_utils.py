from threading import Thread, Event

from svc.constants.home_automation import Automation


class MyThread(Thread):
    def __init__(self, event, sched_function, garage_id, function_interval):
        Thread.__init__(self)
        self.garage_id = garage_id
        self.stopped = event
        self.function = sched_function
        self.interval = function_interval

    def run(self):
        while not self.stopped.wait(self.interval):
            self.function(self.garage_id)


def create_thread(state, fn, garage_id, delay=Automation.TIMING.FIVE_SECONDS):
    stop_event = Event()
    state['stop_event'] = stop_event
    state['active_thread'] = MyThread(stop_event, fn, garage_id, delay)
    state['active_thread'].start()
