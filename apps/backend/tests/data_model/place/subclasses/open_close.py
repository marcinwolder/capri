import unittest

from src.data_model.place.place_subclasses import TimePoint, RegularOpeningHours, Period


class TestTimePoint(unittest.TestCase):
    def test_default_instantiation(self):
        tp = TimePoint()
        self.assertEqual(tp.hour, 0)
        self.assertEqual(tp.minute, 0)
        self.assertEqual(tp.sum_minutes, 0)

    def test_custom_instantiation(self):
        tp = TimePoint(hour=1, minute=30)
        self.assertEqual(tp.hour, 1)
        self.assertEqual(tp.minute, 30)
        self.assertEqual(tp.sum_minutes, 90)

class TestRegularOpeningHours(unittest.TestCase):
    def test_default_instantiation(self):
        roh = RegularOpeningHours()
        self.assertEqual(len(roh.periods), 7)
        for period in roh.periods:
            self.assertIsInstance(period, Period)
            self.assertEqual(period.open.sum_minutes, 0)
            self.assertEqual(period.close.sum_minutes, 1440)  

    def test_one_day_instantiation(self):
        periods_input = [
            {'open': {'day': 1, 'hour': 8, 'minute': 0}, 'close': {'day': 1, 'hour': 17, 'minute': 0}},
        ]
        roh = RegularOpeningHours(periods=periods_input)

        for i, period in enumerate(roh.periods):
            if i == 1:
                self.assertEqual(period.open.hour, 8)
                self.assertEqual(period.close.hour, 17)
                self.assertEqual(period.open_in_minutes, 480)  
                self.assertEqual(period.close_in_minutes, 1020)  
            else:
                self.assertEqual(period.open.hour, 0)
                self.assertEqual(period.close.minute, 0)
                self.assertEqual(period.open.sum_minutes, 0)
                self.assertEqual(period.close.sum_minutes, 0)

        periods_input = [
            {'open': {'day': 0, 'hour': 8, 'minute': 0}, 'close': {'day': 0, 'hour': 17, 'minute': 0}},
        ]
        roh = RegularOpeningHours(periods=periods_input)

        for i, period in enumerate(roh.periods):
            if i == 0:
                self.assertEqual(period.open.hour, 8)
                self.assertEqual(period.close.hour, 17)
                self.assertEqual(period.open_in_minutes, 480)
                self.assertEqual(period.close_in_minutes, 1020)
            else:
                self.assertEqual(period.open.hour, 0)
                self.assertEqual(period.close.minute, 0)
                self.assertEqual(period.open.sum_minutes, 0)
                self.assertEqual(period.close.sum_minutes, 0)



    def test_all_days_instantiation(self):
        periods_input = [
            {'open': {'day': 0, 'hour': 8, 'minute': 0}, 'close': {'day': 0, 'hour': 17, 'minute': 0}},
            {'open': {'day': 1, 'hour': 9, 'minute': 0}, 'close': {'day': 1, 'hour': 18, 'minute': 0}},
            {'open': {'day': 2, 'hour': 10, 'minute': 0}, 'close': {'day': 2, 'hour': 19, 'minute': 0}},
            {'open': {'day': 3, 'hour': 11, 'minute': 0}, 'close': {'day': 3, 'hour': 20, 'minute': 0}},
            {'open': {'day': 4, 'hour': 12, 'minute': 0}, 'close': {'day': 4, 'hour': 21, 'minute': 0}},
            {'open': {'day': 5, 'hour': 13, 'minute': 0}, 'close': {'day': 5, 'hour': 22, 'minute': 0}},
            {'open': {'day': 6, 'hour': 14, 'minute': 0}, 'close': {'day': 6, 'hour': 23, 'minute': 0}},
        ]
        roh = RegularOpeningHours(periods=periods_input)

        for i, period in enumerate(roh.periods):
            self.assertEqual(period.open.hour, i + 8)
            self.assertEqual(period.close.hour, i + 17)
            self.assertEqual(period.open_in_minutes, (i + 8) * 60)
            self.assertEqual(period.close_in_minutes, (i + 17) * 60)

    def test_open_24_hours(self):
        periods_input = [
            {'open': {'day': 0, 'hour': 0, 'minute': 0}, 'close': {'day': 0, 'hour': 0, 'minute': 0}},
        ]
        roh = RegularOpeningHours(periods=periods_input)

        for i, period in enumerate(roh.periods):
            self.assertEqual(period.open.hour, 0)
            self.assertEqual(period.close.hour, 24)
            self.assertEqual(period.open_in_minutes, 0)
            self.assertEqual(period.close_in_minutes, 1440)

    def test_close_after_midnight(self):
        periods_input = [
            {'open': {'day': 0, 'hour': 23, 'minute': 0}, 'close': {'day': 1, 'hour': 1, 'minute': 0}},
        ]
        roh = RegularOpeningHours(periods=periods_input)

        for i, period in enumerate(roh.periods):
            if i == 0:
                self.assertEqual(period.open.hour, 23)
                self.assertEqual(period.close.hour, 24+1)
                self.assertEqual(period.open_in_minutes, 1380)



if __name__ == '__main__':
    unittest.main()