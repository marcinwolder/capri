from src.data_model.place.place import Place

from src.data_model.place.place_subclasses import (
	AccessibilityOptions,
	Alcohol,
	Children,
	Dining,
	PlaceInfo,
)
from src.data_model.user.user_preferences import UserPreferences


def _arguments_rating(*args):
	"""It calculates the arithmetic mean of the given arguments."""

	return sum(args) / len([int(arg) for arg in args])


class UserPreferencesRating:
	"""rating = -1 -> dany czynnik nie jest brany pod uwagę.

	rating = 0 -> dany czynnik jest brany pod uwagę, ale nie spełnia oczekiwań.

	rating = 1 -> dany czynnik jest brany pod uwagę i spełnia oczekiwania.

	"""

	def __init__(self, user_preferences: UserPreferences):
		self.user_preferences = user_preferences

	def category_rating(self, types: list[str]):
		rating = 0

		if len([1 for type in types if type in self.user_preferences.categories]) == 0:
			return 0

		for category in types:
			if category in self.user_preferences.categories:
				rating += 1

		if rating:
			return rating / len(self.user_preferences.categories)

		return 0

	def subcategory_rating(self, subcategories: list[str]):
		rating = 0

		for subcategory in subcategories:
			if subcategory in self.user_preferences.subcategories:
				rating += 1

		return rating / len(self.user_preferences.subcategories) if rating else -1

	def __repr__(self):
		return str(self.__dict__)

	def alcohol_rating(self, alcohol: Alcohol):
		if self.user_preferences.alcohol:
			return _arguments_rating(
				alcohol.servesBeer, alcohol.servesWine, alcohol.servesCocktails
			)

		return -1.0

	def dining_rating(self, restaurant: Dining) -> float:
		# FIXME: 18.11.2025 - This is not right. There is no dining attr in UserPreferences. This function is not used anyways. ~Folder
		# if self.user_preferences.dining:
		# 	return _arguments_rating(
		# 		restaurant.goodForWatchingSports,
		# 		restaurant.reservable,
		# 		restaurant.takeout,
		# 		restaurant.dineIn,
		# 		restaurant.delivery,
		# 		restaurant.outdoorSeating,
		# 		restaurant.servesBreakfast,
		# 		restaurant.servesLunch,
		# 		restaurant.servesDinner,
		# 		restaurant.servesBrunch,
		# 		restaurant.outdoorSeating,
		# 		restaurant.servesDessert,
		# 		restaurant.servesCoffee,
		# 	)

		return -1.0

	def children_rating(self, children: Children):
		if self.user_preferences.children:
			return _arguments_rating(children.goodForChildren, children.menuForChildren)

		return -1.0

	def servesVegetarianFood_rating(self, servesVegetarianFood: bool):
		if self.user_preferences.serves_vegetarian_food:
			return int(servesVegetarianFood)

		return -1.0

	def accessibilityOptions_rating(self, accessibilityOptions: AccessibilityOptions):
		if self.user_preferences.accessibility_options:
			return _arguments_rating(
				accessibilityOptions.wheelchairAccessibleParking,
				accessibilityOptions.wheelchairAccessibleSeating,
				accessibilityOptions.wheelchairAccessibleEntrance,
				accessibilityOptions.wheelchairAccessibleRestroom,
			)

		return -1.0

	def allowsDogs_rating(self, allowsDogs: bool):
		if self.user_preferences.allows_dogs:
			return float(allowsDogs)

		return -1.0

	def priceLevel_rating(self, priceLevel: int) -> float:
		if self.user_preferences.price_level >= priceLevel:
			return 1.0

		return 0.0

	def goodForGroups_rating(self, goodForGroups: bool) -> float:
		if self.user_preferences.good_for_groups:
			return float(goodForGroups)

		return -1.0


def debug():
	user_needs = UserPreferences(
		5,
		['museum', 'park'],
		{'museum': ['Art', 'History'], 'park': []},
		[],
	)

	place = Place(
		placeInfo=PlaceInfo(id='1'),
		types=['museum', 'park'],
		subcategories=['Art', 'History'],
		accessibilityOptions=AccessibilityOptions(),
	)

	user_preferences_rating = UserPreferencesRating(user_needs)

	print(user_preferences_rating.category_rating(place.types))


if __name__ == '__main__':
	debug()
