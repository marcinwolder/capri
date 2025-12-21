from abc import abstractmethod

from collections.abc import Iterable

from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from src.data_model.place.place_subclasses import (
	AccessibilityOptions,
	Alcohol,
	Children,
	Dining,
	Location,
	Photo,
	PlaceInfo,
	PlaceRating,
	RegularOpeningHours,
	Review,
	TextWithLang,
)
from src.data_model.place.place_utils import map_prices
from src.rating.confidence_rating import confidence_rating_by_population


@dataclass_json
@dataclass
class Place:
	"""Class representing place in the city.

	Attributes:
	:param placeInfo: PlaceInfo - information about the place
	:param dining: Dining - information about dining options
	:param alcohol: Alcohol - information about alcohol options
	:param children: Children - information about children options
	:param ratings: PlaceRating - information about ratings
	:param reviews: list[Review] - list of reviews
	:param editorialSummary: TextWithLang - summary of the place

	:param types: list[str] - list of types of the place
	:param primaryTypeDisplayName: dict[str, str] - dictionary with primary type display name
	:param photos: list[Photo] - list of photos
	:param primaryType: str - primary type of the place
	:param location: Location - location of the place
	:param regularOpeningHours: RegularOpeningHours - regular opening hours of the place
	:param priceLevel: int - price level of the place
	:param accessibilityOptions: AccessibilityOptions - accessibility options
	:param allowsDogs: bool - information if the place allows dogs
	:param servesVegetarianFood: bool - information if the place serves vegetarian food
	:param estimatedTime: int - estimated time to spend in the place
	:param goodForGroups: bool - information if the place is good for groups
	:param subcategories: list[str] - list of subcategories

	Methods:
	must_see() - returns True if the place is worth seeing

	"""

	placeInfo: PlaceInfo = field(default_factory=PlaceInfo)
	dining: Dining = field(default_factory=Dining)
	alcohol: Alcohol = field(default_factory=Alcohol)
	children: Children = field(default_factory=Children)
	ratings: PlaceRating = field(default_factory=PlaceRating)
	reviews: list[Review] = field(default_factory=list)
	editorialSummary: TextWithLang = field(default_factory=TextWithLang)
	types: list[str] = field(default_factory=list)
	primaryTypeDisplayName: dict[str, str] = field(default_factory=dict)
	photos: list[Photo] = field(default_factory=list)
	primaryType: str = ''
	location: Location = field(default_factory=Location)
	regularOpeningHours: RegularOpeningHours = field(
		default_factory=RegularOpeningHours
	)
	priceLevel: int = 0
	accessibilityOptions: AccessibilityOptions = field(
		default_factory=AccessibilityOptions
	)
	allowsDogs: bool = False
	servesVegetarianFood: bool = False
	estimatedTime: int = 60
	goodForGroups: bool = False
	subcategories: list[str] = field(default_factory=list)

	@property
	def must_see(self):
		return self.ratings.statisticalRating > 4.5 and (
			'tourist_attraction' in self.types or 'historical_landmark' in self.types
		)

	def to_json(self):
		return self.to_dict()

	def to_dict(self):
		return {
			'types': self.types,
			'primaryTypeDisplayName': self.primaryTypeDisplayName,
			'primaryType': self.primaryType,
			'priceLevel': self.priceLevel,
			'allowsDogs': self.allowsDogs,
			'servesVegetarianFood': self.servesVegetarianFood,
			'estimatedTime': self.estimatedTime,
			'goodForGroups': self.goodForGroups,
			'subcategories': self.subcategories,
		}


