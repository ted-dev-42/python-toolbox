from unittest import TestCase
from adb import ADB


class TestAdb(TestCase):

    def test_get_devices(self):
        adb = ADB()
        adb.set_adb_path()
        adb.start_server()
        err, devices = adb.get_devices()
        print(str(err))
        if len(devices) > 0:
            print(str(devices))

    def test_install(self):
        adb = ADB()
        adb.set_adb_path()
        _, ds = adb.get_devices()
        device_id = ds[0]
        adb.set_target_device(device_id)
        adb.enable_debug()
        output = adb.install(reinstall=True, pkgapp='ctssetup.apk')
        print("output: " + str(output))
