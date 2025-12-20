"""Local JSON-backed storage for places data (cloudless replacement)."""

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src.constants import default_categories, dining
from src.data_model import Places
from src.data_model.city.city import City
from src.data_model.place.place import Place, PlaceCreator, PlaceCreatorDatabase

load_dotenv()


class DataBase:
	"""Lightweight local persistence layer that replaces Firebase."""

	def __init__(self, base_path: str | Path | None = None):
		default_base = Path(__file__).resolve().parents[2] / 'data'
		self.base_path = Path(os.getenv('DATA_DIR', base_path or default_base))
		self.places_path = self.base_path / 'places'
		self.places_path.mkdir(parents=True, exist_ok=True)
		self._categories = default_categories
		self._dining = dining

	@staticmethod
	def _city_file(city: City) -> Path:
		country = str(city.country).replace(' ', '_').lower()
		return Path(f'{country}_{city.id}.json')

	def _load_city_payload(self, city: City) -> dict[str, Any]:
		file_path = self.places_path / self._city_file(city)
		if not file_path.exists():
			return {'places': [], 'categories': {}}
		with open(file_path, 'r', encoding='utf-8') as handle:
			try:
				return json.load(handle)
			except json.JSONDecodeError:
				return {'places': [], 'categories': {}}

	def _write_city_payload(self, city: City, payload: dict[str, Any]):
		file_path = self.places_path / self._city_file(city)
		file_path.parent.mkdir(parents=True, exist_ok=True)
		with open(file_path, 'w', encoding='utf-8') as handle:
			json.dump(payload, handle)

	def add_place_to_database(
		self,
		place: Place,
		city: City,
		category_type: str,
		place_type: str,
		categories: list[str],
	):
		"""Persist a place locally; avoids duplicate ids."""
		payload = self._load_city_payload(city)
		place_dict = json.loads(place.to_json())
		existing = [
			p for p in payload.get('places', []) if p.get('placeInfo', {}).get('id') != place.placeInfo.id
		]
		existing.append(place_dict)
		payload['places'] = existing
		cat_map = payload.get('categories', {})
		cat_map[category_type] = categories
		payload['categories'] = cat_map
		self._write_city_payload(city, payload)

	def add_categories_to_database(
		self, city, category_type: str, categories: list[str]
	):
		payload = self._load_city_payload(city)
		cat_map = payload.get('categories', {})
		cat_map[category_type] = categories
		payload['categories'] = cat_map
		self._write_city_payload(city, payload)

	def read_places_data_from_db(
		self, city, place_type: str, placeCreator: type[PlaceCreator]
	) -> Places:
		"""Load places for a city and hydrate them into objects."""
		payload = self._load_city_payload(city)
		places = []
		for item in payload.get('places', []):
			place = placeCreator(item, city).create_place()
			places.append(place)
		return Places(places, city)

	def check_if_city_exist(self, city):
		"""Check if we have cached data for a city."""
		return (self.places_path / self._city_file(city)).exists()

	def get_all_places(self, city, place_type: str):
		"""Return all raw places for a city."""
		payload = self._load_city_payload(city)
		return payload.get('places', [])

	def get_place(self, city, place_id: str):
		"""Return a single place by id."""
		payload = self._load_city_payload(city)
		for item in payload.get('places', []):
			if item.get('placeInfo', {}).get('id') == place_id:
				return PlaceCreatorDatabase(item, city).create_place()
		raise ValueError(f'Place {place_id} not found for city {city.id}')
