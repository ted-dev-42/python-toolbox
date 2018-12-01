from __future__ import print_function
import os
import sys
import logging
import re
from py_common.timeutils import TimeUnit


class Result(object):
    STOP_REASON_KEYWORDS = [
        ("New native crash detected", "native crash happended"),
        ("Error: RemoteException", "device restart"),
        ("Error: SecurityException", "security exception occured"),
        ("Monkey aborted due to error", "java crash or anr occured"),
        ("Monkey finished", "finish normally")
    ]

    START_TIME_REGEX = r"// Monkey Start Time : (\d+)"
    SYSTEM_UPTIME_REGEX = r"system_uptime:(\d+)"
    END_TIME_REGEX = r"Monkey End Time : (\d+)"
    FIRST_NATIVE_CRASH_TIME_REGEX = r"^// First NativeCrash Time : (\d+)"
    FIRST_JAVA_CRASH_TIME_REGEX = r"^// First JavaCrash Time : (\d+)"
    FIRST_ANR_TIME_REGEX = r"^// First ANR Time : (\d+)"
    CRASH_REGEX = r"// CRASH:\s+([.0-9A-Za-z_:]*) \(pid \d+\)\s+Time Longth Since Monkey Start:\s+(\d+)"
    ANR_REGEX = r"// NOT RESPONDING:\s+([.A-Za-z0-9:]*) \(pid \d+\)\s+Time Longth Since Monkey Start:\s+(\d+)"

    NATIVE_CRASH_TAG = 'Native crash'

    def __init__(self, result_file):
        self.result_file = result_file
        self.packages_str = ''
        # self.mLogPath = ""
        # self.mMonkeyLogPath = ""
        # self.mTombstonesPath = ""
        # self.testNameString = ""

        self.elapsed_time = 0
        self.stop_reason = None
        self.start_time = 0
        self.end_time = 0

        self.system_uptime = 0
        # self.mMonkeyLastTime
        self.first_exception_time = sys.maxint
        self.first_java_crash_time = sys.maxint
        self.first_native_crash_time = sys.maxint
        self.first_anr_time = sys.maxint

        self.mANRInfo = ""
        self.mJavaCrashInfo = ""
        self.mNativeCrashInfo = ""

        self.java_crash_packages = {}
        self.native_crash_packages = {}
        self.anr_packages = {}
        self.tombstones = Result.TombStone()

        self.current_package = None
        self.next_line_is_mine = False

    def parse_monkey(self):
        if not os.path.isfile(self.result_file):
            logging.error("no result file found")
            return

        with open(self.result_file) as f:
            for line in f:
                if line.strip() == '':
                    continue
                if self.parse_start_time(line):
                    continue
                if self.parse_run_time(line):
                    continue
                if self.parse_end_time(line):
                    continue
                if self.parse_first_native_crash_time(line):
                    continue
                if self.parse_first_anr_time(line):
                    continue
                if self.parse_first_java_crash_time(line):
                    continue
                if self.parse_crash(line):
                    continue
                if self.parse_anr(line):
                    continue
                if self.parse_stop_reason(line):
                    continue

    def parse_start_time(self, line):
        m = re.search(Result.START_TIME_REGEX, line)
        if m is not None:
            self.start_time = int(m.group(1))
            logging.info('start_time: ' + str(self.start_time))
            return True
        return False

    def parse_run_time(self, line):
        m = re.search(Result.SYSTEM_UPTIME_REGEX, line)
        if m is not None:
            self.system_uptime = int(m.group(1))
            logging.info('system_uptime: ' + str(self.system_uptime))
            return True
        return False

    def parse_end_time(self, line):
        m = re.search(Result.END_TIME_REGEX, line)
        if m is not None:
            self.end_time = int(m.group(1))
            logging.info('end_time: ' + str(self.end_time))
            return True
        return False

    def parse_first_native_crash_time(self, line):
        m = re.search(Result.FIRST_NATIVE_CRASH_TIME_REGEX, line)
        if m is not None:
            self.first_native_crash_time = int(m.group(1))
            logging.info('first_native_crash_time: ' + str(self.first_native_crash_time))
            return True
        return False

    def parse_first_java_crash_time(self, line):
        m = re.search(Result.FIRST_JAVA_CRASH_TIME_REGEX, line)
        if m is not None:
            self.first_java_crash_time = int(m.group(1))
            logging.info('first_java_crash_time: ' + str(self.first_java_crash_time))
            return True
        return False

    def parse_first_anr_time(self, line):
        m = re.search(Result.FIRST_ANR_TIME_REGEX, line)
        if m is not None:
            self.first_anr_time = int(m.group(1))
            logging.info('first_anr_time: ' + str(self.first_anr_time))
            return True
        return False

    def parse_crash(self, line):
        if self.next_line_is_mine:
            if Result.NATIVE_CRASH_TAG in line:
                crash_packages = self.native_crash_packages
            else:
                crash_packages = self.java_crash_packages

            if self.current_package in crash_packages:
                crash_packages[self.current_package] += 1
            else:
                crash_packages[self.current_package] = 1
            logging.info('crash: {}({})'.format(self.current_package, crash_packages[self.current_package]))
            self.current_package = None
            self.next_line_is_mine = False
            return True
        else:
            m = re.search(Result.CRASH_REGEX, line)
            if m is None:
                return False

            # save package for next line
            self.current_package = m.group(1)
            self.next_line_is_mine = True
            logging.info('found crash, we need next line to know it is java crash or native crash')
            return True

    def parse_anr(self, line):
        m = re.search(Result.ANR_REGEX, line)
        if m is None:
            return False
        package = m.group(1)
        if package in self.anr_packages:
            self.anr_packages[package] += 1
        else:
            self.anr_packages[package] = 1
        logging.info('anr: {}({})'.format(package, self.anr_packages[package]))
        return True

    def parse_stop_reason(self, line):
        for tag, reason in Result.STOP_REASON_KEYWORDS:
            if tag in line:
                self.stop_reason = reason
                logging.info('stop reason: ' + line)
                return True
        return False

    def get_elapsed_time(self):
        if self.end_time > 0:
            elapsed_time = self.end_time - self.start_time
        else:
            elapsed_time = self.system_uptime - self.start_time
        return TimeUnit.MILLISECONDS(elapsed_time).to_hhmmss()

    def get_first_exception_time(self):
        first = min(self.first_anr_time, self.first_java_crash_time, self.first_native_crash_time)
        if first == sys.maxint:
            return 'N/A'
        else:
            return TimeUnit.MILLISECONDS(first - self.start_time).to_hhmmss()

    def get_first_anr_time(self):
        if self.first_anr_time == sys.maxint:
            return 'N/A'
        return TimeUnit.MILLISECONDS(self.first_anr_time - self.start_time).to_hhmmss()

    def get_first_java_crash_time(self):
        if self.first_java_crash_time == sys.maxint:
            return 'N/A'
        return TimeUnit.MILLISECONDS(self.first_java_crash_time - self.start_time).to_hhmmss()

    def get_first_native_crash_time(self):
        if self.first_native_crash_time == sys.maxint:
            return 'N/A'
        return TimeUnit.MILLISECONDS(self.first_native_crash_time - self.start_time).to_hhmmss()

    class TombStone(object):
        NATIVE_CRASH_REGEX = r"pid: [0-9]+, tid: [0-9]+, name: [-.0-9a-zA-Z:]+\s+>>> ([-./@0-9a-zA-Z:]*) <<<"

        def __init__(self):
            self.native_crash_packages = {}

        def parse_native_crash(self, line):
            m = re.search(Result.TombStone.NATIVE_CRASH_REGEX, line)
            if m is None:
                return False
            package = m.group(1)
            if package in self.native_crash_packages:
                self.native_crash_packages[package] += 1
            else:
                self.native_crash_packages[package] = 1
            logging.info('native crash: {}({})'.format(package, self.native_crash_packages[package]))
            return True

        def parse(self):
            if not os.path.isdir('tombstones'):
                return

            for tf in os.listdir('tombstones'):
                with open(tf) as f:
                    for line in f:
                        if line.strip() == '':
                            continue
                        if self.parse_native_crash(line):
                            break

    def parse_tombstones(self):
        # ts = Result.TombStone()
        self.tombstones.parse()
        # self.tombstones = ts

    def parse(self):
        self.parse_monkey()
        self.parse_tombstones()


monkey_result_list = []


def parse(result_file, is_parse_tombstones, packages_str):
    result = Result(result_file)
    result.parse_monkey()

    if is_parse_tombstones:
        result.parse_tombstones()
    result.packages_str = packages_str

    monkey_result_list.append(result)
    return result


def get_all_results():
    return monkey_result_list
