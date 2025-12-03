import logging
import os
import re
from datetime import datetime

from firebase_admin import auth
from flask import Flask, Response, jsonify, request
from flask_cors import CORS, cross_origin
import requests

from src.backend.get_recommendation import get_recommendations
from src.backend.get_user_trip_history import get_user_trip
from src.data_model import UserPreferences
from src.database import DataBase, DataBaseUsers

app = Flask(__name__)
# Allow Angular dev server plus Electron's ephemeral 127.0.0.1:<random-port> origin.
ALLOWED_ORIGINS = ['http://localhost:4200', r'http://127\.0\.0\.1:\d+']
CORS(app, resources={r'/api/*': {'origins': ALLOWED_ORIGINS}})

db = DataBase()
db_users = DataBaseUsers()


@app.route('/api/trip-history/<trip_id>', methods=['GET'])
def trip_details(trip_id: str):
	token: str = request.headers.get('Authorization', '').split('Bearer ')[1]
	try:
		trip = get_user_trip(
			db,
			db_users,
			token,
			trip_id,
		)
		print('\n' * 4, trip)
		return jsonify(
			{
				'success': True,
				'data': trip,
			}
		), 200
	except auth.InvalidIdTokenError:
		logging.exception('Invalid token')
		return jsonify(
			{
				'success': False,
				'message': 'Unauthorized',
			}
		), 401
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify(
			{
				'success': False,
				'message': str(e),
			}
		), 500


@app.route('/api/recommendation/preferences', methods=['POST'])
@cross_origin(
	origins=ALLOWED_ORIGINS,
	allow_headers=['Content-Type', 'Authorization'],
)
def get_with_categories():
	"""Check if loc exist in firebase db"""
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
			db_users,
			data['user_id'],
			data['city_id'],
			data['days'],
			dates_tuple,
			user_specified_needs,
		)
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
