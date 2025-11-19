"""To test the routing module, we have 10 atractions in a city.
We will use the Routing class to split the attractions into 3 days.
We will also visualize the graph with the attractions and the routes.
"""

import pickle
from datetime import date

from src.route_optimalization.not_used.osm import open_map

from src.data_model.city.city import City
from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import (
	Location,
	Period,
	PlaceInfo,
	PlaceRating,
	RegularOpeningHours,
	TimePoint,
)
from src.data_model.places.places import Places
from src.data_model.user.user_info import TripInfo
from src.path import get_path
from src.route_optimalization import SplitForDays
from src.route_optimalization.routing import Routing

Wawel_location = Location(50.0547, 19.9354)
AGH_location = Location(50.0661, 19.9135)
Rynek_location = Location(50.0614, 19.9366)
Kazimierz_location = Location(50.0499, 19.9449)
Wieliczka_location = Location(49.9875, 20.0611)

city = City.get_const_krakow()
hotel = Place(
	placeInfo=PlaceInfo(displayName='Hotel'),
	location=Location(latitude=city.lat, longitude=city.lng),
	regularOpeningHours=RegularOpeningHours(
		periods=[Period(open=TimePoint(), close=TimePoint(23)) for _ in range(7)],
		weekdayDescriptions=[''],
	),
	estimatedTime=0,
)


def test_openingHours():
	place1 = Place(
		placeInfo=PlaceInfo(id='1', name='place1'),
		location=Wawel_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=10), close=TimePoint(hour=18))
				for _ in range(7)
			]
		),
	)

	place2 = Place(
		placeInfo=PlaceInfo(id='2', name='place2'),
		location=AGH_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=11), close=TimePoint(hour=18))
				for _ in range(7)
			]
		),
	)

	place3 = Place(
		placeInfo=PlaceInfo(id='3', name='place3'),
		location=Rynek_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=11), close=TimePoint(hour=17))
				for _ in range(7)
			]
		),
	)

	places = Places([place1, place2, place3], city)
	routes = Routing(places, depot=hotel, num_routes=1).get_routes()
	assert routes[0].get_list()[0].placeInfo.id == '3'


def test_closing_hours():
	"""Test if the routing module works correctly.
	We have 3 places, that have the same rating, but different opening hours, the first one is open from 10 to 18,
	the second one is open from 10 to 18, and the third one is open from 10 to 17.
	To co zamyka się najszybciej powinno być na początku trasy * jeśli odległość nie ma znaczącej roli*
	"""
	place1 = Place(
		placeInfo=PlaceInfo(id='1', name='place1'),
		location=Wawel_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=10), close=TimePoint(hour=18))
				for _ in range(7)
			]
		),
	)

	place2 = Place(
		placeInfo=PlaceInfo(id='2', name='place2'),
		location=AGH_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=10), close=TimePoint(hour=18))
				for _ in range(7)
			]
		),
	)

	place3 = Place(
		placeInfo=PlaceInfo(id='3', name='place3'),
		location=Rynek_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=10), close=TimePoint(hour=17))
				for _ in range(7)
			]
		),
	)

	places = Places([place1, place2, place3], city)

	routes = Routing(places, depot=hotel, num_routes=1).get_routes()
	assert routes[0].get_list()[0].placeInfo.id == '3'


def test_order():
	place1 = Place(
		placeInfo=PlaceInfo(id='1', displayName='place1'),
		location=Wawel_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=11), close=TimePoint(hour=14))
				for _ in range(7)
			]
		),
	)

	place2 = Place(
		placeInfo=PlaceInfo(id='2', displayName='place2'),
		location=AGH_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=12), close=TimePoint(hour=15))
				for _ in range(7)
			]
		),
	)

	place3 = Place(
		placeInfo=PlaceInfo(id='3', displayName='place3'),
		location=Rynek_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=13), close=TimePoint(hour=16))
				for _ in range(7)
			]
		),
	)

	places = Places([place1, place2, place3], city)

	routes = Routing(places, depot=hotel, num_routes=1).get_routes()
	assert routes[0].get_list()[0].placeInfo.id == '1'
	assert routes[0].get_list()[1].placeInfo.id == '2'
	assert routes[0].get_list()[2].placeInfo.id == '3'


def test_dropping_places_with_lower_rating():
	"""Two places with the same opening hours, but different ratings,
	the one with lower rating should be dropped.
	"""
	place1 = Place(
		placeInfo=PlaceInfo(id='1', displayName='place1'),
		location=Wawel_location,
		ratings=PlaceRating(rating=4.0, confidenceRating=4.0),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=11), close=TimePoint(hour=12))
				for _ in range(7)
			]
		),
	)

	place2 = Place(
		placeInfo=PlaceInfo(id='2', displayName='place2'),
		location=AGH_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=11), close=TimePoint(hour=12))
				for _ in range(7)
			]
		),
	)
	places = Places([place1, place2], city)

	routes = Routing(places, depot=hotel, num_routes=1).get_routes()
	assert routes[0].get_list()[0].placeInfo.id == '2'
	assert len(routes[0].get_list()) == 1


def test_open_is_close():
	"""Two places with the same opening hours, but different ratings,
	the one with lower rating should be dropped.
	"""
	place1 = Place(
		placeInfo=PlaceInfo(id='1', displayName='place1'),
		location=Wawel_location,
		ratings=PlaceRating(rating=4.0, confidenceRating=4.0),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=11), close=TimePoint(hour=11))
				for _ in range(7)
			]
		),
	)

	place2 = Place(
		placeInfo=PlaceInfo(id='2', displayName='place2'),
		location=AGH_location,
		ratings=PlaceRating(rating=4.5, confidenceRating=4.5),
		regularOpeningHours=RegularOpeningHours(
			periods=[
				Period(open=TimePoint(hour=12), close=TimePoint(hour=12))
				for _ in range(7)
			]
		),
	)
	places = Places([place1, place2], city)

	routes = Routing(places, depot=hotel, num_routes=1).get_routes()
	assert len(routes[0]) == 0


def test_real_data():
	start = date(2024, 4, 13)
	end = date(2024, 4, 16)
	places = pickle.load(open(get_path('places.pkl', 'data'), 'rb'))
	places_good_hours = Places(
		[
			place
			for place in places.get_list()
			if place.regularOpeningHours.periods[0].open_in_minutes
			< place.regularOpeningHours.periods[0].close_in_minutes
		],
		places.city,
	)
	splitForDays = SplitForDays(from_date=start, to_date=end, places=places_good_hours)
	clustered_places = splitForDays.split()

	recommended_places = []
	hotel = TripInfo(city=places.city)._init_hotel()
	for i, places in enumerate(clustered_places):
		period = splitForDays.weekday_indices[i]
		route = Routing(
			places, depot=hotel, num_routes=1, period_index=period
		).get_routes()[0]
		recommended_places.append(route)

	print('recommended_places', recommended_places)
	open_map(recommended_places, city=places.city)
