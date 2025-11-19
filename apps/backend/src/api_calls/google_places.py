import json
import logging
import os

import requests
from dotenv import load_dotenv
from requests import Response

from src.constants import all_categories, default_categories, excluded_categories
from src.data_model import City, Places
from src.data_model.place.place import PlaceCreator, PlaceCreatorAPI
from src.data_model.place.place_visitor import RestaurantVisitor, Visitor
from src.path import get_path
from src.rating.statistical_rating import StatisticalRating

load_dotenv()


def get_one_attraction_by_id(place_id: str, fields: str = '*') -> dict:
	"""Debug function that makes a request to Google Places API.

	:param place_id: id of the place
	:param fields: fields to be returned
	:return: response from Google Places API
	"""
	url = f'https://places.googleapis.com/v1/places/{place_id}?fields={fields}&key={os.getenv("GOOGLE_PLACES_API_KEY")}'
	response = requests.get(url)
	return response.json()


def nearby_search(
	location,
	included_primary_types=None,
	included_types=None,
	excluded_types=None,
	radius=20000,
) -> Response:
	"""Function that makes a nearby search request to Google Places API.

	:param included_types: list of included types
	:param included_primary_types: list of included primary types
	:param location: location of the city
	:param excluded_types: list of excluded types
	:param radius: radius of the search
	:return: response from Google Places API
	"""
	max_result_count = 20
	url = 'https://places.googleapis.com/v1/places:searchNearby'
	api_key = os.getenv('GOOGLE_PLACES_API_KEY')
	headers = {
		'X-Goog-Api-Key': api_key,
		'X-Goog-FieldMask': '*',
		'Content-Type': 'application/json',
	}

	data = {
		'includedPrimaryTypes': included_primary_types,
		'includedTypes': included_types,
		'excludedTypes': excluded_types,
		'maxResultCount': max_result_count,
		'locationRestriction': {
			'circle': {
				'center': {
					'latitude': location[0],
					'longitude': location[1],
				},
				'radius': radius,
			},
		},
	}

	if included_primary_types is None:
		data.pop('includedPrimaryTypes')
	if included_types is None:
		data.pop('includedTypes')

	response = requests.post(url, headers=headers, data=json.dumps(data))
	return response


def get_restaurants_for_city(
	db, lat, lng, radius, city, vegan=False, included_types=None
) -> Places:
	if included_types is None:
		included_types = ['restaurant']
	if vegan:
		included_types.append('vegan_restaurant')
	places_list = []
	search_results = nearby_search(
		location=(lat, lng),
		excluded_types=excluded_categories,
		radius=radius,
		included_types=included_types,
	).json()
	try:
		if search_results['places'] is None:
			print('No places found')
		for result in search_results['places']:
			place = PlaceCreatorAPI(result, city).create_place()
			if not RestaurantVisitor().is_suitable(
				place=place, population=city.population
			):
				continue

			places_list.append(place)
	except KeyError:
		logging.exception('KeyError: %s', search_results)
	places = Places(places_list, city)
	StatisticalRating(places).calculate_statistical_rating()

	return places


def get_places_for_city(
	db,
	city: City,
	placeCreator: type[PlaceCreator],
	placeVisitor: type[Visitor],
	search_categories=all_categories,
	save_raw=False,
) -> Places:
	"""Function that gets places from Google Places API.

	:param db: database_module
	:param city: city
	:param open_ai_client: OpenAIClient
	:param placeCreator: PlaceCreator
	:param placeVisitor: Visitor
	:param search_categories: list of search categories
	:param save_raw: bool
	:return: Places
	"""
	places_list = []
	places_raw = []
	placeVisitor = placeVisitor()

	def process_search_results(search_results):
		try:
			if save_raw:
				places_raw.extend(search_results['places'])
			for result in search_results['places']:
				place = placeCreator(result, city).create_place()
				if not placeVisitor.is_suitable(
					place=place, population=city.population
				):
					continue
				places_list.append(place)
		except KeyError:
			logging.exception('KeyError: %s', search_results)

	process_search_results(
		nearby_search(
			location=(city.lat, city.lng),
			included_types=['tourist_attraction'],
			excluded_types=excluded_categories,
			radius=city.get_radius(),
		).json()
	)
	for category in search_categories:
		search_results = nearby_search(
			location=(city.lat, city.lng),
			included_primary_types=category,
			excluded_types=excluded_categories,
			radius=city.get_radius(),
		).json()
		process_search_results(search_results)
	if save_raw:
		with open(get_path('raw.json', 'data'), 'w') as f:
			json.dump(places_raw, f, default=vars)
	places = Places(places_list, city)
	StatisticalRating(places).calculate_statistical_rating()

	if db is not None:
		placeVisitor.save_places_to_database(db, places, city, default_categories)
	return places
