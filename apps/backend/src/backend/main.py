import logging
import os
import re
from datetime import datetime

from flask import Flask, Response, jsonify, request
from flask_cors import CORS, cross_origin
import requests

from src.backend.get_recommendation import get_recommendations
from src.backend.get_recommendation_wibit import get_recommendations_wibit
from src.backend.get_trip_history import (
	get_trip,
	get_trip_history,
	get_trip_history_overview,
)
from src.data_model import UserPreferences
from src.database import DataBase, DataBaseTrips
from src.api_calls.llama import Llama

app = Flask(__name__)
# Allow Angular dev server plus Electron's ephemeral 127.0.0.1:<random-port> origin.
ALLOWED_ORIGINS = ['http://localhost:4200', r'http://127\.0\.0\.1:\d+']
CORS(app, resources={r'/api/*': {'origins': ALLOWED_ORIGINS}})

db = DataBase()
db_trips = DataBaseTrips()


@app.route('/api/health', methods=['GET'])
def health_check():
	return jsonify({'success': True}), 200


@app.route('/api/trip-history', methods=['GET'])
def trip_history():
	try:
		trips = get_trip_history(db, db_trips)
		return jsonify({'success': True, 'data': trips}), 200
	except Exception as exc:
		logging.exception(exc)
		return jsonify({'success': False, 'message': str(exc)}), 500


@app.route('/api/trip-history/overview', methods=['GET'])
def trip_history_overview():
	try:
		trips = get_trip_history_overview(db_trips)
		return jsonify({'success': True, 'data': trips}), 200
	except Exception as exc:
		logging.exception(exc)
		return jsonify({'success': False, 'message': str(exc)}), 500


@app.route('/api/trip-history/<trip_id>', methods=['GET'])
def trip_details(trip_id: str):
	try:
		trip = get_trip(
			db,
			db_trips,
			trip_id,
		)
		return jsonify(
			{
				'success': True,
				'data': trip,
			}
		), 200
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify(
			{
				'success': False,
				'message': str(e),
			}
		), 500


@app.route('/api/trip-history/<trip_id>/rating', methods=['POST'])
def rate_trip(trip_id: str):
	data = request.json or {}
	try:
		day_index = int(data.get('day_index'))
		place_index = int(data.get('place_index'))
		rating = float(data.get('rating'))
	except Exception as exc:
		return jsonify({'success': False, 'message': f'Invalid payload: {exc}'}), 400

	try:
		db_trips.set_trip_rating(trip_id, day_index, place_index, rating)
		return jsonify({'success': True}), 200
	except Exception as exc:
		logging.exception(exc)
		return jsonify({'success': False, 'message': str(exc)}), 500


@app.route('/api/trip-history/<trip_id>', methods=['DELETE'])
def delete_trip(trip_id: str):
	try:
		db_trips.delete_trip(trip_id)
		return jsonify({'success': True}), 200
	except Exception as exc:
		logging.exception(exc)
		return jsonify({'success': False, 'message': str(exc)}), 500


@app.route('/api/trip-history/batch-delete', methods=['POST'])
def delete_trips_batch():
	data = request.json or {}
	trip_ids = data.get('trip_ids')
	if not isinstance(trip_ids, list) or not trip_ids:
		return jsonify({'success': False, 'message': 'trip_ids must be a non-empty list.'}), 400
	try:
		deleted_ids, missing_ids = db_trips.delete_trips(trip_ids)
		if missing_ids:
			return jsonify(
				{
					'success': False,
					'deleted_ids': [],
					'missing_ids': missing_ids,
					'errors': ['Some trips were not found; no trips were deleted.'],
				}
			), 404
		return jsonify({'success': True, 'deleted_ids': deleted_ids}), 200
	except Exception as exc:
		logging.exception(exc)
		return jsonify(
			{
				'success': False,
				'deleted_ids': [],
				'errors': [str(exc)],
			}
		), 500


