from unittest import TestCase

import ptty

class TestExec(TestCase):
    def test_exec_cmd_linux(self):
        ptty.exec_cmd_linux("adb pull /sdcard/ylog/ap")

    def test_exec_cmd_windows(self):
        ptty.exec_cmd_windows("adb pull /sdcard/ylog/ap")
