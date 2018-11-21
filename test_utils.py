from unittest import TestCase

import utils
from py_modules.pyadb import ADB

class TestUtils(TestCase):
    def test_get_pid_on_device(self):
        adb = ADB()
        adb.enable_debug()
        adb.set_adb_path()
        adb.set_target_device()

        pid = utils.get_pid_on_device(adb, 'com.android.commands.monkey')
        utils.kill_proc_on_device(adb, pid)
        print(pid)
