from unittest import TestCase
import os
from py_common.jsonutils import JsonConvert


# @JsonConvert.register
# class MonkeyToolParms(object):
#     def __init__(self, test_mode=None, max_time=None, throttle=None):
#         """
#
#         :type packages: [Package]
#         """
#         self.test_mode = test_mode
#         self.max_time = max_time
#         self.throttle = throttle
#         # self.packages = [] if packages is None else packages
#
#     def __str__(self):
#         return str(self.test_mode) + os.linesep + str(self.max_time) + os.linesep + str(self.throttle)
#
#
# @JsonConvert.register
# class Package(object):
#     def __init__(self, name=None, type=None, throttle=None, max_time=None, event_count=None):
#         self.name = name
#         self.type = type
#         self.throttle = throttle
#         self.max_time = max_time
#         self.event_count = event_count
#         # self.Employees = [] if Employees is None else Employees
#
#     def __str__(self):
#         ret = [str(self.name), str(self.type), str(self.throttle), str(self.max_time), str(self.event_count)]
#         return os.linesep.join(ret)




class Params(object):
    class Package(object):
        name = ""
        type = ""
        throttle = ""
        max_time = ""
        event_count = ""

        def __str__(self):
            return os.linesep.join([self.name, str(self.type), str(self.throttle), str(self.max_time), str(self.event_count)])

    test_mode = ""
    max_time = ""
    throttle = ""
    packages = [Package()]

    def __str__(self):
        params_str =  os.linesep.join([self.test_mode, str(self.max_time), str(self.throttle)]) + os.linesep
        for p in self.packages:
            params_str += os.linesep + str(p) + os.linesep
        return params_str


class TestJson(TestCase):
    def test_FromFile(self):
        result = JsonConvert.FromFile('tool.cfg')
        print(result)

    def test_jsonstruct(self):
        import jsonstruct
        from py_common import fsutils
        j = fsutils.read_file('tool.cfg')
        e = jsonstruct.decode(j, Params)
        print(e.__dict__)
        print(e)
