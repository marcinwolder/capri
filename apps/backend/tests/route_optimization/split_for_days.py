import pickle
from datetime import date

from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import (
	Location,
	PlaceInfo,
	PlaceRating,
	RegularOpeningHours,
)
from src.data_model.places.places import Places
from src.path import get_path
from src.route_optimalization import SplitForDays

Place.__repr__ = lambda self: f'Place {self.placeInfo.id}'
Places.__repr__ = lambda self: f'Places {self.get_list()}'

from src.route_optimalization.not_used.osm import open_map

places = Places(
	[
		Place(
			placeInfo=PlaceInfo(id='1'),
			regularOpeningHours=RegularOpeningHours(
				periods=[
					{
						'open': {'day': 0, 'hour': 0, 'minute': 0},
						'close': {'day': 0, 'hour': 0, 'minute': 0},
					},
				]
			),
			location=Location(latitude=0, longitude=0),
			ratings=PlaceRating(rating=5.0),
		),
		Place(
			placeInfo=PlaceInfo(id='2'),
			regularOpeningHours=RegularOpeningHours(
				periods=[
					{
						'open': {'day': 0, 'hour': 1, 'minute': 0},
						'close': {'day': 0, 'hour': 10, 'minute': 0},
					},
				]
			),
			location=Location(latitude=1, longitude=1),
			ratings=PlaceRating(rating=4.0),
		),
		Place(
			placeInfo=PlaceInfo(id='3'),
			regularOpeningHours=RegularOpeningHours(
				periods=[
					{
						'open': {'day': 1, 'hour': 1, 'minute': 0},
						'close': {'day': 0, 'hour': 10, 'minute': 0},
					},
				]
			),
			location=Location(latitude=2, longitude=2),
			ratings=PlaceRating(rating=3.0),
		),
		Place(
			placeInfo=PlaceInfo(id='4'),
			regularOpeningHours=RegularOpeningHours(
				periods=[
					{
						'open': {'day': 2, 'hour': 1, 'minute': 0},
						'close': {'day': 0, 'hour': 10, 'minute': 0},
					},
					{
						'open': {'day': 6, 'hour': 1, 'minute': 0},
						'close': {'day': 0, 'hour': 10, 'minute': 0},
					},
				]
			),
			location=Location(latitude=3, longitude=3),
			ratings=PlaceRating(rating=2.0),
		),
		Place(
			placeInfo=PlaceInfo(id='5'),
			regularOpeningHours=RegularOpeningHours(
				periods=[
					{
						'open': {'day': 6, 'hour': 1, 'minute': 0},
						'close': {'day': 0, 'hour': 10, 'minute': 0},
					},
				]
			),
			location=Location(latitude=4, longitude=4),
			ratings=PlaceRating(rating=4.0),
		),
	]
)


def test_get_weekday_indices():
	start = date(2024, 4, 13)
	end = date(2024, 4, 16)
	split_for_days = SplitForDays(start, end, None)
	assert split_for_days.get_weekday_indices(start, end) == [6, 0, 1, 2]


def test_get_places_to_days():
	start = date(2024, 4, 13)
	end = date(2024, 4, 16)
	split_for_days = SplitForDays(start, end, places)
	places_to_days = split_for_days.get_places_to_days()

	expected = {
		'1': {0, 1, 2, 6},
		'2': {0},
		'3': {1},
		'4': {2, 6},
		'5': {6},
	}

	for key, days in places_to_days.items():
		assert set(days) == expected[key]


def test_split_basic():
	start = date(2024, 4, 13)
	end = date(2024, 4, 16)
	splitted = SplitForDays(start, end, places).split()
	assert all(
		place in [places.get_place_by_id('4'), places.get_place_by_id('5')]
		for place in splitted[0].get_list()
	)
	assert all(
		place in [places.get_place_by_id('1'), places.get_place_by_id('2')]
		for place in splitted[1].get_list()
	)
	assert all(
		place in [places.get_place_by_id('1'), places.get_place_by_id('3')]
		for place in splitted[2].get_list()
	)
	assert all(
		place in [places.get_place_by_id('1'), places.get_place_by_id('4')]
		for place in splitted[3].get_list()
	)


def test_split_real_data():
	start = date(2024, 4, 13)
	end = date(2024, 4, 16)
	places = pickle.load(open(get_path('places.pkl', 'data'), 'rb'))
	split_for_days = SplitForDays(start, end, places)
	weekday_indices = split_for_days.get_weekday_indices(start, end)
	assert weekday_indices == [6, 0, 1, 2]
	splitted = split_for_days.split()
	path = get_path('clusters.html', 'outputs')
	open_map(splitted, save_name=path)
	for i, day in enumerate(splitted):
		for place in day.get_list():
			opening_hours = place.regularOpeningHours
			assert opening_hours.periods[weekday_indices[i]].open_today is True
