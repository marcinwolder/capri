import unittest
from unittest.mock import patch

from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import PlaceInfo
from src.data_model.places.places import Places


class TestPlaces(unittest.TestCase):
	"""Test class for Places."""

	def setUp(self):
		self.places = self.make_places()

	def tearDown(self):
		pass

	def make_places(self):
		places = []
		for i in range(5):
			place = Place(
				placeInfo=PlaceInfo(id=f'place{i}', displayName=f'place{i}'),
				estimatedTime=60,
			)
			places.append(place)
		return Places(places)

	def test_get_time(self):
		"""(480, {'place1': 60, 'place2': 180, 'place3': 300, 'place4': 420})"""
		with patch(
			'src.travel_time.travel_time.TravelEstimator.get_estimated_time'
		) as mock_get_estimated_time:
			mock_get_estimated_time.return_value = 60
			places = self.places
			time, arrival_times = places.get_time()

			assert time == 480
			assert arrival_times == {
				'place1': 60,
				'place2': 180,
				'place3': 300,
				'place4': 420,
			}

	def test_get_place_by_id(self):
		places = self.places
		place = places.get_place_by_id('place1')
		assert place.placeInfo.id == 'place1'
		assert place.estimatedTime == 60

	def test_set_place(self):
		pass

	def test_get_by_index(self):
		pass

	def test_get_list(self):
		pass
