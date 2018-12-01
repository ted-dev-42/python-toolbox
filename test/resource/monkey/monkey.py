from __future__ import print_function
import os
import sys
import logging
import time

import result
import report
from params import Params

import utils
import fsutils
from timeutils import TimeUnit
from pyadb import ADB
#from py_common import utils
#from py_common import fsutils
#from py_common.timeutils import TimeUnit
#from py_common.py_modules.pyadb import ADB

__maintainer__ = "Xuanchen.Jiang"
__email__ = "xuanchen.jiang@spreadtrum.com"


adb = None  # type: ADB
def_cmd_params = '--ignore-crashes --ignore-native-crashes --ignore-timeouts --ignore-security-exceptions --kill-process-after-error -v -v -v'
params = None  # type: Params

RESULT_FILE = '/data/local/tmp/monkey'
LOCAL_RESULT_FILE = './results/monkey'
PACKAGE_FILE = 'monkey_packages'
DEVICE_PACKAGE_FILE = '/data/local/tmp/' + PACKAGE_FILE
LAUNCHER = 'monkey-launcher'
MAX_COUNT = 10000000
MONKEY_PROC_NAME = "com.android.commands.monkey"


def init():
    init_log()
    init_env()
    init_adb()
    clear_result()
    clear_device()
    init_device()
    init_ylog()


def init_env():
    if os.path.isdir('results'):
        return
    os.mkdir('results')


def init_log():
    logging.basicConfig(level=logging.DEBUG,
                        format='[MONKEY]%(asctime)s [%(levelname)s] %(message)s (%(filename)s[%(lineno)d])',
                        datefmt='%m-%d %H:%M:%S')


def init_adb():
    device_id = os.getenv("ANDROID_SERIAL")
    global adb
    adb = ADB()
    adb.enable_debug()
    adb.set_adb_path()
    adb.set_target_device(device_id)
    # adb.set_adb_root()


def init_device():
    _, timeout = adb.wait_for_device(120)
    if timeout:
        sys.exit("device not found")

    adb.shell_command('settings put secure user_setup_complete 1')
    adb.shell_command('settings put global device_provisioned 1')
    adb.shell_command('pm clear com.google.android.setupwizard')
    adb.shell_command('settings put system screen_off_timeout 1800000')
    adb.shell_command('settings put global stay_on_while_plugged_in 3')
    adb.push_local_file('nolock.jar', '/data/local/tmp/')
    adb.shell_command('uiautomator runtest nolock.jar')
    adb.push_local_file(LAUNCHER, '/data/local/tmp/')
    adb.shell_command('chmod 777 /data/local/tmp/{}'.format(LAUNCHER))


def clear_device():
    adb.shell_command('rm -f {}'.format(DEVICE_PACKAGE_FILE))
    # adb.shell_command('rm -rf {}'.format('/data/tombstones'))
    # utils.remove('./data/tombstones')


def clear_result():
    adb.shell_command('rm -f {}*'.format(RESULT_FILE))


def init_ylog():
    adb.shell_command('ylog_cli ylog all start')
    adb.shell_command('ylog_cli ryloga')


def start():
    save_package()
    if params.test_mode == 'package':
        for pkg in params.packages:
            launcher_monkey(pkg)
            reason = wait_monkey_finish_or_timeout(pkg)
            kill_monkey()
            process_result(reason, pkg)
            clear_device()
    else:
        launcher_monkey()
        reason = wait_monkey_finish_or_timeout()
        kill_monkey()
        process_result(reason)
        clear_device()


def get_params(pkg=None):
    return "-s {seed} --throttle {throttle} {package} {param} {count}" \
        .format(seed=get_seed(),
                throttle=get_throttle(),
                package=get_package(pkg),
                param=def_cmd_params,
                count=get_count(pkg))


def get_throttle(pkg=None):
    if pkg is not None:
        return pkg.throttle
    return params.throttle


def get_count(pkg=None):
    if pkg is not None:
        if pkg.type == "event":
            return pkg.event_count
    return MAX_COUNT


def get_package(pkg=None):
    if pkg is not None:
        return '-p ' + pkg.name

    if params.test_mode == 'white':
        return '--pkg-whitelist-file ' + DEVICE_PACKAGE_FILE

    if params.test_mode == 'black':
        return '--pkg-blacklist-file ' + DEVICE_PACKAGE_FILE


def get_seed():
    import random
    return random.randint(100, 100000)


def save_package():
    if params.test_mode == "package":
        return

    packages = params.packages
    fsutils.remove(PACKAGE_FILE)

    with open(PACKAGE_FILE, 'w') as f:
        for p in packages:
            print(p.name, file=f)

    rst = adb.push_local_file(PACKAGE_FILE, DEVICE_PACKAGE_FILE)
    logging.info(rst)


