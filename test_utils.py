from unittest import TestCase

import utils
from py_modules.pyadb import ADB

class TestUtils(TestCase):
    def test_get_pid_on_device(self):
        adb = ADB()
        adb.enable_debug()
        adb.set_adb_path()
        adb.set_target_device()

        pid = utils.get_pid_on_device(adb, 'com.sprd.commlog')
        print(pid)
