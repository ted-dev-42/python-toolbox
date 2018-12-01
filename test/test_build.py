from unittest import TestCase
import py_common.build

class TestBuild(TestCase):
    def test_get_config_file_dir_name(self):
        py_common.build.get_config_file_dir_name('../../monkey/build.json')
