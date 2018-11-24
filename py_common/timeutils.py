import datetime

class TimeUnit(object):
    MILLISECONDS_UNIT = 0
    SECONDS_UNIT = 1
    MINITES_UNIT = 2
    HOURS_UNIT = 3

    @staticmethod
    def SECONDS(secs):
        return TimeUnit(secs, TimeUnit.SECONDS_UNIT)

    @staticmethod
    def MILLISECONDS(millis):
        return TimeUnit(millis, TimeUnit.MILLISECONDS_UNIT)

    @staticmethod
    def MINUTES(minutes):
        return TimeUnit(minutes, TimeUnit.MINITES_UNIT)

    def __init__(self, time, unit):
        self.time = time
        self.unit = unit
        self.secs = self.convert_to_secs(self.time, self.unit)

    def convert_to_secs(self, time, unit):
        if unit == TimeUnit.MILLISECONDS_UNIT:
            return time/1000
        elif self.unit == TimeUnit.SECONDS_UNIT:
            return time
        elif self.unit == TimeUnit.MINITES_UNIT:
            return time*60
        else:
            raise RuntimeError("wrong unit")

    def to_hhmmss(self):
        return str(datetime.timedelta(seconds=self.secs))


class TimeUnitSeconds(TimeUnit):
    def __init__(self, time):
        self.time = time
        self.unit = TimeUnit.SECONDS_UNIT


class TimeUnitMilliseconds(TimeUnit):
    def __init__(self, time):
        self.time = time
        self.unit = TimeUnit.MILLISECONDS_UNIT

