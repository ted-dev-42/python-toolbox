import os
from unittest import TestCase

import fsutils
from pathlib2 import Path


class TestFsutils(TestCase):
    def test_copy(self):
        path = Path('resource/monkey')
        flist = path.glob("*")
        for f in flist:  # type: Path
            if f.is_file():
                continue
            else:
                print('dir')

    def test_wark(self):
        for r,d,f in os.walk('resource/monkey'):
            print(r)
            print(d)
            print(f)
            print(os.linesep)
            print(os.linesep)

    def test_get_all(self):
        path = Path('resource/monkey').resolve()
        f , d = fsutils.get_all_files_dirs(path, '*.pyc, mako')
        print(f)
        print(d)

    def test_remove_dir(self):
        fsutils.remove_dir("aaaa")
