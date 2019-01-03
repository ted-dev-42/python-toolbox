from unittest import TestCase

from timeutils import TimeUnit


class TestTime(TestCase):
    def test_milisecs(self):
        tu = TimeUnit(3650365, TimeUnit.MILLISECONDS_UNIT)
        print(tu.to_milliseconds())
        print(tu.to_seconds())
        print(tu.to_minutes())
        print(tu.to_hours())
        print(tu.to_hhmmss())

    def test_seconds(self):
        tu = TimeUnit(3650, TimeUnit.SECONDS_UNIT)
        print(tu.to_milliseconds())
        print(tu.to_seconds())
        print(tu.to_minutes())
        print(tu.to_hours())
        print(tu.to_hhmmss())

    def test_minutes(self):
        tu = TimeUnit(1650, TimeUnit.MINUTES_UNIT)
        print(tu.to_milliseconds())
        print(tu.to_seconds())
        print(tu.to_minutes())
        print(tu.to_hours())
        print(tu.to_hhmmss())

    def test_hours(self):
        tu = TimeUnit(48, TimeUnit.HOURS_UNIT)
        print(tu.to_milliseconds())
        print(tu.to_seconds())
        print(tu.to_minutes())
        print(tu.to_hours())
        print(tu.to_hhmmss())
