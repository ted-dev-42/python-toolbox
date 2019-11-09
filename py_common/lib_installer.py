import logging

import utils
import fsutils
from pathlib2 import Path
from pkginfo import Distribution

libs_dir = ""
dest_dir = ""


def _install(lib_name, dest, src):
    cmd = 'install --target={} --no-index --find-link={} {}'.format(dest, src, lib_name)
    print(cmd)
    from pip._internal import main as pip_main
    pip_main(utils.split(cmd))


def install_lib(lib_name, dest=None, src=None):
    """
        install lib
        must exec install in a separated process because we can't invoke pip_main multiple times in the same process
    """
    if dest is None:
        dest = dest_dir
    if src is None:
        src = libs_dir
    import multiprocessing
    p = multiprocessing.Process(target=_install, args=(lib_name, dest, src))
    p.start()
    p.join()


def init(libs="libs", dest="py_common/py_modules"):
    logging.info("init libs: " + libs)
    if not Path(libs).is_dir():
        raise Exception("libs dir not exists, " + libs)
    global libs_dir
    global dest_dir
    libs_dir = libs
    dest_dir = dest

