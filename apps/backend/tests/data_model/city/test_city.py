import unittest

from src.data_model.city.city import City


class TestCity(unittest.TestCase):

    def setUp(self):
        self.city = City(_id=1616172264)

    def test_id(self):
        assert self.city.id == 1616172264

    def test_name(self):
        assert self.city.name == 'Kraków'

    def test_country(self):
        assert self.city.country == 'Poland'

    def test_population(self):
        assert self.city.population == 800653.0

    def test_lat(self):
        assert self.city.lat == 50.0614

    def test_lng(self):
        assert self.city.lng == 19.9372

    def test_get_radius(self):
        assert self.city.get_radius() == 15000

    def test_str(self):
        assert str(self.city) == "City: Kraków, Poland, 50.0614, 19.9372, 1616172264, 800653.0"

    def test_repr(self):
        assert repr(self.city) == "City: Kraków, Poland, 50.0614, 19.9372, 1616172264, 800653.0"

    def test_to_json(self):
        assert self.city.to_json() == ('{"name": "Krak\\u00f3w", "country": "Poland", "lat": 50.0614, "lng": '
                                       '19.9372, "id": 1616172264, "population": 800653.0}')

    def test_to_dict(self):
        assert self.city.to_dict() == {'country': 'Poland',
                                       'id': 1616172264,
                                       'lat': 50.0614,
                                       'lng': 19.9372,
                                       'name': 'Kraków',
                                       'population': 800653.0}

    def test_get_const_krakow(self):
        assert City.get_const_krakow().id


if __name__ == '__main__':
    test = TestCity()
