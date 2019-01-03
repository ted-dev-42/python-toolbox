from threading import Event


class Sleep(object):
    def __init__(self):
        self.event = Event()
        self._aborted = False

    def __call__(self, secs):
        self.event.wait(timeout=secs)
        return not self._aborted

    def wake(self):
        self.event.set()
        self._aborted = True
