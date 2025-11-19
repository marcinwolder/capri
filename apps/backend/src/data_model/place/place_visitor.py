import math
from abc import abstractmethod

from src.constants import dining, excluded_categories
from src.data_model.city.city import City
from src.data_model.place.place import Place
from src.data_model.place.place_utils import miniman_review_count
from src.data_model.places.places import Places


class Visitor:
	@staticmethod
	def place_to_itinerary(place: Place, transportation: [int, str] = None):
		"""Function that converts a place to an itinerary."""
		return {
			'name': place.placeInfo.displayName,
			'id': place.placeInfo.id,
			'types': place.types,
			'formattedAddress': place.placeInfo.formattedAddress,
			'description': place.editorialSummary.text,
			'rating': place.ratings.rating,
			'personal_rating': place.ratings.cumulative_rating,
			'googleMapsUri': place.placeInfo.googleMapsUri,
			'image': place.photos[0] if len(place.photos) > 0 else None,
			'price': place.priceLevel,
			'reviews': place.ratings.userRatingCount,
			'latitude': place.location.latitude,
			'longitude': place.location.longitude,
			'transportation': transportation,
		}

	def is_suitable(self, place, population):
		"""Function that checks if the place is suitable."""
		if not self._check_types(place):
			print('Place has wrong type', place.types)
			return False

		if place.ratings.rating is None or math.isnan(place.ratings.rating):
			print('Place has no rating: ')
			return False

		if (
			place.placeInfo.businessStatus == 'CLOSED_PERMANENTLY'
			or place.placeInfo.businessStatus == 'CLOSED_TEMPORARILY'
		):
			print('Place is closed')
			return False

		if miniman_review_count(population) > place.ratings.userRatingCount:
			print('Place has too few reviews: ', place.ratings.userRatingCount)
			return False

		if place.ratings.confidenceRating < 3.5:
			print(
				'Place has too low confidence rating: ', place.ratings.confidenceRating
			)
			return False

		return True

	def _check_types(self, place):
		"""Function that checks if the place is suitable.

		:param place: Place object
		:return: True if the place is suitable, False otherwise
		"""
		for category in excluded_categories:
			if category in place.types:
				print('wrong type', category)
				return False
			if category in place.primaryType:
				print('wrong primary type', category)
				return False
		return True

	@staticmethod
	def _save_places_to_database(
		db,
		places: Places,
		city: City,
		category_type: str,
		place_type: str,
		categories: list[str],
	):
		db.add_categories_to_database(
			city=city, category_type=category_type, categories=categories
		)
		for place in places.get_list():
			db.add_place_to_database(place, city, category_type, place_type, categories)

	@abstractmethod
	def save_places_to_database(
		self, db, places: Places, city: City, categories: list[str]
	):
		pass


class PlaceVisitor(Visitor):
	"""Class that manages a place."""

	def save_places_to_database(
		self, db, places: Places, city: City, categories: list[str]
	):
		self._save_places_to_database(
			db, places, city, 'places_categories', 'places', categories
		)


class RestaurantVisitor(Visitor):
	def is_suitable(self, place, population):
		if not self._check_types(place):
			print('Place has wrong type', place.types)
			return False
		return super().is_suitable(place, population)

	def _check_types(self, place):
		"""Function that checks if the place is suitable.
		:return: True if the place is suitable, False otherwise
		"""
		return super()._check_types(place) and any(
			d_type in place.types for d_type in dining
		)

	def save_places_to_database(
		self, db, places: Places, city: City, categories: list[str]
	):
		self._save_places_to_database(
			db, places, city, 'restaurant_categories', 'restaurants', categories
		)
