from unittest import TestCase
import build

class TestBuild(TestCase):
    def test_get_config_file_dir_name(self):
        build.get_config_file_dir_name('../../monkey/build.json')
