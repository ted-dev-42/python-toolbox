# import datetime


class TimeUnit(object):
    MILLISECONDS_UNIT = 0
    SECONDS_UNIT = 1
    MINUTES_UNIT = 2
    HOURS_UNIT = 3

    @staticmethod
    def MILLISECONDS(millis):
        return TimeUnit(millis, TimeUnit.MILLISECONDS_UNIT)

    @staticmethod
    def SECONDS(secs):
        return TimeUnit(secs, TimeUnit.SECONDS_UNIT)

    @staticmethod
    def MINUTES(minutes):
        return TimeUnit(minutes, TimeUnit.MINUTES_UNIT)

    @staticmethod
    def HOURS(hours):
        return TimeUnit(hours, TimeUnit.HOURS_UNIT)

    def __init__(self, time, unit):
        self.time = time
        self.unit = unit
        # use millisecs to store all types of time
        self.millisecs = self.convert_to_milisecs(self.time, self.unit)

    def convert_to_milisecs(self, time, unit):
        if unit == TimeUnit.MILLISECONDS_UNIT:
            return time
        elif self.unit == TimeUnit.SECONDS_UNIT:
            return time*1000
        elif self.unit == TimeUnit.MINUTES_UNIT:
            return (time*1000)*60
        elif self.unit == TimeUnit.HOURS_UNIT:
            return (time*1000)*60*60
        else:
            raise RuntimeError("wrong unit")

    def to_hhmmss(self):
        m, s = divmod(self.millisecs/1000, 60)
        h, m = divmod(m, 60)
        return "{0:d}:{1:02d}:{2:02d}".format(h, m, s)

    def to_milliseconds(self):
        return self.millisecs

    def to_seconds(self):
        return self.millisecs/1000

    def to_minutes(self):
        return self.millisecs/(1000*60)

    def to_hours(self):
        return self.millisecs/(1000*60*60)


# class TimeUnitMilliseconds(TimeUnit):
#     def __init__(self, time):
#         self.time = time
#         self.unit = TimeUnit.MILLISECONDS_UNIT
#
#
# class TimeUnitSeconds(TimeUnit):
#     def __init__(self, time):
#         self.time = time
#         self.unit = TimeUnit.SECONDS_UNIT
