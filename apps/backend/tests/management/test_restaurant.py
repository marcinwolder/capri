from src.api_calls import get_restaurants_for_city, nearby_search

valid_location = (40.7128, -74.0060)
krakow_location = (50.06143, 19.93658)
radius = 100000
city_population = 1000000


def test():
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


def test1():
	ret = nearby_search(krakow_location, included_types=['restaurant'])
	print(ret.json())
