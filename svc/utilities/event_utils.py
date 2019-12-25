from threading import Thread


class MyThread(Thread):
    def __init__(self, event, sched_function, function_interval):
        Thread.__init__(self)
        self.stopped = event
        self.function = sched_function
        self.interval = function_interval

    def run(self):
        while not self.stopped.wait(self.interval):
            self.function()
