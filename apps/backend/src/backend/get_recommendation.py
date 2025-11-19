import json
import logging
from datetime import date

from src.api_calls.google_places import get_places_for_city
from src.data_model.city.city import City
from src.data_model.place.place import PlaceCreatorAPI, PlaceCreatorDatabase
from src.data_model.place.place_visitor import PlaceVisitor
from src.data_model.places.places import Places
from src.data_model.user.user_info import TripInfo
from src.data_model.user.user_preferences import UserPreferences
from src.database import DataBase, DataBaseUsers
from src.path import get_path
from src.recommendation import Recommendation


def _get_from_file(city, file_name='attractions.json'):
	"""Function that reads data from file and creates places."""
	with open(get_path(file_name, 'data')) as f:
		attractions = json.load(f)
	places = []
	for i in attractions:
		if file_name == 'raw.json':
			place = PlaceCreatorAPI(i, city).create_place()
		else:
			place = PlaceCreatorDatabase(i, city).create_place()

		places.append(place)

	return Places(places, city)


def _get_places_and_save_to_file(city):
	"""Function that gets places from api and saves it to file."""
	db = None
	attractions = get_places_for_city(
		db, city, PlaceCreatorAPI, PlaceVisitor, save_raw=False
	)
	with open(get_path('attractions.json', 'data'), 'w') as f:
		json.dump(attractions.get_list(), f, default=vars)
	return attractions


def get_attractions(
	db: DataBase | None, city: City, user_preferences, from_file: bool = False
) -> Places:
	"""Get attractions from database_module or create new one."""
	if from_file:
		attractions = _get_from_file(city)
		return attractions

	if db is None:
		attractions = _get_places_and_save_to_file(city)
		return attractions

	if db.check_if_city_exist(city):
		logging.info('City exist in database_module.')
		attractions = db.read_places_data_from_db(city, 'places', PlaceCreatorDatabase)

	else:
		attractions = get_places_for_city(
			db, city, placeCreator=PlaceCreatorAPI, placeVisitor=PlaceVisitor
		)

		logging.info('Created new city in database_module.')
	return attractions


def get_recommendations(
	db: DataBase,
	db_users: DataBaseUsers,
	user_id: str,
	city_id: int,
	days: int,
	dates: tuple[date, date],
	preferences: UserPreferences,
	from_file: bool = False,
):
	"""Function that returns a list of place for each day."""
	city = City(city_id)

	user = TripInfo(
		user_id=user_id, user_preferences=preferences, city=city, days=days, dates=dates
	)

	places_list = get_attractions(
		db=db, city=city, user_preferences=user, from_file=from_file
	)

	recommendation = Recommendation(places=places_list, user=user).get_recommendation()
	itinerary = recommendation.get_itinerary()
	trip_id = db_users.save_user_trip_history(user.user_id, city, itinerary)
	itinerary['id'] = trip_id
	return itinerary
