from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import *

place1 = Place(
    placeInfo=PlaceInfo(
        id='123',
        displayName='Place1',
        formattedAddress='Address1',
        googleMapsUri='Uri1'),
    ratings=PlaceRating(
        rating=4.5,
        userRatingCount=100,
        confidenceRating=4.0),
)


def test_1():
    assert place1.ratings.rating > place1.ratings.confidenceRating


def test_confidence_rating():
    ret = confidence_rating_by_population(place1.ratings.rating, place1.ratings.userRatingCount, 1000)
    print(ret, place1.ratings.rating)
    assert ret < place1.ratings.rating


def test_confidence_rating_2():
    place1.ratings.userRatingCount = 1000
    ret = confidence_rating_by_population(place1.ratings.rating, place1.ratings.userRatingCount, 100)
    print(ret, place1.ratings.rating)
    assert ret < place1.ratings.rating

def test_confidence_rating_3():
    place1.ratings.userRatingCount = 10000
    ret = confidence_rating_by_population(place1.ratings.rating, place1.ratings.userRatingCount, 100)
    print(ret, place1.ratings.rating)
    assert ret < place1.ratings.rating

def test_confidence_rating_4():
    place1.ratings.userRatingCount = 1000000
    ret = confidence_rating_by_population(place1.ratings.rating, place1.ratings.userRatingCount, 100)
    print(ret, place1.ratings.rating)
    assert ret < place1.ratings.rating