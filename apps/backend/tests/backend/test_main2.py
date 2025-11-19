from src.data_model.city.city import City
from src.data_model.user.user_info import TripInfo
from src.data_model.user.user_preferences import UserPreferences


def _make_dict():
	"""Check if loc exist in firebase db."""
	return {
		'days': 1,
		'categories': {
			'museum': ['Art', 'History', 'Science', 'War', 'Maritime'],
			'park': [],
			'zoo': [],
			'church': [],
		},
		'restaurant': ['Polish', 'Italian', 'French', 'Asian', 'American'],
		'city_id': City.get_const_krakow().id,
		'use_saved_preferences': False,
		'user_preferences': {
			'wheelchair_accessible': True,
			'family_friendly': False,
			'allowsDogs': True,
			'outdoor': True,
			'price_level': 1,
			'goodForGroups': True,
			'vegan': True,
			'children': True,
			'alcohol': True,
		},
		'user_id': 'user_id',
		'location': {'latitude': 50.06143, 'longitude': 19.93658},
	}


def test_main():
	data = _make_dict()
	categories = [category for category in data['categories'].keys()]
	subcategories = data['categories']
	print(categories)
	print(subcategories)
	user_needs = UserPreferences(data['user_preferences'], categories, subcategories)
	city = City(data['city_id'])
	user = TripInfo(user_preferences=user_needs, city=city, days=data['days'])
