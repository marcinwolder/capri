from src.data_model.place.place import Place
from src.data_model.user.user_preferences import UserPreferences
from src.data_model.place.place_subclasses import *


def _arguments_rating(*args):
    """It calculates the arithmetic mean of the given arguments."""
    return sum(args) / len([int(arg) for arg in args])


class UserPreferencesRating:
    """
    rating = -1 -> dany czynnik nie jest brany pod uwagę.
    rating = 0 -> dany czynnik jest brany pod uwagę, ale nie spełnia oczekiwań.
    rating = 1 -> dany czynnik jest brany pod uwagę i spełnia oczekiwania.
    """

    def __init__(self, user_preferences: UserPreferences):
        self.user_preferences = user_preferences

    def category_rating(self,  types: list[str]):  
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
            return _arguments_rating(alcohol.servesBeer,
                                     alcohol.servesWine, alcohol.servesCocktails)
        return -1  

    def dining_rating(self, restaurant: Dining):  
        if self.user_preferences.dining:
            return _arguments_rating(restaurant.goodForWatchingSports,
                                     restaurant.reservable,
                                     restaurant.takeout,
                                     restaurant.dineIn,
                                     restaurant.delivery,
                                     restaurant.outdoorSeating,
                                     restaurant.servesBreakfast,
                                     restaurant.servesLunch,
                                     restaurant.servesDinner,
                                     restaurant.servesBrunch,
                                     restaurant.outdoorSeating,
                                     restaurant.servesDessert,
                                     restaurant.servesCoffee)
        else:
            return -1

    def children_rating(self, children: Children):
        if self.user_preferences.children:
            return _arguments_rating(children.goodForChildren, children.menuForChildren)
        return -1

    def servesVegetarianFood_rating(self, servesVegetarianFood: bool):  
        if self.user_preferences.servesVegetarianFood:
            return int(servesVegetarianFood)
        return -1

    def accessibilityOptions_rating(self, accessibilityOptions: AccessibilityOptions):
        if self.user_preferences.accessibilityOptions:
            return _arguments_rating(accessibilityOptions.wheelchairAccessibleParking,
                                     accessibilityOptions.wheelchairAccessibleSeating,
                                     accessibilityOptions.wheelchairAccessibleEntrance,
                                     accessibilityOptions.wheelchairAccessibleRestroom
                                     )
        return -1

    def allowsDogs_rating(self, allowsDogs: bool):
        if self.user_preferences.allowsDogs:
            return int(allowsDogs)
        return -1

    def priceLevel_rating(self, priceLevel: int):
        if self.user_preferences.priceLevel >= priceLevel:
            return 1
        return 0

    def goodForGroups_rating(self, goodForGroups: bool):
        if self.user_preferences.goodForGroups:
            return int(goodForGroups)
        return -1


def debug():
    user_needs = UserPreferences([],
                                 5, ['museum', 'park'], {'museum': ['Art', 'History'], 'park': []}
                                 )

    place = Place(placeInfo={'id': '1'},
                  types=['museum', 'park'],
                  subcategories=['Art', 'History'],
                  accessibilityOptions=AccessibilityOptions(),
                  )

    user_preferences_rating = UserPreferencesRating(user_needs)
    print(user_preferences_rating.category_rating(place.types))


if __name__ == '__main__':
    debug()
