import unittest

from src.data_model import PlaceFromAPI
from src.data_model.city.city import City


class TestIsSuitable(unittest.TestCase):
    def test_is_suitable(self):
        place = PlaceFromAPI(data={
            
            'rating': 4.5,
            'businessStatus': 'OPERATIONAL',
            'userRatingCount': 100,
            
        }, city=City.get_const_krakow())
        self.assertTrue(place.is_suitable(population=1000))

        place.rating = 2.5
        self.assertFalse(place.is_suitable(population=1000))
        


if __name__ == '__main__':
    unittest.main()