class PlaceCreator:
	"""Abstract class for creating Place object.

	Attributes:
	:param data: dict - dictionary with data about the place
	:param city: City - city where the place is located

	"""

	def __init__(self, data, city):
		self.data = data
		self.city = city

	def _create_place(self):
		"""Create Place object from data."""
		place = Place(self.data, self.city)
		place.goodForGroups = self.data.get('goodForGroups', False)

		place.location = (
			Location(**self.data['location']) if 'location' in self.data else Location()
		)

		if (
			'regularOpeningHours' in self.data
			and 'periods' in self.data['regularOpeningHours']
		):
			place.regularOpeningHours = RegularOpeningHours(
				periods=self.data['regularOpeningHours']['periods'],
				weekdayDescriptions=self.data['regularOpeningHours'][
					'weekdayDescriptions'
				],
			)
		else:
			place.regularOpeningHours = RegularOpeningHours()
		place.types = self.data.get('types', [])
		place.primaryType = self.data.get(
			'primaryType',
			'tourist_attraction' if 'tourist_attraction' in place.types else '',
		)
		place.primaryTypeDisplayName = self.data.get('primaryTypeDisplayName', {})

		place.editorialSummary = TextWithLang(**self.data.get('editorialSummary', {}))
		place.accessibilityOptions = AccessibilityOptions(
			**self.data.get('accessibilityOptions', {})
		)
		place.reviews = [
			Review(**{k: v for k, v in review.items() if k in Review.__annotations__})
			for review in self.data.get('reviews', [])
		]
		place.photos = [
			Photo(**{k: v for k, v in photo.items() if k in Photo.__annotations__})
			for photo in self.data.get('photos', [])
		]

		place.priceLevel = map_prices(self.data.get('priceLevel', ''))

		place.estimatedTime = self.data.get('estimated_time', 60)
		place.estimatedTime = 60

		place.allowsDogs = self.data.get('allowsDogs', False)
		place.servesVegetarianFood = self.data.get('servesVegetarianFood', False)

		return place

	@abstractmethod
	def create_place(self):
		pass


class PlaceCreatorAPI(PlaceCreator):
	"""Class for creating Place object from API data."""

	def create_place(self):
		place = self._create_place()

		place.placeInfo = PlaceInfo(
			name=self.data.get('name', ''),
			id=self.data.get('id', ''),
			formattedAddress=self.data.get('formattedAddress', ''),
			googleMapsUri=self.data.get('googleMapsUri', ''),
			websiteUri=self.data.get('websiteUri', ''),
			iconMaskBaseUri=self.data.get('iconMaskBaseUri', ''),
			displayName=self.data.get('displayName', {'text': ''})['text'],
			businessStatus=self.data.get('businessStatus', ''),
		)

		place.dining = Dining(
			reservable=self.data.get('reservable', False),
			takeout=self.data.get('takeout', False),
			dineIn=self.data.get('dineIn', False),
			delivery=self.data.get('delivery', False),
			outdoorSeating=self.data.get('outdoorSeating', False),
			servesBreakfast=self.data.get('servesBreakfast', False),
			servesLunch=self.data.get('servesLunch', False),
			servesDinner=self.data.get('servesDinner', False),
			servesBrunch=self.data.get('servesBrunch', False),
			servesDessert=self.data.get('servesDessert', False),
			servesCoffee=self.data.get('servesCoffee', False),
			goodForWatchingSports=self.data.get('goodForWatchingSports', False),
		)

		place.alcohol = Alcohol(
			servesBeer=self.data.get('servesBeer', False),
			servesWine=self.data.get('servesWine', False),
			servesCocktails=self.data.get('servesCocktails', False),
		)

		place.children = Children(
			goodForChildren=self.data.get('goodForChildren', False),
			menuForChildren=self.data.get('menuForChildren', False),
		)
		rating = self.data.get('rating', 0)
		userRatingCount = self.data.get('userRatingCount', 0)
		place.ratings = PlaceRating(
			statisticalRating=self.data.get('statisticalRating', 0),
			userRatingCount=userRatingCount,
			confidenceRating=confidence_rating_by_population(
				rating,
				userRatingCount,
				self.city.population,
			),
			rating=rating,
			cumulative_rating=0,
		)
		return place


class PlaceCreatorDatabase(PlaceCreator):
	"""Class for creating Place object from database data."""

	def create_place(self):
		"""Create Place object from database data."""
		place = self._create_place()

		place.children = Children(**self.data.get('children', {}))
		place.dining = Dining(**self.data.get('dining', {}))
		place.alcohol = Alcohol(**self.data.get('alcohol', {}))
		place.placeInfo = PlaceInfo(**self.data.get('placeInfo', {}))
		place.ratings = PlaceRating(**self.data.get('ratings', {}))
		place.reviews = [
			Review(**{k: v for k, v in review.items() if k in Review.__annotations__})
			for review in self.data.get('reviews', [])
		]
		return place
