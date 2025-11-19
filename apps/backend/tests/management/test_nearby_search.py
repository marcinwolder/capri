from unittest.mock import patch

import pytest
import responses
from src.api_calls.api_call_google import nearby_search

valid_location = (40.7128, -74.0060)
valid_included_type = 'restaurant'
valid_excluded_types = ['bar', 'cafe']
invalid_location = 'invalid_location'


@responses.activate
def test_nearby_search_valid_input():
	responses.add(
		responses.POST,
		'https://places.googleapis.com/v1/places:searchNearby',
		json={'result': 'success'},
		status=200,
	)

	response = nearby_search(valid_location, valid_included_type, valid_excluded_types)
	assert response.status_code == 200
	assert 'result' in response.json()


@patch('project.management.api_call_google.os.getenv')
def test_nearby_search_invalid_api_key(mock_getenv):
	mock_getenv.return_value = None

	ret = nearby_search(valid_location, valid_included_type, valid_excluded_types)
	assert ret.status_code == 403


def test_nearby_search_invalid_location():
	ret = nearby_search(invalid_location, valid_included_type, valid_excluded_types)
	assert ret.status_code == 400


def test_nearby_search_invalid_radius():
	ret = nearby_search(valid_location, valid_included_type, valid_excluded_types, -1)
	assert ret.status_code == 400


def test_nearby_search_success_1():
	ret = nearby_search((50.06143, 19.93658), 'restaurant', ['bar', 'cafe'])
	assert ret.status_code == 200


def test_nearby_search_success_2():
	ret = nearby_search((13.7563, 100.5018), 'restaurant', ['bar', 'cafe'])
	assert ret.status_code == 200


if __name__ == '__main__':
	pytest.main()
