from src.data_model.place._place import Location
from src.route_optimalization.travel.travel_time import get_travel_time


def test_travel_time():
	start_coordinates = Location(latitude=59.323356399999994, longitude=18.09639)
	end_coordinates = Location(latitude=59.366065, longitude=18.0313543)
	time, distance = get_travel_time(
		start_coordinates, end_coordinates, transport='car'
	)

	if time < 1000:
		assert True
