"""Given a list of preferences and two different places, check if the place
that has more preferences in common with the list of preferences is returned,
as it is given has higher rating"""
from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import PlaceRating, AccessibilityOptions, Dining, Alcohol, Children
from src.data_model.user.user_preferences import UserPreferences
from src.rating.cumulative_rating import _calculate_cumulative_rating
from src.rating.user_preferences_rating import UserPreferencesRating








def data():
    user_needs = UserPreferences({
        "priceLevel": 1,
        "paymentOptions": False,
        "wheelchairAccessible": False,
        "goodForGroups": False,
        "vegan": False,
        "children": False,
        "alcohol": False,
        "allowsDogs": False
    }, ["museum", "park", "zoo", "church"], ["Art", "History", "Science", "War", "Maritime"])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, dining={'servesVegetarianFood': True}, alcohol={'servesBeer': True},
                   children={'isFamilyFriendly': True}, ratings=PlaceRating({"normalizedRating": 4.6}),
                   types=['museum', 'park'],
                   subcategories=['Art', 'History'], priceLevel=1, paymentOptions={'acceptsCashOnly': True,
                                                                                   'acceptsCreditCards': True,
                                                                                   'acceptsNfc': True},
                   accessibilityOptions={'wheelchairAccessible': True},
                   allowsDogs=True, goodForGroups=True)

    place2 = Place(placeInfo={'id': '2'}, dining={'servesVegetarianFood': True}, alcohol={'servesBeer': True},
                   children={'isFamilyFriendly': True}, ratings=PlaceRating({"normalizedRating": 4.6}),
                   types=['museum', 'park'],
                   subcategories=['Art', 'History'], priceLevel=1, paymentOptions={'acceptsCashOnly': True,
                                                                                   'acceptsCreditCards': True,
                                                                                   'acceptsNfc': True},
                   accessibilityOptions={'wheelchairAccessible': True},
                   allowsDogs=True, goodForGroups=True)


def test_priceLevel():
    user_needs = UserPreferences({
        "priceLevel": 1,
        "paymentOptions": False,
        "wheelchairAccessible": False,
        "goodForGroups": False,
        "vegan": False,
        "children": False,
        "alcohol": False,
        "allowsDogs": False
    }, ["museum", "park", "zoo", "church"], ["Art", "History", "Science", "War", "Maritime"])
    user_preferences_rating = UserPreferencesRating(user_needs)
    place1 = Place(placeInfo={'id': '1'}, priceLevel=1)
    place2 = Place(placeInfo={'id': '2'}, priceLevel=3)
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 > rating2


