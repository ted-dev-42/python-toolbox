from unittest import TestCase

import ylog


class TestYlog(TestCase):
    def test_start(self):
        ylog.start()

    def test_stop(self):
        ylog.start()
        ylog.stop()

    def test_clear(self):
        ylog.clear()

    def test_running(self):
        ylog.start()
        assert ylog.is_running()
        ylog.stop()
        assert not ylog.is_running()
