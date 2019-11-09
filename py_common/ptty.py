import logging
import os
import select
import sys
import threading
import signal
from Queue import Queue

STDIN_FD = sys.stdin.fileno()
STDOUT_FD = sys.stdout.fileno()

# from py_modules.ptyprocess import PtyProcessUnicode

class PTY(object):
    pty_process = None  # type: PtyProcessUnicode

    def __init__(self):
        self.log = ''
        self.pty_process = None
        self.stdout = None
        self.queue = None

    def set_quit_signal(self):
        oldsignal = signal.getsignal(signal.SIGINT)
        import types
        if isinstance(oldsignal, types.BuiltinFunctionType):
            signal.signal(signal.SIGINT, self.quit)

    def spawn(self, argv, cwd=None, env=None, echo=True, preexec_fn=None, dimensions=(24, 80), stdout=sys.stdout, queue=None):
        # type: (str, str, str, bool, callable, tuple, object, Queue) -> None
        self.set_quit_signal()
        self.pty_process = PtyProcessUnicode.spawn(argv, cwd, env, echo, preexec_fn, dimensions)
        t = threading.Thread(target=self._copy)
        t.setDaemon(True)
        t.start()
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout
        self.queue = queue

    def quit(self, *args, **kwargs):
        sys.exit(1)  # must exit with something not '0'

    def write_log(self, b):
        assert isinstance(b, str), 'log only str'
        self.log += b

    def _copy(self):
        assert isinstance(self.pty_process, PtyProcessUnicode)
        with os.fdopen(self.pty_process.fd) as f:
            while True:
                try:
                    line = f.readline()
                except IOError:
                    break

                if line == '':
                    break

                if self.queue is not None:
                    self.queue.put(line)
                else:
                    self.stdout.write(line)
        print('copy thread exit')

    def _has_user_input(self):
        assert isinstance(self.pty_process, PtyProcessUnicode)
        data = self._read_stdin(1024)
        if not data:
            return False
        self.pty_process.write(data)
        return True

    def write_stdin(self, data):
        self.pty_process.write(data)

    def _read_stdin(self, bufsize):
        return os.read(STDIN_FD, bufsize)


from Queue import Queue, Empty
def exec_cmd_linux(cmd, cwd=None):
    queue = Queue()
    pty = PTY()
    pty.spawn(cmd, cwd=cwd, echo=False, queue=queue)
    while True:
        line = ""
        try:
            line = queue.get(timeout=2)
            print(line)
        except Empty:
            if not pty.pty_process.isalive():
                logging.warning('process not alive, exit')
                break
    return pty.pty_process.exitstatus


def exec_cmd_windows(cmd, cwd=None):
    from py_modules.winpty import PtyProcess
    proc = PtyProcess.spawn(cmd, cwd=cwd)
    while proc.isalive():
        print(proc.readline())
