from collections import OrderedDict

from src.data_model.city.city import City
from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import Location
from src.rating.statistical_rating import StatisticalRating


class Places:
	"""A list of place with their attributes.

	Attributes:
	:param _places: OrderedDict[str, Place] - dictionary of places
	:param city: City - city where the places are located
	:param _average_rating: float - average rating of all places
	:param _average_rating_count: float - average rating count of all places

	"""

	_places: OrderedDict[str, Place]
	city: City
	_average_rating: float = -1
	_average_rating_count: float = -1

	def __init__(self, _places=None, city: City = None):
		if _places is None:
			_places = []
		self._places = OrderedDict()
		self.city = city

		self.init_with_places(_places)
		self.statisticalRating = StatisticalRating(self)

	def init_with_places(self, places_list: list[Place]):
		"""Init place list with place"""
		for atr in places_list:
			self._places[atr.placeInfo.id] = atr

	def get_location_by_id(self, place_id: str) -> Location:
		"""Returns a location of a place by its id"""
		return self._places[place_id].location

	def get_location_dict_with_id(self, place_id: str) -> dict:
		"""Returns a location of a place by its id"""
		place = self._places[place_id]
		return {
			'id': place.placeInfo.id,
			'lat': place.location.latitude,
			'lng': place.location.longitude,
		}

	def get_place_by_id(self, place_id: str) -> Place:
		"""Returns a place by its id"""
		return self._places[place_id]

	def get_list(self) -> list[Place]:
		"""Returns a list of all place"""
		return list(self._places.values())

	def create_new_places_with_id_list(self, places_ids_list):
		"""Returns a list of place from a list of place ids"""
		places_list = []
		for place_id in places_ids_list:
			places_list.append(self.get_place_by_id(place_id))
		return Places(places_list, self.city)

	def add_place(self, place: Place):
		"""Adds a place to the list"""
		self._places[place.placeInfo.id] = place

	def sort_by_rating(self):
		"""Sorts place by their ratings.
		Used for restaurants to pick the best ones.
		:return: sorted list of place
		"""
		self._places = OrderedDict(
			sorted(
				self._places.items(),
				key=lambda x: x[1].ratings.cumulative_rating,
				reverse=True,
			)
		)
		return self

	@property
	def count(self):
		"""Returns the number of places"""
		return len(self._places)

	def __len__(self):
		return self.count

	def get_by_index(self, index):
		"""Returns a place by its index"""
		return list(self._places.values())[index]

	def __getitem__(self, index):
		"""Returns a place by its index"""
		return list(self._places.values())[index]

	def remove_place(self, place: Place):
		"""Removes a place from the list"""
		self._places.pop(place.placeInfo.id)

	@property
	def places(self):
		return self._places

	def set_place(self, place: Place):
		self._places[place.placeInfo.id] = place
