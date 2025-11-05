import unittest

from src.data_model import PlaceFromAPI
from src.data_model.city.city import City
from src.data_model.place.place_visitor import PlaceVisitor
from src.constants import excluded_categories


class TestCheckTypes(unittest.TestCase):
    def test_check_types(self):
        place = PlaceFromAPI(data={
            'types': ['restaurant', 'cafe'],
            'primaryType': 'restaurant'
        }, city=City.get_const_krakow())
        self.assertTrue(PlaceVisitor._check_types(place))

        place.types = excluded_categories[0]
        self.assertFalse(PlaceVisitor._check_types(place))

        place.types = None
        self.assertFalse(PlaceVisitor._check_types(place))

        place.types = []
        self.assertFalse(PlaceVisitor._check_types(place))

        place.types = ['restaurant', 'cafe']
        place.primary_type = None
        self.assertFalse(PlaceVisitor._check_types(place))

        place.types = ['restaurant', 'cafe']
        place.primary_type = ''
        self.assertFalse(PlaceVisitor._check_types(place))

    
    
    
    
    
    
    
    
    
    
    
    


class TestCheckIsSuitable(unittest.TestCase):

    def test_check_is_suitable(self):
        place = PlaceFromAPI(data={
            'types': ['restaurant', 'cafe'],
            'primaryType': 'restaurant',
            'rating': 4.0,
            'businessStatus': 'OPERATIONAL',
            'userRatingCount': 100
        },city=City.get_const_krakow())
        self.assertTrue(PlaceVisitor.is_suitable(place, 1000))

        place.rating = None
        self.assertFalse(PlaceVisitor.is_suitable(place, 1000))

        place.rating = 4.0
        place.business_status = 'CLOSED_PERMANENTLY'
        self.assertFalse(PlaceVisitor.is_suitable(place, 1000))

        place.business_status = 'OPERATIONAL'
        place.user_rating_count = 9
        self.assertFalse(PlaceVisitor.is_suitable(place, 1000))

        place.user_rating_count = 100
        place.rating = 3.0
        self.assertFalse(PlaceVisitor.is_suitable(place, 1000))

        place.rating = 4.0
        place.types = excluded_categories[0]
        self.assertFalse(PlaceVisitor.is_suitable(place, 1000))

        place.types = None
        self.assertFalse(PlaceVisitor.is_suitable(place, 1000))

        place.types = []
        self.assertFalse(PlaceVisitor.is_suitable(place, 1000))

        place.types = ['restaurant', 'cafe']
        place.primary_type = None
        self.assertFalse(PlaceVisitor.is_suitable(place, 1000))

        place.types = ['restaurant', 'cafe']
        place.primary_type = ''
        self.assertFalse(PlaceVisitor.is_suitable(place, 1000))


if __name__ == '__main__':
    unittest.main()
