import unittest

from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import AccessibilityOptions, Alcohol, Children
from src.data_model.user.user_preferences import UserPreferences
from src.rating.user_preferences_rating import UserPreferencesRating


def _make_user_preferences_rating():
    user = UserPreferences(['wheelchair_accessible', 'outdoor', 'vegan', 'children'],
                           5, ['museum', 'park'], {'museum': ['Art', 'History'], 'park': []}
                           )
    return user


def _make_place():
    return Place(placeInfo={'id': '1'},
                 types=['museum', 'park'],
                 subcategories=['Art', 'History'],
                 accessibilityOptions=AccessibilityOptions(),
                 )


class TestUserNeedsRating(unittest.TestCase):

    def setUp(self):
        self.userPreferences = UserPreferences([], 5, [], {})
        self.user_preferences_rating = UserPreferencesRating(self.userPreferences)
        self.place = _make_place()

    def test_alcohol_rating(self):
        assert self.user_preferences_rating.alcohol_rating(self.place.alcohol) == -1

    def test_allowsDogs_rating(self):
        assert self.user_preferences_rating.allowsDogs_rating(self.place.allowsDogs) == -1

    def test_servesVegetarianFood_rating(self):
        assert self.user_preferences_rating.servesVegetarianFood_rating(self.place.servesVegetarianFood) == -1

    def test_children_rating(self):
        assert self.user_preferences_rating.children_rating(self.place.children) == -1

    def test_accessibilityOptions_rating(self):
        assert self.user_preferences_rating.accessibilityOptions_rating(self.place.accessibilityOptions) == -1

    def test_goodForGroups_rating(self):
        assert self.user_preferences_rating.goodForGroups_rating(self.place.goodForGroups) == -1


class TestUserNeedsRatingAllNeeds(unittest.TestCase):

    def setUp(self):
        self.userPreferences = UserPreferences(['wheelchairAccessible', 'outdoor', 'vegan', 'children', 'allowsDogs',
                                                'alcohol', 'goodForGroups'], 5, [], {})
        self.place = _make_place()

    def test_alcohol_rating(self):
        user_preferences_rating = UserPreferencesRating(self.userPreferences)
        self.place.alcohol = Alcohol(False, False, False)
        assert user_preferences_rating.alcohol_rating(self.place.alcohol) == 0

        self.place.alcohol = Alcohol(False, False, True)
        assert user_preferences_rating.alcohol_rating(self.place.alcohol) == 1 / 3

        self.place.alcohol = Alcohol(True, True, True)
        assert user_preferences_rating.alcohol_rating(self.place.alcohol) == 1

    def test_allowsDogs_rating(self):
        user_preferences_rating = UserPreferencesRating(self.userPreferences)
        self.place.allowsDogs = False
        assert user_preferences_rating.allowsDogs_rating(self.place.allowsDogs) == 0

        self.place.allowsDogs = True
        assert user_preferences_rating.allowsDogs_rating(self.place.allowsDogs) == 1

    def test_servesVegetarianFood_rating(self):
        user_preferences_rating = UserPreferencesRating(self.userPreferences)
        self.place.servesVegetarianFood = False
        assert user_preferences_rating.servesVegetarianFood_rating(self.place.servesVegetarianFood) == 0

        self.place.servesVegetarianFood = True
        assert user_preferences_rating.servesVegetarianFood_rating(self.place.servesVegetarianFood) == 1

    def test_children_rating(self):
        user_preferences_rating = UserPreferencesRating(self.userPreferences)
        self.place.children = Children(False, False)

        assert user_preferences_rating.children_rating(self.place.children) == 0

        self.place.children = Children(True, True)
        assert user_preferences_rating.children_rating(self.place.children) == 1

    def test_accessibilityOptions_rating(self):
        user_preferences_rating = UserPreferencesRating(self.userPreferences)

        self.place.accessibilityOptions = AccessibilityOptions(False, False, False, False)
        assert user_preferences_rating.accessibilityOptions_rating(self.place.accessibilityOptions) == 0

        self.place.accessibilityOptions = AccessibilityOptions(False, False, False, True)
        assert user_preferences_rating.accessibilityOptions_rating(self.place.accessibilityOptions) == 1 / 4

        self.place.accessibilityOptions = AccessibilityOptions(False, False, True, True)
        assert user_preferences_rating.accessibilityOptions_rating(self.place.accessibilityOptions) == 2 / 4

        self.place.accessibilityOptions = AccessibilityOptions(False, True, True, True)
        assert user_preferences_rating.accessibilityOptions_rating(self.place.accessibilityOptions) == 3 / 4

        self.place.accessibilityOptions = AccessibilityOptions(True, True, True, True)
        assert user_preferences_rating.accessibilityOptions_rating(self.place.accessibilityOptions) == 1

    def test_goodForGroups_rating(self):
        user_preferences_rating = UserPreferencesRating(self.userPreferences)
        self.place.goodForGroups = False
        assert user_preferences_rating.goodForGroups_rating(self.place.goodForGroups) == 0

        self.place.goodForGroups = True
        assert user_preferences_rating.goodForGroups_rating(self.place.goodForGroups) == 1


class TestUserPreferencesRatingNoCategories(unittest.TestCase):

    def setUp(self):
        self.user_preferences = UserPreferences([], 5, [], {})
        self.user_preferences_rating = UserPreferencesRating(self.user_preferences)
        self.place = _make_place()

    def test_category_rating(self):
        assert self.user_preferences_rating.category_rating(self.place.types) == -1

    def test_subcategory_rating(self):
        assert self.user_preferences_rating.subcategory_rating(self.place.subcategories) == -1

class TestUserPreferencesPlacesOfWorship(unittest.TestCase):
    def setUp(self):
        self.user_preferences_church = UserPreferences([], 5, ['place_of_worship'],
                                                {'place_of_worship': ['church']})
        self.user_preferences_empty = UserPreferences([], 5, ['place_of_worship'],
                                                {'place_of_worship': []})

    def test_handle_places_of_worship(self):
        assert self.user_preferences_church.categories == ['church']
        assert self.user_preferences_church.subcategories == {'church': []}

    def test_handle_places_of_worship_empty(self):
        assert self.user_preferences_empty.categories == ['church', 'mosque', 'synagogue']
        assert self.user_preferences_empty.subcategories == {'church': [], 'mosque': [], 'synagogue': []}

