import logging

import utils
import fsutils
from pathlib2 import Path
from pkginfo import Distribution

all_libs = []  # type: [Lib]
installed_libs = []  # type: [Lib]


class Lib(object):
    def __init__(self):
        self.name = ""
        self.requires = []
        self.path = None


def _install(lib_file, dest):
    cmd = 'install --target={} {}'.format(dest, lib_file)
    print(cmd)
    from pip._internal import main as pip_main
    pip_main(utils.split(cmd))


def install_lib(lib_file, dest="py_common/py_modules"):
    """
        install lib
        must exec install in a separated process because we can't invoke pip_main multiple times in the same process
    """
    import multiprocessing
    p = multiprocessing.Process(target=_install, args=(lib_file, dest))
    p.start()
    p.join()


# noinspection PyUnresolvedReferences
def get_lib_by_name(lib_name):
    # type: (str) -> Optional[Lib]
    for l in all_libs:
        if l.name == lib_name:
            return l
    return None


def install(lib_name, dest="py_common/py_modules"):
    if len(all_libs) == 0:
        init()
    logging.info("install lib: {} to {} ".format(lib_name, dest))
    if lib_name in installed_libs:
        logging.info("{} has been installed".format(lib_name))
        return

    lib = get_lib_by_name(lib_name)
    if lib is None:
        raise Exception("lib not found: " + lib_name)
    if len(lib.requires) > 0:
        for r in lib.requires:
            install(r, dest)
    install_lib(str(lib.path), dest)
    installed_libs.append(lib_name)


# noinspection PyUnresolvedReferences
def get_lib_info(lib_path):
    # type: (str) -> (Optional[Lib])
    pkg = get_pkg_info(lib_path)
    if pkg is None:
        return None
    lib = Lib()
    lib.name = pkg.name.strip()
    for require in pkg.requires_dist:
        lib.requires.append(require.split(';')[0].strip())
    return lib


def get_pkg_info(lib_path):
    # type: (str) -> Distribution
    from pkginfo import Wheel, SDist
    if lib_path.endswith("whl"):
        pkg = Wheel(lib_path)
    elif lib_path.endswith("zip") or lib_path.endswith("tar.gz"):
        pkg = SDist(lib_path)
    else:
        return None
    return pkg


def init(libs_dir="libs"):
    logging.info("init libs: " + libs_dir)
    libs_path = Path(libs_dir)
    if not libs_path.is_dir():
        raise Exception("libs dir not exists, " + libs_dir)

    all_files = fsutils.get_all_files(Path(libs_dir))
    for f in all_files:
        lib = get_lib_info(str(f))
        lib.path = f
        all_libs.append(lib)
        print("found a lib, name: {}, requires: {}, path: {}".format(lib.name, lib.requires, lib.path))
