import logging
from datetime import date
from typing import Tuple

from src.backend.get_recommendation import get_attractions
from src.data_model.city.city import City
from src.data_model.user.user_info import TripInfo
from src.data_model.user.user_preferences import UserPreferences
from src.database import DataBase, DataBaseTrips
from src.metrics import build_trip_day_metrics, weekday_indices_from_dates, write_trip_metrics_csv
from src.recommendation_wibit import recommend_itinerary


def get_recommendations_wibit(
	db: DataBase,
	db_trips: DataBaseTrips,
	city_id: int,
	days: int,
	dates: Tuple[date, date],
	preferences: UserPreferences,
	from_file: bool = False,
):
	city = City(city_id)
	user = TripInfo(
		user_id='global', user_preferences=preferences, city=city, days=days, dates=dates
	)
	places_list = get_attractions(
		db=db, city=city, user_preferences=user, from_file=from_file
	)

	itinerary = recommend_itinerary(places_list, preferences, dates, city.name)
	trip_id = db_trips.save_trip_history(city, itinerary)
	itinerary['id'] = trip_id
	itinerary['city_name'] = city.name
	itinerary['city_id'] = str(city.id)
	try:
		places_by_id = {place.placeInfo.id: place for place in places_list.get_list()}
		places_by_day = []
		for day in itinerary.get('days', []):
			day_places = []
			for place in day.get('places', []):
				place_obj = places_by_id.get(place.get('id'))
				if place_obj is not None:
					day_places.append(place_obj)
			places_by_day.append(day_places)
		day_metrics = build_trip_day_metrics(
			places_by_day,
			preferences,
			weekday_indices_from_dates(dates[0], dates[1]),
			city=city,
			day_start_minutes=9 * 60,
			day_end_minutes=17 * 60,
		)
		write_trip_metrics_csv(trip_id, day_metrics)
	except Exception as exc:
		logging.exception('Failed to log trip metrics: %s', exc)
	return itinerary
