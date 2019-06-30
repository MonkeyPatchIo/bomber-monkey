class State(object):
    def __init__(self):
        self.stop_requested = False

    def init(self):
        raise NotImplementedError

    def start(self):
        self.stop_requested = False
        self._start()
        while not self.stop_requested:
            self._run()

    def stop(self):
        self.stop_requested = True
        self._stop()

    def _start(self):
        pass

    def _stop(self):
        pass

    def _run(self):
        raise NotImplementedError()
