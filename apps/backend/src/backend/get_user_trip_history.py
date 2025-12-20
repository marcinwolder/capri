from src.data_model.city.city import City
from src.data_model.place.place_visitor import PlaceVisitor
from src.database import DataBase, DataBaseUsers


def get_user_trip(db: DataBase, db_users: DataBaseUsers, user_id: str, trip_id: str):
	trip = db_users.get_user_trip(user_id, trip_id)
	for day in trip['days']:
		for i, place in enumerate(day['places']):
			city = City(trip['city_id'])
			full_place = db.get_place(city, place['id'])
			day['places'][i] = {**PlaceVisitor.place_to_itinerary(full_place), **place}
	return trip


def get_user_trip_history(db: DataBase, db_users: DataBaseUsers, user_id: str):
	trip_history = db_users.get_user_trip_history(user_id)
	for i, trip in enumerate(trip_history):
		trip_history[i] = get_user_trip(db, db_users, user_id, trip['id'])
	return trip_history
