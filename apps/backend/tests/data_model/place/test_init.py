import unittest

from src.data_model import PlaceFromAPI
from src.data_model.city.city import City


class TestPlaceInit(unittest.TestCase):
    def test_init_with_full_data(self):
        data = {
            'name': 'Example Place',
            'id': '123',
            'formattedAddress': '123 Example Street',
            'googleMapsUri': 'http://example.com',
            'websiteUri': 'http://example.com',
            'iconMaskBaseUri': 'http://example.com',
            'displayName': 'Example Place',
            'businessStatus': 'OPERATIONAL',
            'primaryType': 'restaurant',
            'location': {'latitude': 12.34, 'longitude': 56.78},
            
        }
        place = PlaceFromAPI(data, city=City.get_const_krakow())
        self.assertEqual(place.name, 'Example Place')
        self.assertEqual(place.id, '123')
        

    def test_init_with_partial_data(self):
        data = {
            'name': 'Example Place',
            'id': '123',
            'location': {'latitude': 12.34, 'longitude': 56.78},
            
        }
        place = PlaceFromAPI(data, city=City.get_const_krakow())
        self.assertEqual(place.name, 'Example Place')
        self.assertEqual(place.id, '123')
        self.assertEqual(place.formatted_address, '')  
        

    
    
    
    
        

    def test_missing_fields(self):
        data = {
            
            'name': 'Example Place',
            'id': '123',
            'location': {'latitude': 12.34, 'longitude': 56.78},
        }
        place = PlaceFromAPI(data, city=City.get_const_krakow())
        self.assertIsNotNone(place.location)  
        

    def test_invalid_data_types(self):
        data = {
            'name': 123,  
            'id': '123',
            'location': {'latitude': 12.34, 'longitude': 56.78},
        }
        with self.assertRaises(TypeError):
            place = PlaceFromAPI(data, city=City.get_const_krakow())
            

    




if __name__ == '__main__':
    unittest.main()
