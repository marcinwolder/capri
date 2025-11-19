import unittest
from unittest.mock import patch

from src.backend.utils import get_attractions
from src.open_ai.main import OpenAIClient

from src.data_model.city.city import City
from src.data_model.places.places import Places


class TestGetAttractionsForCity(unittest.TestCase):
	@patch('project.management.api_call_google.nearby_search')
	@patch('project.data_model.place.place_visitor.PlaceVisitor')
	@patch('your_module.db')
	def test_valid_city_and_categories(
		self, mock_db, mock_place_visitor, mock_nearby_search
	):
		mock_nearby_search.return_value.json.return_value = {
			'place': [{'name': 'Attraction1', 'category': 'Museum'}]
		}
		mock_place_visitor.return_value.is_suitable.return_value = True

		city = City('Test City', location='Some Location', population=100000)
		open_ai_client = OpenAIClient()

		result = get_attractions(db=mock_db, city=city, open_ai_client=open_ai_client)

		self.assertIsInstance(result, Places)
		self.assertEqual(len(result.get_list()), 1)
		mock_db.add_place_to_database.assert_called()


if __name__ == '__main__':
	unittest.main()
