from unittest import TestCase

import py_common.utils
from pyadb import ADB

class TestUtils(TestCase):
    def test_get_pid_on_device(self):
        adb = ADB()
        adb.enable_debug()
        adb.set_adb_path()
        adb.set_target_device()

        pid = py_common.utils.get_pid_on_device(adb, 'com.android.commands.monkey')
        py_common.utils.kill_proc_on_device(adb, pid)
        print(pid)

    def test_cut_string(self):
        s = 'storage/sdcard0/ylog'
        print(s[:s.rfind("/")])
        print(s[s.rfind("/")+1:])
