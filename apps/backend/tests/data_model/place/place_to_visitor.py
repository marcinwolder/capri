import unittest

from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import (
	Location,
	PlaceInfo,
	PlaceRating,
	TextWithLang,
)
from src.data_model.place.place_visitor import PlaceVisitor


class TestPlaceToItinerary(unittest.TestCase):
	def setUp(self):
		self.place = Place(
			placeInfo=PlaceInfo(
				name='Example Place',
				id='123',
				formattedAddress='123 Example Street',
				googleMapsUri='http://example.com',
				websiteUri='http://example.com',
				iconMaskBaseUri='http://example.com',
				displayName='Example Place',
				businessStatus='OPERATIONAL',
			),
			types=['restaurant'],
			location=Location(latitude=0.0, longitude=0.0),
			regularOpeningHours=None,
			primaryType='restaurant',
			primaryTypeDisplayName={},
			editorialSummary=TextWithLang(),
			accessibilityOptions=None,
			reviews=[],
			photos=[],
			priceLevel=None,
			ratings=PlaceRating(rating=4.0, userRatingCount=100),
		)
		self.population = 100
		self.visitor = PlaceVisitor()

	def test_place_to_itinerary(self):
		itinerary = PlaceVisitor.place_to_itinerary(self.place)
		self.assertIsInstance(itinerary, dict)
		self.assertEqual(itinerary['name'], self.place.placeInfo.displayName)
		self.assertEqual(itinerary['id'], self.place.placeInfo.id)
		self.assertEqual(itinerary['types'], self.place.types)
		self.assertEqual(
			itinerary['formattedAddress'], self.place.placeInfo.formattedAddress
		)
		self.assertEqual(itinerary['description'], self.place.editorialSummary.text)
		self.assertEqual(itinerary['location'], self.place.location)
		self.assertEqual(itinerary['rating'], self.place.ratings.rating)
		self.assertEqual(itinerary['googleMapsUri'], self.place.placeInfo.googleMapsUri)
		self.assertEqual(
			itinerary['image'],
			self.place.photos[0] if len(self.place.photos) > 0 else None,
		)
		self.assertEqual(itinerary['price'], self.place.priceLevel)
		self.assertEqual(itinerary['reviews'], self.place.ratings.userRatingCount)
		self.assertEqual(itinerary['latitude'], self.place.location.latitude)
		self.assertEqual(itinerary['longitude'], self.place.location.longitude)

	def test_is_suitable_ratings_lower_than_3_5(self):
		ratings = [None, 0.0, 1.0, 1.5, 2.0, 3.0]
		for rating in ratings:
			self.place.ratings.rating = rating
			self.assertFalse(self.visitor.is_suitable(self.place, self.population))

	def test_is_suitable_ratings_higher_than_3_5(self):
		ratings = [3.5, 3.6, 4.0, 4.5, 5.0]
		for rating in ratings:
			self.place.ratings.rating = rating
			self.assertTrue(self.visitor.is_suitable(self.place, self.population))

	def test_is_suitable_mixed(self):
		self.assertTrue(self.visitor.is_suitable(self.place, self.population))
		self.place.types = []
		self.assertFalse(self.visitor.is_suitable(self.place, self.population))

		self.place.types = ['restaurant']
		self.place.ratings.rating = None
		self.assertFalse(self.visitor.is_suitable(self.place, self.population))

		self.place.ratings.rating = 3.0
		self.assertFalse(self.visitor.is_suitable(self.place, self.population))

		self.place.placeInfo.businessStatus = 'CLOSED_PERMANENTLY'
		self.assertFalse(self.visitor.is_suitable(self.place, self.population))

		self.place.placeInfo.businessStatus = 'OPERATIONAL'
		self.place.ratings.userRatingCount = 0
		self.assertFalse(self.visitor.is_suitable(self.place, self.population))

		self.place.ratings.userRatingCount = 100
		self.place.ratings.rating = 4.0
		self.assertTrue(self.visitor.is_suitable(self.place, self.population))

	def test_is_suitable_businessStatus(self):
		self.assertTrue(self.visitor.is_suitable(self.place, self.population))
		self.place.placeInfo.businessStatus = 'CLOSED_PERMANENTLY'
		self.assertFalse(self.visitor.is_suitable(self.place, self.population))
		self.place.placeInfo.businessStatus = 'OPERATIONAL'
		self.assertTrue(self.visitor.is_suitable(self.place, self.population))
		self.place.placeInfo.businessStatus = 'CLOSED_TEMPORARILY'
		self.assertFalse(self.visitor.is_suitable(self.place, self.population))

	def test_check_types_incomplete_data(self):
		self.place.types = ['restauran', 'amusement park']
		self.assertFalse(self.visitor._check_types(self.place))
		self.place.types = []
		self.assertFalse(self.visitor._check_types(self.place))
		self.place.types = None
		self.assertFalse(self.visitor._check_types(self.place))

	def test_check_types_good_types(self):
		good_types = [
			'restaurant',
			'museum',
			'amusement_park',
			'aquarium',
			'art_gallery',
			'bowling_alley',
			'casino',
			'movie_theater',
			'night_club',
			'zoo',
		]
		for category in good_types:
			self.place.types = [category]
			self.assertTrue(self.visitor._check_types(self.place))

	def test_check_types_excluded_categories(self):
		excluded_categories = [
			'airport',
			'bus_station',
			'car_rental',
			'car_repair',
			'car_wash',
			'gas_station',
			'parking',
			'subway_station',
			'taxi_stand',
			'train_station',
			'transit_station',
		]
		for category in excluded_categories:
			self.place.types = [category]
			self.assertFalse(self.visitor._check_types(self.place))

	def test_save_places_to_database(self):
		pass


if __name__ == '__main__':
	unittest.main()
