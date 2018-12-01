import os
import shutil
import errno
import logging
import types

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


def copy_to_dir(src, dest):
    # type: (Path, Path) -> None
    if not dest.exists():
        dest.mkdir(parents=True, exist_ok=True)

    if src.is_file():
        copy_file(src, dest.joinpath(src.name))
    else:
        # distutils is better than shutil.copy_tree
        from distutils.dir_util import copy_tree
        copy_tree(str(src), str(dest))


def copy_file(src, dest):
    # type: (Path, Path) -> None
    """
    :param src: src file
    :param dest: dest file
    """
    if not src.is_file():
        logging.error('src is not file:' + str(src))
        return

    if dest.exists() and dest.is_dir():
        logging.error('dest is dir:' + str(dest))
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(str(src), str(dest))


def copy(src, dest, ignore=None):
    # type: (Path, Path, str) -> None
    if not src.exists():
        logging.error('src not exists, ' + str(src))

    file_list = get_all_files(src, ignore)

    for src_file in file_list:
        relative_path = src_file.relative_to(src)
        copy_file(src_file, dest.joinpath(relative_path))


def ignore_process(ignore_pattern):
    # type: (str) -> types.FunctionType

    def _none_ignore(_path):
        return False

    from fnmatch import fnmatch
    ignore_names = ignore_pattern.split(',') if ignore_pattern is not None else ""

    def _ignore(path):
        for ignore in ignore_names:
            if fnmatch(str(path), ignore.strip()):
                return True
        return False

    if ignore_pattern is None:
        return _none_ignore
    else:
        return _ignore


def get_all_files_dirs(path_obj, ignore_pattern=None):
    # type: (Path, str) -> (list, list)
    flist = []
    dlist = []
    ignore_list = []
    ignore = ignore_process(ignore_pattern)
    if path_obj.is_file():
        if not ignore(path_obj):
            flist.append(path_obj)
    else:
        for r, dl, fl in os.walk(str(path_obj)):
            if Path(r) in ignore_list:
                for d in dl:
                    ignore_list.append(Path(r).joinpath(d))
                continue
            for d in dl:
                _d = Path(r).joinpath(d)
                if ignore(d):
                    ignore_list.append(_d)
                else:
                    print(r)
                    print(dl)
                    print(fl)
                    dlist.append(_d)
            for f in fl:
                if not ignore(f):
                    flist.append(Path(r).joinpath(f))

    return flist, dlist


def get_all_files(path_obj, ignore_pattern=None):
    f, _ = get_all_files_dirs(path_obj, ignore_pattern)
    return f


def get_all_dirs(path_obj, ignore_pattern=None):
    _, d = get_all_files_dirs(path_obj, ignore_pattern)
    return d


def read_file(file_name):
    with open(file_name) as f:
        return f.read()
