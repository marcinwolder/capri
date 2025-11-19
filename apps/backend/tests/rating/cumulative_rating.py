from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import AccessibilityOptions
from src.data_model.user.user_preferences import UserPreferences
from src.rating.cumulative_rating import _calculate_cumulative_rating
from src.rating.user_preferences_rating import UserPreferencesRating


def _make_user_preferences_rating():
	user = UserPreferences(
		['wheelchair_accessible', 'outdoor', 'vegan', 'children'],
		5,
		['museum', 'park'],
		{'museum': ['Art', 'History'], 'park': []},
	)
	return user


def _make_place():
	return Place(
		placeInfo={'id': '1'},
		types=['museum', 'park'],
		subcategories=['Art', 'History'],
		accessibilityOptions=AccessibilityOptions(),
	)


def test_confidence_rating_4():
	user_preferences_rating = UserPreferencesRating(_make_user_preferences_rating())
	place = _make_place()
	rating = _calculate_cumulative_rating(place, user_preferences_rating)
	print(rating)
	assert rating == 1
