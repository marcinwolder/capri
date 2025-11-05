import pickle

from src.api_calls import get_restaurants_for_city
from src.constants import dining
from src.data_model.city.city import City
from src.data_model.place.place_subclasses import Location
from src.data_model.place.place_visitor import PlaceVisitor
from src.data_model.places.places import Places
from src.path import get_path
from src.travel_time import travel_estimator


def get_restaurants(city_id, lat, lon, categories, vegan, alcohol):
    city = City(city_id)
    place_location = Location(lat, lon)
    
    
    
    
    restaurants: Places = pickle.load(open(get_path('restaurants.pkl', 'outputs'), "rb"))

    for restaurant in restaurants.get_list():
        restaurant.ratings.cumulative_rating = restaurant.ratings.statisticalRating
        restaurant.types = [category for category in restaurant.types if category in dining and category != 'restaurant']

    
    
    
    
    
    
    restaurant_list = restaurants.sort_by_rating().get_list()

    restaurants_itineraries = [PlaceVisitor.place_to_itinerary(restaurant, travel_estimator.get_estimated_time(
        place_location, restaurant.location, city)) for restaurant in restaurant_list
                               if restaurant.ratings.cumulative_rating > 0]

    return restaurants_itineraries
