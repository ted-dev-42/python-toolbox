import logging
from unittest import TestCase
import log

class TestLog(TestCase):
    def test_init(self):
        log.init("TEST", "logs/log.txt")
        logging.info("this is a test")


