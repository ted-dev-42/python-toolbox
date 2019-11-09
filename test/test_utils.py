import os
from unittest import TestCase

import utils
from adb import ADB

class TestUtils(TestCase):
    def test_get_pid_on_device(self):
        adb = ADB()
        adb.enable_debug()
        adb.set_adb_path()
        adb.set_target_device()

        pid = utils.get_pid_on_device(adb, 'com.android.commands.monkey')
        utils.kill_proc_on_device(adb, pid)
        print(pid)

    def test_cut_string(self):
        s = 'storage/sdcard0/ylog'
        print(s[:s.rfind("/")])
        print(s[s.rfind("/")+1:])

    def test_exec_cmd_live(self):
        utils.exec_cmd_live("adb pull /sdcard/ylog/ap")

    def test_exec_cmd_live2(self):
        for line in utils.exec_cmd_live2("adb pull /sdcard/ylog/ap"):
            print(line)

    def test_exec_cmd_3(self):
        os.system("adb pull /sdcard/ylog/ap")
