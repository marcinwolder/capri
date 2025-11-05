
from unittest.mock import patch

from src.data_model.city.city import City
from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import PlaceInfo
from src.data_model.places.places import Places


def _make_restaurants():
    restaurants = []
    for i in range(5):
        restaurant = Place(placeInfo=PlaceInfo(id=f'restaurant{i}', displayName=f'restaurant{i}'),
                           estimatedTime=60)
        
        
        
        restaurants.append(restaurant)
    return Places(restaurants)


def _make_user_preferences():
    return {
        "wheelchair_accessible": True,
        "family_friendly": False,
        "allowsDogs": True,
        "outdoor": True,
        "price_level": 1,
        "goodForGroups": True,
        "vegan": True,
        "children": True,
        "alcohol": True
    }


def _make_user_info():
    return {
        "days": 1,
        "categories": {"museum": ["Art", "History", "Science", "War", "Maritime"],
                       "park": [], "zoo": [], "church": [],
                       },
        "restaurant": ["Polish", "Italian", "French", "Asian", "American"],
        "city_id": City.get_const_krakow(),
        'use_saved_preferences': False,  
        "user_preferences": _make_user_preferences(),
        "user_id": "user_id",
        "location": {"latitude": 50.06143, "longitude": 19.93658}
    }


def test_get_ratings():
    with (patch('src.rating.restaurants.Rating.get_ratings') as
          mock_get_ratings):
        mock_get_ratings.return_value = 4.5
        restaurants = _make_restaurants()
        ratings = restaurants.get_ratings()

        assert ratings == {'restaurant1': 4.5, 'restaurant2': 4.5, 'restaurant3': 4.5, 'restaurant4': 4.5}




def test_get_prices():
    with (patch('src.rating.restaurants.Price.get_prices') as
          mock_get_prices):
        mock_get_prices.return_value = 2
        restaurants = _make_restaurants()
        prices = restaurants.get_prices()

        assert prices == {'restaurant1': 2, 'restaurant2': 2, 'restaurant3': 2, 'restaurant4': 2}


