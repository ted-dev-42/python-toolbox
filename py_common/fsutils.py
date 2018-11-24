import os
import shutil
import errno
import logging
from py_modules.pathlib2 import Path


def is_dir_empty(dirname):
    if not os.listdir(dirname):
        return True
    else:
        return False


def remove_file(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
    print("delete file {} success".format(filename))


def remove_dir(dirname):
    try:
        shutil.rmtree(dirname)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
    print("delete dir {} success".format(dirname))


def remove(fname):
    if os.path.isfile(fname):
        remove_file(fname)
    else:
        remove_dir(fname)


def copy_dir(src, dest):
    # type: (Path, Path) -> None
    if not dest.exists():
        dest.mkdir(parents=True, exist_ok=True)

    # distutils is better than shutil.copy_tree
    from distutils.dir_util import copy_tree
    copy_tree(str(src), str(dest))


def copy_file(src, dest):
    # type: (Path, Path) -> None
    """
    :param src: src file
    :param dest: dest file or dest dir(dir must be existing)
    """
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(str(src), str(dest))


def copy(src, dest):
    # type: (Path, Path) -> None
    if not src.exists():
        logging.error('src not exists')
    if src.is_file():
        copy_file(src, dest)
    else:
        copy_dir(src, dest)
