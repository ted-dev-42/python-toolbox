from unittest import TestCase

import lib_installer as installer

class TestInstall(TestCase):
    def test_install_lib(self):
       installer.install_lib("pathlib2", "install_target", "../py_common/libs")
