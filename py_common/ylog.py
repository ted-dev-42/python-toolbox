import logging

from adb import ADB
from distutils.version import StrictVersion

adb = ADB()
device = None
version = "0.0.0"


def set_device(device_id):
    global device
    device = device_id
    logging.info("set device: " + device)
    init_adb()


def is_legacy_ylog():
    return StrictVersion(version) < StrictVersion("3.0.0")


def init_adb():
    adb.set_target_device(device)


def get_ylog_version():
    stdout, timeout = adb.shell_command("getprop sys.ylog.version")
    if timeout or stdout == "":
        return
    else:
        global version
        version = stdout


class Ylog(object):
    start_cmd = "ylogctl enable 1"
    stop_cmd = "ylogctl enable 0"
    clear_cmd = "ylogctl clear"

    # def get_ylog_ctl_cmd():
    #     if is_new_ylog():
    #         return "ylogctl"
    #     else:
    #         return "ylog_cli"

    def start(self):
        stdout, _ = adb.shell_command(self.start_cmd, 60)
        logging.info(stdout)

    def stop(self):
        stdout, _ = adb.shell_command(self.stop_cmd, 60)
        logging.info(stdout)

    def clear(self):
        stdout, _ = adb.shell_command(self.clear_cmd, 60)
        logging.info(stdout)

    def is_running(self):
        stdout, _ = adb.shell_command("ylogctl query ylogdebug", 60)  # type: (str, bool)
        logging.info(stdout)
        return "open" in stdout.lower()


class YlogLegacy(Ylog):
    start_cmd = "ylog_cli ylog all start"
    stop_cmd = "ylog_cli ylog all stop"
    clear_cmd = "ylog_cli ryloga"

    def is_running(self):
        return 'running' in adb.get_prop('sys.ylog.svc.ylog_debug')


ylog = Ylog()  # type: Ylog


def start():
    ylog.start()


def stop():
    ylog.stop()


def clear():
    ylog.clear()


def is_running():
    return ylog.is_running()


init_adb()
get_ylog_version()
if is_legacy_ylog():
    ylog = YlogLegacy()
