"""Module that handles the connection to the database_module."""

import json
import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

from src.constants import default_categories, dining
from src.data_model import Places
from src.data_model.city.city import City
from src.data_model.place.place import Place, PlaceCreator, PlaceCreatorDatabase
from src.data_model.place.place_subclasses import PlaceInfo

load_dotenv()


class DataBase:
	"""Class that handles the connection to the database_module."""

	app: firebase_admin.App
	db: firestore.client

	def __init__(self):
		self._init_client()
		self._categories = default_categories
		self._dining = dining

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

	@classmethod
	def _init_client(cls):
		"""Function that initializes the connection to the database_module."""
		config = cls._load_service_account(
			'PLACES_DB_API_CONFIG', 'PLACES_DB_API_CONFIG_FILE'
		)
		cred = credentials.Certificate(config)
		cls.app = firebase_admin.initialize_app(cred, name='PLACES')
		cls.db = firestore.client(cls.app)

	def add_place_to_database(
		self,
		place: Place,
		city: City,
		category_type: str,
		place_type: str,
		categories: list[str],
	):
		"""Function that saves data to the database_module."""
		place_dict = json.loads(place.to_json())
		doc_ref = (
			self.db.collection(city.country)
			.document(str(city.id))
			.collection(place_type)
			.document(str(place.placeInfo.id))
		)
		doc_ref.set(place_dict)

		for i in place.types:
			if categories.count(i) == 0:
				continue
			doc_ref_category = (
				self.db.collection(city.country)
				.document(str(city.id))
				.collection(category_type)
				.document(i)
			)

	def add_categories_to_database(
		self, city, category_type: str, categories: list[str]
	):
		"""Function that adds categories to the database_module."""
		for category in categories:
			doc_ref_category = (
				self.db.collection(city.country)
				.document(str(city.id))
				.collection(category_type)
			).document(category)
			doc_ref_category.set(
				{
					'ids': [],
				}
			)

	def read_places_data_from_db(
		self, city, place_type: str, placeCreator: type[PlaceCreator]
	) -> Places:
		"""Function that reads data from the database_module and
		returns it in the form of a pandas dataframe.
		"""
		doc_ref = (
			self.db.collection(city.country)
			.document(str(city.id))
			.collection(place_type)
		)
		places = []
		for i in doc_ref.get():
			i = i.to_dict()
			place = placeCreator(i, city).create_place()
			places.append(place)

		return Places(places, city)

	def check_if_city_exist(self, city):
		"""Function that checks if city exist in database_module."""
		doc_ref = (
			self.db.collection(city.country).document(str(city.id)).collection('places')
		)
		if doc_ref.get():
			return True
		return False

	def get_all_places(self, city, place_type: str):
		"""Function that returns all places from the database_module."""
		doc_ref = (
			self.db.collection(city.country)
			.document(str(city.id))
			.collection(place_type)
		)
		places = []
		for i in doc_ref.get():
			i = i.to_dict()
			places.append(i)
		return places

	def get_place(self, city, place_id: str):
		"""Function that returns one place from the database_module."""
		doc_ref = (
			self.db.collection(city.country)
			.document(str(city.id))
			.collection('places')
			.document(place_id)
		)
		return PlaceCreatorDatabase(doc_ref.get().to_dict(), city).create_place()


def debug():
	city = City(1705104301)
	place = Place(PlaceInfo(id='1'))
	db = DataBase()
	db.update_place(place, city, 'categories', 'places', default_categories)
	ret = db.get_all_places(city, 'places')
	print(ret)
