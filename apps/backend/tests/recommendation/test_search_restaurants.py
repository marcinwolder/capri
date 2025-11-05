from typing import List
from unittest.mock import patch

from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import PlaceInfo
from src.data_model.places.places import Places
from src.data_model.user.user_info import TripInfo
from src.data_model.user.user_preferences import UserPreferences
from src.recommendation import Recommendation

breakfast_time = 60 * 8
coffee_time = 60 * 10
lunch_time = 60 * 13
dinner_time = 60 * 18
bar_time = 60 * 20
eating_list = [breakfast_time, coffee_time, lunch_time, dinner_time, bar_time]


def _make_places():
    places = []
    for i in range(5):
        place = Place(placeInfo=PlaceInfo(id=f'place{i}', displayName=f'place{i}'),
                      estimatedTime=60)
        places.append(place)
    return Places(places)


def _make_restaurants():
    places = []
    for i in range(5):
        print(f'restaurant{i}')
        place = Place(placeInfo=PlaceInfo(id=f'restaurant{i}', displayName=f'restaurant{i}'),
                      estimatedTime=60)
        places.append(place)
    return Places(places)


def _restaurants() -> List[Places]:
    places = []
    for i in range(5):
        print(f'restaurant{i}')
        place = Place(placeInfo=PlaceInfo(id=f'restaurant{i}', displayName=f'restaurant{i}'),
                      estimatedTime=60)
        places.append(Places([place]))
    return places


def _make_user_preferences():
    userInfo = TripInfo(
        category_preferences={'museum': 5, 'restaurant': 3, 'park': 2, 'church': 1},
        user_preferences=UserPreferences
        (needs={'priceLevel': 1, 'paymentOptions': False, 'wheelchairAccessible': False,
               'goodForGroups': False, 'vegan': False, 'children': False, 'alcohol': False,
               'allowsDogs': False, 'restaurant': []},
         categories=['museum', 'restaurant', 'park', 'church'],
         subcategories=['art', 'history', 'modern', 'fastfood', 'traditional', 'bar']),

        days=3)
    return userInfo


def test_search_restaurants():
    routes = _make_places()
    restaurants = _make_restaurants()
    with patch('src.recommendation.recommendation.get_restaurants_for_city'
               ) as mock_get_restaurants_for_city:
        with patch('src.data_model.places.places.Places.get_time') as mock_get_time:
            mock_get_time.return_value = (480, {'place1': 480, 'place2': 600,
                                                'place3': 780, 'place4': 1080})
            mock_get_restaurants_for_city.side_effect = _restaurants()
            recommendation = Recommendation(routes, _make_user_preferences())
            ret = recommendation.search_restaurants(routes)
            assert ret.get_list() == restaurants.get_list()
