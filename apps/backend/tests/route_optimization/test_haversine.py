from src.route_optimalization.haversine import calculate_distance


def test_calculate_distance():
	location1 = 50, 19
	location2 = 50, 19
	ret = calculate_distance(location1[0], location1[1], location2[0], location2[1])
	assert ret == 0


def test_calculate_distance_2():
	location1 = 50.059553099999995, 19.9380345
	location2 = 50.0484899, 19.912295999999998
	ret = calculate_distance(location1[0], location1[1], location2[0], location2[1])
	assert int(ret) == 2.0
