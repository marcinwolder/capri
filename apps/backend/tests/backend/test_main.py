import unittest
from unittest.mock import patch

from flask_testing import TestCase
from src.backend.main import app, db


class TestGetWithTextRoute(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        
        db.create_all()

    def tearDown(self):
        
        db.session.remove()
        db.drop_all()

    
    
    def test_successful_request(self):
        with patch('project.backend.helpers.get_recommendations') as mock_get_recommendations:
            with patch('project.nlp_operations.nlp.aspect_analyzer.get_preferences_from_text_data') as mock_get_preferences:
                mock_get_preferences.return_value = {'preference1': 0.8, 'preference2': 0.6}
            mock_get_recommendations.return_value = 'Mocked Recommendations'
            response = self.client.post('/get_with_text', json={
                'text': 'Some text data',
                'user_specified_needs': 'User needs'
            })
        
        
        
        
        
        
        

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertEqual(response.json['received_data'], 'Mocked Recommendations')

    def test_invalid_data_format(self):
        response = self.client.post('/get_with_text', json={
            'wrong_key': 'Some text data'
        })

        self.assertNotEqual(response.status_code, 200)

    def test_empty_data(self):
        response = self.client.post('/get_with_text', json={})

        self.assertNotEqual(response.status_code, 200)

    


if __name__ == '__main__':
    unittest.main()
