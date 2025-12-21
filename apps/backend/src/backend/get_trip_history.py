from src.data_model.city.city import City
from src.data_model.place.place_visitor import PlaceVisitor
from src.database import DataBase, DataBaseTrips


def get_trip(db: DataBase, db_trips: DataBaseTrips, trip_id: str):
	trip = db_trips.get_trip(trip_id)
	for day in trip['days']:
		for i, place in enumerate(day['places']):
			city = City(trip['city_id'])
			full_place = db.get_place(city, place['id'])
			day['places'][i] = {**PlaceVisitor.place_to_itinerary(full_place), **place}
	return trip


def get_trip_history(db: DataBase, db_trips: DataBaseTrips):
	trip_history = db_trips.get_trip_history()
	for i, trip in enumerate(trip_history):
		trip_history[i] = get_trip(db, db_trips, trip['id'])
	return trip_history
