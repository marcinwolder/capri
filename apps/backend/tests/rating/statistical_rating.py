import unittest

from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import PlaceRating, PlaceInfo
from src.data_model.places.places import Places
from src.rating.statistical_rating import StatisticalRating



def _make_places():
    return Places(
        [Place(placeInfo=PlaceInfo(id='1'),
               ratings=PlaceRating(rating=4.0,
                                   cumulative_rating=4.0,
                                   userRatingCount=50.0)),
         Place(placeInfo=PlaceInfo(id='2'),
               ratings=PlaceRating(rating=4.0,
                                   cumulative_rating=5.0,
                                   userRatingCount=4.0))
         ])


class TestStatisticalRating(unittest.TestCase):

    def setUp(self):
        self.places = _make_places()
        self.statisticalRating = StatisticalRating(self.places)
        self.statisticalRating.calculate_statistical_rating()

    def test_average_rating(self):
        rating = self.statisticalRating.average_rating
        assert rating == 4

    def test_average_rating_count(self):
        rating = self.statisticalRating.average_rating_count
        assert rating == 4.5

    def test_calculate_statistical_rating(self):
        """Place with id=1 would have higher statistical rating than Place with id=2. It's because
        Place with id=1 has higher userRatingCount=5, than Place with id=2, which has userRatingCount=4."""
        
        for place in self.places.get_list():
            print(place.ratings)
        assert (self.places.get_place_by_id('1').ratings.statisticalRating
                > self.places.get_place_by_id('2').ratings.statisticalRating)