@app.route('/api/recommendation/preferences', methods=['POST'])
@cross_origin(
	origins=ALLOWED_ORIGINS,
	allow_headers=['Content-Type', 'Authorization'],
)
def get_with_categories():
	"""Create recommendation from structured preferences."""
	data = request.json

	if not data:
		return jsonify({'status': 'error', 'message': 'No data in the request'})

	categories = [category for category in data['preferences']['categories'].keys()]
	subcategories = data['preferences']['categories']
	dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in data['dates']]
	dates_tuple = (dates[0], dates[1])

	user_specified_needs = UserPreferences(
		data['preferences']['money'],
		categories,
		subcategories,
		data['preferences']['needs'],
	)
	try:
		recommendation = get_recommendations(
			db,
			db_trips,
			data['city_id'],
			data['days'],
			dates_tuple,
			user_specified_needs,
		)
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify({'status': 'error', 'received_data': e.__str__()})

	return jsonify({'status': 'success', 'received_data': recommendation})


@app.route('/api/recommendation/wibit/preferences', methods=['POST'])
@cross_origin(
	origins=ALLOWED_ORIGINS,
	allow_headers=['Content-Type', 'Authorization'],
)
def get_with_categories_wibit():
	data = request.json

	if not data:
		return jsonify({'status': 'error', 'message': 'No data in the request'})

	categories = [category for category in data['preferences']['categories'].keys()]
	subcategories = data['preferences']['categories']
	dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in data['dates']]
	dates_tuple = (dates[0], dates[1])

	user_specified_needs = UserPreferences(
		data['preferences']['money'],
		categories,
		subcategories,
		data['preferences'].get('restaurant_categories', []),
		data['preferences'].get('needs', []),
	)
	try:
		recommendation = get_recommendations_wibit(
			db,
			db_trips,
			data['city_id'],
			data['days'],
			dates_tuple,
			user_specified_needs,
		)
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify({'status': 'error', 'received_data': e.__str__()})

	return jsonify({'status': 'success', 'received_data': recommendation})


def _build_recommendation_from_free_text(data: dict, use_wibit: bool):
	categories = [category for category in data['preferences']['categories'].keys()]
	subcategories = data['preferences']['categories']
	dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in data['dates']]
	dates_tuple = (dates[0], dates[1])
	user_specified_needs = UserPreferences(
		data['preferences']['money'],
		categories,
		subcategories,
		data['preferences'].get('restaurant_categories', []),
		data['preferences'].get('needs', []),
	)
	if use_wibit:
		return get_recommendations_wibit(
			db,
			db_trips,
			data['city_id'],
			data['days'],
			dates_tuple,
			user_specified_needs,
		)
	return get_recommendations(
		db,
		db_trips,
		data['city_id'],
		data['days'],
		dates_tuple,
		user_specified_needs,
	)


@app.route('/api/recommendation/messages', methods=['POST'])
@cross_origin(
	origins=ALLOWED_ORIGINS,
	allow_headers=['Content-Type', 'Authorization'],
)
def get_with_messages():
	data = request.json
	if not data:
		return jsonify({'status': 'error', 'message': 'No data in the request'})
	preferences = Llama.get_preferences_from_messages(data.get('preferences', []))
	data['preferences'] = preferences
	try:
		recommendation = _build_recommendation_from_free_text(data, use_wibit=False)
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify({'status': 'error', 'received_data': e.__str__()})
	return jsonify({'status': 'success', 'received_data': recommendation})


@app.route('/api/recommendation/note', methods=['POST'])
@cross_origin(
	origins=ALLOWED_ORIGINS,
	allow_headers=['Content-Type', 'Authorization'],
)
def get_with_note():
	data = request.json
	if not data:
		return jsonify({'status': 'error', 'message': 'No data in the request'})
	preferences = Llama.get_preferences_from_text(data.get('preferences', ''))
	data['preferences'] = preferences
	try:
		recommendation = _build_recommendation_from_free_text(data, use_wibit=False)
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify({'status': 'error', 'received_data': e.__str__()})
	return jsonify({'status': 'success', 'received_data': recommendation})


@app.route('/api/recommendation/wibit/messages', methods=['POST'])
@cross_origin(
	origins=ALLOWED_ORIGINS,
	allow_headers=['Content-Type', 'Authorization'],
)
def get_with_messages_wibit():
	data = request.json
	if not data:
		return jsonify({'status': 'error', 'message': 'No data in the request'})
	preferences = Llama.get_preferences_from_messages(data.get('preferences', []))
	data['preferences'] = preferences
	try:
		recommendation = _build_recommendation_from_free_text(data, use_wibit=True)
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify({'status': 'error', 'received_data': e.__str__()})
	return jsonify({'status': 'success', 'received_data': recommendation})


