import unittest

from src.data_model.place.place_subclasses import Location


class TestLocation(unittest.TestCase):
	def test_default_location(self):
		loc = Location()
		self.assertEqual(loc.latitude, 0.0)
		self.assertEqual(loc.longitude, 0.0)

	def test_custom_location(self):
		loc = Location(52.5200, 13.4050)
		self.assertEqual(loc.latitude, 52.5200)
		self.assertEqual(loc.longitude, 13.4050)


if __name__ == '__main__':
	unittest.main()
