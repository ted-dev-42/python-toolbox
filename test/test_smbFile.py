from unittest import TestCase


class TestSmbFile(TestCase):
    def test_get(self):
        from smbutils import SmbFile
        smbf = SmbFile('smb://SPREADTRUM.COM;public:Sprd1234@shnas02/TestData/TestLogs/SZTest/subplan/sharkl3.xml')
        smbf.get('test.xml')
