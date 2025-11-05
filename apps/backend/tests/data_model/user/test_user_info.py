from src.data_model.city.city import City
from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import *
from src.data_model.user.user_info import TripInfo
from src.data_model.user.user_preferences import UserPreferences


def test_user_info():
    user_info = TripInfo(user_id="1", location={"lat": 1, "lng": 2},
                         user_preferences=UserPreferences({
                             "priceLevel": 1,
                             "wheelchairAccessible": False,
                             "goodForGroups": False,
                             "vegan": False,
                             "children": False,
                             "alcohol": False,
                             "allowsDogs": False
                         },
                             categories=[], subcategories=[]
                         ), city=City(_id=City.get_const_krakow().id),
                         days=1)
    assert user_info.user_id == "1"
    assert user_info.location == {"lat": 1, "lng": 2}
    assert user_info.user_preferences == UserPreferences({
        "priceLevel": 1,
        "wheelchairAccessible": False,
        "goodForGroups": False,
        "vegan": False,
        "children": False,
        "alcohol": False,
        "allowsDogs": False
    }
        , categories=[], subcategories=[])
    assert user_info.city == City(_id=City.get_const_krakow().id)
    assert user_info.days == 1
    assert user_info.hotel == Place(placeInfo=PlaceInfo(displayName="Hotel"),
                                    location=Location(
                                        latitude=50.0614, longitude=19.9372),
                                    regularOpeningHours=RegularOpeningHours(
                                        periods=[Period(open=TimePoint(), close=TimePoint(23)) for _ in range(7)],
                                        weekdayDescriptions=['']),
                                    estimatedTime=0)

    assert user_info.to_json() == ({
        "user_id": "1",
        "location": {"lat": 1, "lng": 2},
        "user_preferences": {
            "priceLevel": 1,
            "wheelchairAccessible": False,
            "goodForGroups": False,
            "vegan": False,
            "children": False,
            "alcohol": False,
            "allowsDogs": False,
            "restaurant": []
        },
        "city": {"name": "Krakow", "lat": 50.0614, "lng": 19.9372},
        "days": 1
    })

    assert user_info.to_dict() == {
        "user_id": "1",
        "location": {"lat": 1, "lng": 2},
        "user_preferences": {
            "priceLevel": 1,
            "wheelchairAccessible": False,
            "goodForGroups": False,
            "vegan": False,
            "children": False,
            "alcohol": False,
            "allowsDogs": False,
            "restaurant": []
        },
        "city": {"name": "Krakow", "lat": 50.0614, "lng": 19.9372},
        "days": 1
    }
    assert user_info._init_hotel() == Place(placeInfo=PlaceInfo(displayName="Hotel"),
                                            location=Location(
                                                latitude=50.0614, longitude=19.9372),
                                            regularOpeningHours=RegularOpeningHours(
                                                periods=[Period(open=TimePoint(), close=TimePoint(23)) for _ in
                                                         range(7)],
                                                weekdayDescriptions=['']),
                                            estimatedTime=0)
