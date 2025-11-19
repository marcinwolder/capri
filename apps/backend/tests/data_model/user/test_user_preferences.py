from src.data_model.user.user_preferences import UserPreferences


def test_user_preferences():
	data = {
		'priceLevel': 2,
		'wheelchairAccessible': True,
		'goodForGroups': True,
		'vegan': True,
		'children': True,
		'alcohol': True,
		'allowsDogs': True,
		'restaurant': ['italian', 'pub'],
	}

	user_preferences = UserPreferences(
		needs=data,
		categories=['restaurant', 'bar'],
		subcategories=['italian', 'pub'],
	)

	print(user_preferences)

	assert user_preferences.categories == ['restaurant', 'bar']

	assert user_preferences.subcategories == ['italian', 'pub']

	assert user_preferences.alcohol == True

	assert user_preferences.children == True

	assert user_preferences.price_level == 2

	assert user_preferences.to_dict() == {
		'priceLevel': 2,
		'wheelchairAccessible': True,
		'goodForGroups': True,
		'vegan': True,
		'children': True,
		'alcohol': True,
		'allowsDogs': True,
		'restaurant': ['italian', 'pub'],
	}

	assert (
		user_preferences.to_json()
		== '{"priceLevel": 2, "wheelchairAccessible": true, "goodForGroups": '
		'true, "vegan": true, "children": true, "alcohol": true, "allowsDogs": true, '
		'"restaurant": ["italian", "pub"]}'
	)


def test_user_preferences_2():
	data = {
		'priceLevel': 1,
		'wheelchairAccessible': False,
		'goodForGroups': False,
		'vegan': False,
		'children': False,
		'alcohol': False,
		'allowsDogs': False,
		'restaurant': [],
	}

	user_preferences = UserPreferences(
		needs=data,
		categories=['restaurant', 'bar'],
		subcategories=['italian', 'pub'],
	)

	print(user_preferences)

	assert user_preferences.categories == ['restaurant', 'bar']

	assert user_preferences.subcategories == ['italian', 'pub']

	assert user_preferences.alcohol == False

	assert user_preferences.children == False

	assert user_preferences.price_level == 1

	assert user_preferences.to_dict() == {
		'priceLevel': 1,
		'wheelchairAccessible': False,
		'goodForGroups': False,
		'vegan': False,
		'children': False,
		'alcohol': False,
		'allowsDogs': False,
		'restaurant': [],
	}

	assert (
		user_preferences.to_json()
		== '{"priceLevel": 1, "wheelchairAccessible": false, "goodForGroups": '
		'false, "vegan": false, "children": false, "alcohol": false, "allowsDogs": false, '
		'"restaurant": []}'
	)
