from src.backend.main import app
from src.backend.mock_trip import load_mock_trip


def test_load_mock_trip_from_sample_csv():
	trip = load_mock_trip('rome_minimal.csv')

	assert trip['city_name'] == 'Rome'
	assert trip['is_mock'] is True
	assert trip['dates'] == ['2026-07-10', '2026-07-11']
	assert len(trip['days']) == 2
	assert len(trip['days'][0]['places']) == 3
	assert trip['days'][0]['places'][1]['name'] == 'Roman Forum'
	assert trip['days'][0]['places'][1]['transportation'] == [12, 'walking']


def test_mock_trip_endpoint_returns_trip():
	client = app.test_client()

	response = client.get('/api/mock-trip?file=rome_minimal.csv')

	assert response.status_code == 200
	payload = response.get_json()
	assert payload['success'] is True
	assert payload['data']['city_name'] == 'Rome'
	assert len(payload['data']['days']) == 2