def get_max_time(pkg=None):
    if pkg is not None:
        if pkg.type == "timespan":
            return pkg.max_time
        else:
            return sys.maxint
    else:
        return 0


def get_packages_str(pkg=None):
    if pkg is None:
        pkg_list = []
        for p in params.packages:
            pkg_list.append(p.name)
        return ', '.join(pkg_list)
    else:
        return pkg.name


def get_monkey_result(pkg=None):
    if pkg is None:
        local_result_file = LOCAL_RESULT_FILE
    else:
        local_result_file = LOCAL_RESULT_FILE + "_" + pkg.name
    adb.get_remote_file(RESULT_FILE, local_result_file)
    if not os.path.isfile(local_result_file):
        logging.error("no monkey result file on device, " + local_result_file)
        return None
    return local_result_file


def get_tombstones():
    adb.get_remote_file('/data/tombstones', '')


def wait_monkey_finish_or_timeout(pkg=None):
    logging.info('wait monkey finish or timeout')
    max_time = get_max_time(pkg)
    if max_time == 0:
        max_time = params.max_time
    logging.info("wait max time: " + str(max_time))

    system_process_id = utils.get_pid_on_device(adb, 'system_server')
    if system_process_id == 0:
        logging.error('get system process id error')
        return RunningEndResult.UNKNOWN

    start_time = int(time.time())
    minute_time = start_time
    while True:
        time.sleep(5)

        elapsed_time = int(time.time() - start_time)
        minute_secs = int(time.time() - minute_time)
        if minute_secs > 60:
            logging.info('monkey has been running for ' + TimeUnit.SECONDS(elapsed_time).to_hhmmss())
            minute_time = int(time.time())

        # when device is offline, we will still wait regardless max time
        state = adb.get_state().strip()
        if state != 'device':
            continue

        if elapsed_time > max_time:
            logging.info("max time reached")
            return RunningEndResult.TIMEOUT

        if utils.is_process_exists_on_device(adb, MONKEY_PROC_NAME):
            continue
        else:
            logging.error("detect monkey process has teminated")
            sysid = utils.get_pid_on_device(adb, 'system_server')
            if sysid == 0:
                continue
            if sysid != system_process_id:
                logging.error("detect phone has reboot")
                return RunningEndResult.DEVICE_REBOOT
            else:
                if pkg is not None:
                    if pkg.type == 'event':
                        return RunningEndResult.EVENT_FINISH
            break

    return RunningEndResult.UNKNOWN


def launcher_monkey(pkg=None):
    cmd = "/data/local/tmp/{lc} {log} {params}".format(lc=LAUNCHER, log=RESULT_FILE, params=get_params(pkg))
    logging.info("command: " + cmd)

    adb.shell_command(cmd)

    logging.info("command exec over, sleep a while")
    time.sleep(5)

    if utils.is_process_exists_on_device(adb, MONKEY_PROC_NAME):
        logging.info('monkey start success')
    else:
        logging.info('monkey start failed')
        adb.shell_command('cat ' + RESULT_FILE)


def kill_monkey():
    pid = utils.get_pid_on_device(adb, MONKEY_PROC_NAME)
    if pid != 0:
        utils.kill_proc_on_device(adb, pid)
        logging.info('kill monkey process: ' + str(pid))
    else:
        logging.warning('monkey process not exists')


def process_result(reason, pkg=None):
    is_parse_tombstones = False
    local_result_file = get_monkey_result(pkg)
    if local_result_file is None:
        return

    # if utils.is_device_root(adb):
    #     get_tombstones()
    #     is_parse_tombstones = True

    r = result.parse(local_result_file, is_parse_tombstones, get_packages_str(pkg))
    if r.stop_reason is None:
        r.stop_reason = reason


def make_report():
    report_info = {}
    report_info['result_list'] = result.get_all_results()
    report_info['test_mode'] = params.test_mode
    report.make(report_info)


def run():
    init()
    start()
    make_report()


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-m',
#                         dest='test_mode',
#                         default=None,
#                         help='test mode: w(hite), b(lack), or p(ackages)')
#
#     parser.add_argument('-t',
#                         dest='throttle',
#                         default=500,
#                         help='throttle, milisec')
#
#     parser.add_argument('--help', action='store_true',
#                         help='help')
#
#     parser.add_argument('--version', action='version',
#                         version=__version__)
#
#     return parser.parse_args()


def load_params():
    if not os.path.exists('tool.cfg'):
        utils.exit_with_error("tool.cfg not found")
    global params
    params = Params.load(fsutils.read_file('tool.cfg'))
    print(params)


class RunningEndResult(object):
    TIMEOUT = 'time out'
    EVENT_FINISH = 'events drain'
    DEVICE_REBOOT = 'device reboot'
    UNKNOWN = 'unknown'


def main():
    load_params()
    run()


if __name__ == "__main__":
    os.chdir(os.path.normpath(os.path.dirname(sys.argv[0])))
    main()
