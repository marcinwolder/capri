from datetime import date
from typing import Tuple

from src.backend.get_recommendation import get_attractions
from src.data_model.city.city import City
from src.data_model.user.user_info import TripInfo
from src.data_model.user.user_preferences import UserPreferences
from src.database import DataBase, DataBaseTrips
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
	return itinerary
