"""Module that handles the connection to the database_module."""

import json
import os

from dotenv import load_dotenv
from firebase_admin import firestore, credentials, initialize_app, auth

from src.data_model import TripInfo
from src.data_model.city.city import City
from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import Location, PlaceInfo
from src.data_model.place.place_visitor import PlaceVisitor
from src.data_model.user.user import User

load_dotenv()


class DataBaseUsers:
	"""Class that handles the connection to the database_module."""

	@staticmethod
	def _load_service_account(env_name: str, file_env_name: str):
		"""Load a Firebase service account config from a JSON string or file."""
		file_path = os.getenv(file_env_name)
		if file_path:
			try:
				with open(file_path, 'r', encoding='utf-8') as file:
					return json.load(file)
			except FileNotFoundError as exc:
				raise ValueError(
					f'{file_env_name} points to a missing file: {file_path}'
				) from exc
			except json.JSONDecodeError as exc:
				raise ValueError(
					f'{file_env_name} does not point to valid JSON: {file_path}'
				) from exc

		json_blob = os.getenv(env_name)
		if json_blob:
			try:
				return json.loads(json_blob)
			except json.JSONDecodeError as exc:
				raise ValueError(f'{env_name} is not valid JSON data.') from exc

		raise ValueError(
			f'Set either {env_name} or {file_env_name} to a Firebase service account.'
		)

	def __init__(self):
		config = self._load_service_account(
			'USERS_DB_API_CONFIG', 'USERS_DB_API_CONFIG_FILE'
		)
		cred = credentials.Certificate(config)
		self.app = initialize_app(cred, name='USERS')
		self.db = firestore.client(self.app)

	def get_one_user_by_id(self, user: TripInfo):
		"""Function that reads data from the database_module
		and returns it in the form of a pandas dataframe.
		"""
		return self.db.collection('users').document(user.user_id).get().to_dict()

	def check_if_user_exist(self, user: TripInfo):
		"""Function that checks if city exist in database_module."""
		doc_ref = self.db.collection(user.user_id)
		if doc_ref.get():
			return True
		return False

	def update_user(self, user: TripInfo):
		"""Function that updates user in database_module."""
		user = user.to_json()
		user = json.loads(user)
		doc_ref = self.db.collection('users').document(user['user_id'])
		doc_ref.update(user)

	def save_user_preferences(self, user: TripInfo):
		"""Function that saves user preferences in database_module."""
		user = user.to_json()
		user = json.loads(user)
		doc_ref = self.db.collection('users').document(user['user_id'])
		doc_ref.update(user['user_preferences'])

	def save_user_trip_history(self, user_id: str, city: City, itinerary: dict) -> str:
		"""Function that saves user trip history in database_module.
		:param user_id: str
		:param city: City
		:param itinerary: list

		:rtype: str
		:return: trip_id
		"""
		itinerary = itinerary.copy()
		itinerary_days = itinerary.pop('days')
		payload = {
			'days_len': len(itinerary_days),
			'city_id': city.id,
			'city_name': city.name,
			**itinerary,
		}

		doc_ref = (
			self.db.collection('users')
			.document(user_id)
			.collection('trip_history')
			.document()
		)
		doc_ref.set(payload)
		days_collection = doc_ref.collection('days')
		for i, day in enumerate(itinerary_days):
			day_doc = days_collection.document(str(i))
			day_doc.set({'places_len': len(day['places']), 'weather': day['weather']})
			for j, place in enumerate(day['places']):
				day_doc.collection('places').document(str(j)).set({'id': place['id']})
		return doc_ref.id

	def _verify_token(self, token):
		"""Function that verifies token."""
		return auth.verify_id_token(token, app=self.app)

	@staticmethod
	def _trip_to_dict(trip_id: str, trip_doc):
		"""Function that converts trip to dict."""
		trip = trip_doc.get().to_dict()
		trip_info = {'id': trip_id, 'days': [], **trip}
		print('trip_info', trip_info)
		for i in range(trip.pop('days_len')):
			day_ref = trip_doc.collection('days').document(str(i))
			day_dict = day_ref.get().to_dict()
			if day_dict is None:
				day_dict = {'places_len': 0}
			day_dict['places'] = []
			for placeIndex in range(day_dict.pop('places_len')):
				day_dict['places'].append(
					day_ref.collection('places')
					.document(str(placeIndex))
					.get()
					.to_dict()
				)
			trip_info['days'].append(day_dict)
		print('trip_info', trip_info)
		return trip_info

	def get_user_trip(self, token: str, trip_id: str):
		"""Function that gets user trip."""
		uid = self._verify_token(token)['uid']
		trip = (
			self.db.collection('users')
			.document(uid)
			.collection('trip_history')
			.document(trip_id)
		)
		return self._trip_to_dict(trip_id, trip)

	def get_user_trip_history(self, token: str = '', user_id: str = None):
		"""Function that gets user trip history."""
		uid = user_id if user_id is not None else self._verify_token(token)['uid']
		return [
			self._trip_to_dict(doc.id, doc)
			for doc in self.db.collection('users')
			.document(uid)
			.collection('trip_history')
			.list_documents()
		]

	def get_all_users(self):
		"""Function that gets all users."""
		return [doc.to_dict() for doc in self.db.collection('users').get()]


def debug_update_user(db, user_id):
	user = TripInfo(user_id, 'user_name', 'user_email')

	print(db.check_if_user_exist(user))
	user = TripInfo(user_id, 'user_name', 'user_email2')
	db.update_user(user)
	print(db.check_if_user_exist(user))


def debug_trip_history(db, user_id):
	user = TripInfo(user_id)

	placeVIsitor = PlaceVisitor()
	place1 = Place(
		location=Location(50.06143, 19.93658), placeInfo=PlaceInfo(displayName='Hotel')
	)
	place2 = Place(
		location=Location(50.06143, 19.93658), placeInfo=PlaceInfo(displayName='Hotel2')
	)
	place1 = placeVIsitor.place_to_itinerary(place1)
	place2 = placeVIsitor.place_to_itinerary(place2)
	itinerary = {'0': [place1, place2]}

	db.save_user_trip_history(user, itinerary)
