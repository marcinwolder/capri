import pytest
import responses

from src.api_calls import get_restaurants_for_city

invalid_location = 'invalid_location'
valid_location = (40.7128, -74.0060)
valid_excluded_types = ['bar', 'cafe']
radius = 1000
city_population = 1000000


@responses.activate
def test_get_restaurants_for_city_valid_input():
	responses.add(
		responses.POST,
		'https://places.googleapis.com/v1/places:searchNearby',
		json={'result': 'success'},
		status=200,
	)

	response = get_restaurants_for_city(
		None,
		lat=valid_location[0],
		lng=valid_location[1],
		radius=radius,
		city=city_population,
		open_ai_client=None,
		included_types='restaurant',
	)
	for i in response.get_list():
		print(i)
	print(len(response.get_list()))


def test_get_restaurants_for_city_invalid_input():
	response = get_restaurants_for_city(invalid_location, valid_excluded_types)
	assert response.status_code == 400


def test_get_restaurants_for_city_invalid_api_key():
	mock_getenv.return_value = None

	ret = get_restaurants_for_city(valid_location, valid_excluded_types)
	assert ret.status_code == 403


def test_get_restaurants_for_city_invalid_location():
	ret = get_restaurants_for_city(invalid_location, valid_excluded_types)
	assert ret.status_code == 400


def test_get_restaurants_for_city_invalid_radius():
	ret = get_restaurants_for_city(valid_location, valid_excluded_types, -1)
	assert ret.status_code == 400


def test_get_restaurants_for_city_success_1():
	ret = get_restaurants_for_city((50.06143, 19.93658), 'restaurant', ['bar', 'cafe'])
	assert ret.status_code == 200


def test_get_restaurants_for_city_success_2():
	ret = get_restaurants_for_city((13.7563, 100.5018), 'restaurant', ['bar', 'cafe'])
	assert ret.status_code == 200


if __name__ == '__main__':
	pytest.main()
