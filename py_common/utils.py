import json
import logging
import sys
import shutil
import socket
import tempfile
import os
import csv
import re
import subprocess
from collections import namedtuple
from py_modules import psutil
from pyadb import ADB


def get_os():
    if sys.platform == "linux" or sys.platform == "linux2":
        return "linux"
    elif sys.platform == "win32":
        return "windows"
    else:
        return "unknown os"


'''
def sed(pattern, f):
    sed_cmd = 'sed "{pattern}" -i {file}'.format(pattern=pattern, file=f)
    print("sed: " + sed_cmd)
    os.system(sed_cmd)
'''


def sed(pattern, repl, filename):
    """
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
    """
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(repl, line))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)


# use this split instead of string's split method, because this one can handle spaces inside arugments.
def split(s):
    for row in csv.reader([s], delimiter=" "):
        return row


def port_is_avaliable(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind((ip, port))
        result = True
    except Exception:
        print("Port is in use: " + str(port))
    sock.close()
    return result


def get_avaliable_port(ip, port):
    po = port
    while not port_is_avaliable(ip, po):
        po = po + 1
    print("availabel port:" + str(po))
    return po


def exit_with_error(errmsg):
    sys.exit("ERROR: " + str(errmsg))


def kill_proc_and_sub(pid):
    print("kill proc and all it's subprocesses: {}".format(pid))
    try:
        parent_process = psutil.Process(pid)
    except Exception as ex:
        print("kill proc failed: " + ex.message)
        return

    # plist = []
    # for p in parent_process.children(recursive=True):
    #     plist.append(p)
    parent_process.suspend()

    for p in parent_process.children(recursive=True):
        try:
            print("kill sub: {}:{} ".format(p.name(), p.pid))
            p.terminate()
        except psutil.NoSuchProcess as ex:
            print("kill sub proc fail, no such process: " + str(ex.message))
        except Exception as e:
            print("kill sub: {}:{} failed".format(p.name, p.pid))
            print(e)

    print("kill parent: " + parent_process.name())
    try:
        parent_process.kill()
    except Exception:
        print("kill parent proc: {} failed".format(parent_process.name))


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


def exec_cmd(cmd, use_shell=False):
    print("exec command: " + cmd)
    cmd_list = split(cmd)
    proc = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=use_shell)

    (output, error) = proc.communicate()
    # exit_code = proc.wait()
    return output


def exec_cmd_live(cmd):
    print("exec command: " + cmd)
    cmd_list = split(cmd)
    p = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        print(str(line))
        if not line:
            if p.poll() is not None:
                break
    return ''.join(stdout)


# can't zip large file, deprecated
#
# def zip_dir(src_dir, destination):
#     base = os.path.basename(destination)
#     name = base.split('.')[0]
#     # fmt = base.split('.')[1]
#     archive_from = os.path.dirname(src_dir)
#     archive_to = os.path.basename(src_dir.strip(os.sep))
#     print(src_dir, destination, archive_from, archive_to)
#     shutil.make_archive(name, 'zip', archive_from, archive_to)
#     shutil.move('%s.%s' % (name, 'zip'), destination)


def zip_dir(src_dir, dest):
    src_dir = os.path.normpath(src_dir)
    dir_name = os.path.basename(src_dir)
    zip_file = os.path.basename(dest)

    working_dir = os.path.normpath(os.path.join(src_dir, os.pardir))
    cwd = os.getcwd()
    os.chdir(working_dir)

    cmd_list = "zip -r {} {}".format(zip_file, dir_name)
    print("pack command: " + cmd_list)
    cmd_proc = subprocess.Popen(cmd_list.split(), stdout=subprocess.PIPE)
    output = cmd_proc.communicate()[0]
    print(output)

    if cmd_proc.returncode == 0:
        print("zip pack success")
    else:
        print("zip pack fail")
    os.chdir(cwd)
    shutil.move(os.path.join(working_dir, zip_file), dest)


def is_process_exists_on_device(adb, process_name):
    """
    :rtype: bool
    :type process_name: str
    :type adb: ADB
    """
    return get_pid_on_device(adb, process_name) != 0


def get_pid_on_device(adb, process_name):
    # type: (ADB, str) -> int
    """
    get process' pid
    return pid if process exists, return 0 if process not exists, return -1 if command exec failed
    """
    _, timeout = adb.wait_for_device(10)
    if timeout:
        return -1

    result, timeout = adb.shell_command("ps | grep " + process_name, 60)  # type: (result, str)
    if timeout:
        logging.warn("exec ps command timeout")
        return -1

    result = result.strip()
    if not result:
        logging.warn("process not exists. process_name is {}, ps results: {}".format(process_name, result))
        return 0

    procs = result.split(os.linesep)
    if len(procs) > 1:
        logging.warn('more than one process have same process name({})'.format(process_name))
        return -1

    for p in procs:
        if process_name.lower() in p.lower():
            return int(p.split()[1])
    logging.warn("process not exists. process_name is {}, ps results: {}".format(process_name, result))
    return 0


def kill_proc_on_device(adb, pid):
    adb.shell_command('kill ' + str(pid))


def get_prop(adb, prop):
    cmd = "getprop " + prop
    output, retcode = adb.shell_command_timeout(cmd, 10)
    if retcode == 0:
        if output is None:
            output = ''
        else:
            output = str(output).strip()
    else:
        output = ''

    return output


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


def is_device_root(adb):
    output, retcode = adb.shell_command('whoami')
    if retcode != 0 or output is None:
        return False

    if str(output).strip() == 'root':
        return True
    return False
