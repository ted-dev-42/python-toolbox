from unittest import TestCase

import lib_installer_legacy as installer
import fsutils
import pkginfo
from pathlib2 import Path


class TestInstaller(TestCase):
    def test_init(self):
        installer.init("../py_common/libs")

    def test_get_all_lib_info(self):
        all_files = fsutils.get_all_files(Path("../py_common/libs"))
        for f in all_files:
            lib = installer.get_lib_info(str(f))  # type: (object, pkginfo)
            if lib is not None:
                print(lib.name)
                print(lib.requires)

    def test_get_all_pkg_info(self):
        all_files = fsutils.get_all_files(Path("../py_common/libs"))
        for f in all_files:
            pkg = installer.get_pkg_info(str(f))  # type: (object, pkginfo)
            if pkg is not None:
                print(pkg.name)
                print(pkg.requires)
                print(pkg.requires_dist)


    def test_get_pkg(self):
        installer.get_pkg_info("../py_common/libs/Mako-1.0.10.tar.gz")

    def test_install_by_path(self):
        installer.install_lib("../py_common/libs/MarkupSafe-1.1.1-cp27-cp27m-any_amd64.whl")

    def test_install_zip(self):
        installer.install_lib("../py_common/libs/jsonstruct-0.2a1.zip")

    def test_install_by_name(self):
        installer.init("../py_common/libs")
        installer.install("Mako")

    def test_install_nonexistent(self):
        installer.install("nonexistent")
