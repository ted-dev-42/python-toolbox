from unittest import TestCase

from py_common import mailer


class TestSend(TestCase):
    def test_send(self):
        mailer.send(to_addr="xuanchen.jiang@unisoc.com", from_addr="ctest@unisoc.com", smtp_server="smtp.unisoc.com",
                    smtp_password="1234abAB", subject="This is a test mail",
                    contents=['this is mail body', "another line", "d:\\tmp\\memtester.png"])