@app.route('/api/recommendation/wibit/note', methods=['POST'])
@cross_origin(
	origins=ALLOWED_ORIGINS,
	allow_headers=['Content-Type', 'Authorization'],
)
def get_with_note_wibit():
	data = request.json
	if not data:
		return jsonify({'status': 'error', 'message': 'No data in the request'})
	preferences = Llama.get_preferences_from_text(data.get('preferences', ''))
	data['preferences'] = preferences
	try:
		recommendation = _build_recommendation_from_free_text(data, use_wibit=True)
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify({'status': 'error', 'received_data': e.__str__()})
	return jsonify({'status': 'success', 'received_data': recommendation})


PLACES_PHOTO_PATTERN = re.compile(r'^places/[^/]+/photos/[^/]+$')
DEFAULT_MAX_DIMENSION = 400
MAX_ALLOWED_DIMENSION = 1600
GOOGLE_PLACES_MEDIA_URL = 'https://places.googleapis.com/v1/{name}/media'
GOOGLE_REQUEST_TIMEOUT = (5, 10)  # (connect, read)


def _parse_dimension(param_value: str | None, param_name: str) -> int:
	if param_value is None or param_value == '':
		return DEFAULT_MAX_DIMENSION
	try:
		value = int(param_value)
	except (TypeError, ValueError):
		raise ValueError(f'{param_name} must be an integer.')
	if value <= 0:
		raise ValueError(f'{param_name} must be a positive integer.')
	if value > MAX_ALLOWED_DIMENSION:
		raise ValueError(f'{param_name} must be <= {MAX_ALLOWED_DIMENSION}.')
	return value


def _extract_google_error_message(response: requests.Response) -> str:
	try:
		data = response.json()
		if isinstance(data, dict):
			if 'error' in data and isinstance(data['error'], dict):
				if 'message' in data['error']:
					return str(data['error']['message'])
			if 'message' in data:
				return str(data['message'])
	except ValueError:
		pass
	text = response.text.strip()
	return text or 'Google Places API error.'


@app.route('/api/places/photos/<path:name>', methods=['GET'])
def get_place_photo(name: str):
	if not PLACES_PHOTO_PATTERN.match(name):
		return jsonify({'success': False, 'message': 'Invalid photo name format.'}), 400
	try:
		max_height = _parse_dimension(request.args.get('maxHeightPx'), 'maxHeightPx')
		max_width = _parse_dimension(request.args.get('maxWidthPx'), 'maxWidthPx')
	except ValueError as exc:
		return jsonify({'success': False, 'message': str(exc)}), 400

	api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
	if not api_key:
		return jsonify(
			{'success': False, 'message': 'GOOGLE_PLACES_API_KEY not configured.'}
		), 500

	url = GOOGLE_PLACES_MEDIA_URL.format(name=name)
	params = {'maxHeightPx': max_height, 'maxWidthPx': max_width}
	headers = {'X-Goog-Api-Key': api_key}

	try:
		google_response = requests.get(
			url,
			params=params,
			headers=headers,
			stream=True,
			timeout=GOOGLE_REQUEST_TIMEOUT,
		)
	except requests.Timeout:
		return jsonify(
			{'success': False, 'message': 'Request to Google Places timed out.'}
		), 504
	except requests.RequestException as exc:  # network or other transport errors
		return jsonify({'success': False, 'message': str(exc)}), 502

	if not google_response.ok:
		message = _extract_google_error_message(google_response)
		return jsonify(
			{'success': False, 'message': message}
		), google_response.status_code

	content_type = google_response.headers.get('Content-Type', '').lower()
	if not content_type.startswith('image/'):
		google_response.close()
		return jsonify(
			{'success': False, 'message': 'Google Places did not return an image.'}
		), 502

	def generate():
		for chunk in google_response.iter_content(chunk_size=8192):
			if chunk:
				yield chunk
		google_response.close()

	response_headers = {
		'Content-Type': content_type,
		'Cache-Control': 'public, max-age=86400',
	}
	content_length = google_response.headers.get('Content-Length')
	if content_length:
		response_headers['Content-Length'] = content_length

	return Response(
		generate(), headers=response_headers, status=google_response.status_code
	)