def test_accessibilityOptions():
    user_needs = UserPreferences({
        "wheelchairAccessible": True
    }, [], [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'},
                   accessibilityOptions=AccessibilityOptions(wheelchairAccessibleSeating=True))
    place2 = Place(placeInfo={'id': '2'},
                   accessibilityOptions=AccessibilityOptions(wheelchairAccessibleSeating=False))
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 > rating2


def test_alcohol():
    user_needs = UserPreferences({
        "alcohol": True
    }, [], [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, alcohol=Alcohol(servesBeer=True))
    place2 = Place(placeInfo={'id': '2'}, alcohol=Alcohol(servesBeer=False))
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 > rating2


def test_equals():
    """If user is not interested in given parameter, it should not affect the rating"""
    user_needs = UserPreferences({
        "alcohol": False
    }, [], [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, alcohol={'servesBeer': True})
    place2 = Place(placeInfo={'id': '2'}, alcohol={'servesBeer': False})
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 == rating2


def test_vegan():
    user_needs = UserPreferences({
        "vegan": True
    }, [], [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, servesVegetarianFood=True)
    place2 = Place(placeInfo={'id': '2'}, servesVegetarianFood=False)
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 > rating2


def test_goodForChildren():
    user_needs = UserPreferences({
        "children": True
    }, [], [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, children=Children(goodForChildren=True))
    place2 = Place(placeInfo={'id': '2'}, children=Children(goodForChildren=False))
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 > rating2


def test_allowsDogs():
    user_needs = UserPreferences({
        "allowsDogs": True
    }, [], [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, allowsDogs=True)
    place2 = Place(placeInfo={'id': '2'}, allowsDogs=False)
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 > rating2


def test_goodForGroups():
    user_needs = UserPreferences({
        "goodForGroups": True
    }, [], [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, goodForGroups=True)
    place2 = Place(placeInfo={'id': '2'}, goodForGroups=False)
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 > rating2


def test_categories_only_1():
    user_needs = UserPreferences({
    }, ["museum", "park", "zoo", "church"],
        [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, types=['museum', 'park'])
    place2 = Place(placeInfo={'id': '2'}, types=['museum', 'park', 'zoo'])
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 < rating2


def test_categories_only_2():
    user_needs = UserPreferences({
    }, ["museum", "park", "zoo", "church"],
        [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, types=['museum', 'park'])
    place2 = Place(placeInfo={'id': '2'}, types=['zoo', 'church'])
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 == rating2


def test_no_specified_categories():
    user_needs = UserPreferences({
    }, [], [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, types=['museum', 'park'])
    place2 = Place(placeInfo={'id': '2'}, types=['zoo', 'church'])
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 == rating2


def test_no_place_categories():
    user_needs = UserPreferences({
    }, ['museum', 'park'], [])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, types=[])
    place2 = Place(placeInfo={'id': '2'}, types=['zoo', 'church'])
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 == rating2




def test_categories_4():
    """Dla obu przykłądów da ten sam score.
    place1 ma tylko połowe wymaganych kategorii, ale atrybut gooodForChildren.
    place2 ma wszystkie wymagane kategorie, ale nie ma atrybutu goodForChildren.
    """

    user_needs = UserPreferences({
        "children": True
    }, ["museum", "park", "zoo", "church"],
        ["Art", "History", "Science", "War", "Maritime"])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, types=['museum', 'park'],
                   children=Children(goodForChildren=True))
    place2 = Place(placeInfo={'id': '2'}, types=['museum', 'park', 'zoo', 'church'])
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 == rating2


def test_categories_5():
    """place1 ma tylko połowe wymaganych kategorii, ale atrybut gooodForChildren.
    place2 ma wszystkie wymagane kategorie i kilka podkategorii, ale nie ma atrybutu goodForChildren.
    rating1=0.5, rating2=0.48
    """
    user_needs = UserPreferences({
        "children": True
    }, ["museum", "park", "zoo", "church"],
        ["Art", "History", "Science", "War", "Maritime"])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, types=['museum', 'park'],
                   children=Children(goodForChildren=True))
    place2 = Place(placeInfo={'id': '2'}, types=['museum', 'park', 'zoo', 'church'],
                   subcategories=['Art', 'History'])

    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    print(rating1, rating2)
    assert rating1 > rating2


def test_categories_vs_subcategories():
    
    user_needs = UserPreferences({
    }, ["museum", "park", "zoo", "church"],
        ["Art", "History", "Science", "War", "Maritime"])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, types=["museum", "park", "zoo", "church"])
    place2 = Place(placeInfo={'id': '2'}, subcategories=["Art", "History", "Science", "War", "Maritime"])
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    assert rating1 == rating2  


def test_categories_7():
    """
    place1 = 0.5666666666666667
    place2 = 0.3333333333333333
    :return:
    """
    
    user_needs = UserPreferences({
        'children': True,
        'alcohol': True,
        'vegan': True
    }, ["museum", "park", "zoo", "church"],
        ["Art", "History", "Science", "War", "Maritime"])

    user_preferences_rating = UserPreferencesRating(user_needs)

    place1 = Place(placeInfo={'id': '1'}, children=Children(goodForChildren=True),
                   servesVegetarianFood=True, alcohol=Alcohol(servesBeer=True))
    place2 = Place(placeInfo={'id': '2'}, types=["museum", "park", "zoo", "church"])
    rating1 = _calculate_cumulative_rating(place1, user_preferences_rating)
    rating2 = _calculate_cumulative_rating(place2, user_preferences_rating)
    print(rating1, rating2)
    assert rating1 > rating2
