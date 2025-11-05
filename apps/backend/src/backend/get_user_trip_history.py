from src.data_model.city.city import City
from src.data_model.place.place_visitor import PlaceVisitor
from src.database import DataBaseUsers, DataBase


def get_user_trip(db: DataBase, db_users: DataBaseUsers, token: str, trip_id: str):
    trip = db_users.get_user_trip(token, trip_id)
    print(trip)
    for day in trip['days']:
        print(day)
        for i, place in enumerate(day['places']):
            print(place)
            city = City(trip['city_id'])
            full_place = db.get_place(city, place['id'])
            day['places'][i] = {**PlaceVisitor.place_to_itinerary(full_place), **place}
    return trip


def get_user_trip_history(db: DataBase, db_users: DataBaseUsers, token: str):
    trip_history = db_users.get_user_trip_history(token)
    trips = []
    for i, trip in enumerate(trip_history):
        trip_history[i] = get_user_trip(db, db_users, token, trip['id'])
    return trips
