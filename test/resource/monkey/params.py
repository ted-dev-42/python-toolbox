import os
import jsonstruct


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

    @staticmethod
    def load(j):
        return jsonstruct.decode(j, Params)

