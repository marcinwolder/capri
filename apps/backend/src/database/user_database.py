"""Local JSON-backed storage for user preferences and trip history."""

import copy
import json
import os
from pathlib import Path
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv

from src.data_model import TripInfo
from src.data_model.city.city import City

load_dotenv()


class DataBaseUsers:
	"""Local persistence replacing Firebase users/trip history."""

	def __init__(self, base_path: str | Path | None = None):
		default_base = Path(__file__).resolve().parents[2] / 'data'
		self.base_path = Path(os.getenv('DATA_DIR', base_path or default_base))
		self.base_path.mkdir(parents=True, exist_ok=True)
		self.users_file = self.base_path / 'users.json'
		if not self.users_file.exists():
			self._persist({'users': {}})

	def _load(self) -> dict[str, Any]:
		with open(self.users_file, 'r', encoding='utf-8') as handle:
			try:
				return json.load(handle)
			except json.JSONDecodeError:
				return {'users': {}}

	def _persist(self, payload: dict[str, Any]):
		self.users_file.parent.mkdir(parents=True, exist_ok=True)
		with open(self.users_file, 'w', encoding='utf-8') as handle:
			json.dump(payload, handle)

	def _get_or_create_user(self, user_id: str) -> dict[str, Any]:
		data = self._load()
		users = data.setdefault('users', {})
		if user_id not in users:
			users[user_id] = {
				'id': user_id,
				'profile': {},
				'preferences': {},
				'trip_history': [],
			}
			self._persist(data)
		return users[user_id]

	def get_one_user_by_id(self, user: TripInfo):
		"""Return stored user payload."""
		data = self._load()
		return data.get('users', {}).get(user.user_id)

	def check_if_user_exist(self, user: TripInfo):
		data = self._load()
		return user.user_id in data.get('users', {})

	def update_user(self, user: TripInfo):
		data = self._load()
		users = data.setdefault('users', {})
		users[user.user_id] = users.get(user.user_id, {})
		users[user.user_id]['id'] = user.user_id
		users[user.user_id]['profile'] = user.to_dict()
		self._persist(data)

	def save_user_preferences(self, user: TripInfo):
		data = self._load()
		users = data.setdefault('users', {})
		users[user.user_id] = users.get(user.user_id, {'id': user.user_id})
		users[user.user_id]['preferences'] = user.user_preferences.to_dict()
		self._persist(data)

	def save_user_trip_history(self, user_id: str, city: City, itinerary: dict) -> str:
		"""Persist a trip itinerary locally."""
		data = self._load()
		users = data.setdefault('users', {})
		user_entry = users.setdefault(
			user_id,
			{'id': user_id, 'profile': {}, 'preferences': {}, 'trip_history': []},
		)

		itinerary_copy = copy.deepcopy(itinerary)
		days = itinerary_copy.pop('days', [])
		trip_id = itinerary_copy.pop('id', str(uuid4()))
		payload = {
			'id': trip_id,
			'days': days,
			'days_len': len(days),
			'city_id': city.id,
			'city_name': city.name,
			**itinerary_copy,
		}

		user_entry['trip_history'] = user_entry.get('trip_history', [])
		user_entry['trip_history'] = [
			t for t in user_entry['trip_history'] if t.get('id') != trip_id
		]
		user_entry['trip_history'].append(payload)
		self._persist(data)
		return trip_id

	@staticmethod
	def _trip_to_dict(trip: dict[str, Any]):
		"""Normalize trip payload to expected shape."""
		trip_info = {'id': trip.get('id'), 'days': trip.get('days', []), **trip}
		trip_info.pop('trip_history', None)
		return trip_info

	def get_user_trip(self, user_id: str, trip_id: str):
		data = self._load()
		user_entry = data.get('users', {}).get(user_id)
		if not user_entry:
			raise ValueError(f'User {user_id} not found')
		for trip in user_entry.get('trip_history', []):
			if trip.get('id') == trip_id:
				return self._trip_to_dict(trip)
		raise ValueError(f'Trip {trip_id} not found for user {user_id}')

	def get_user_trip_history(self, user_id: str):
		data = self._load()
		user_entry = data.get('users', {}).get(user_id, {})
		return [self._trip_to_dict(trip) for trip in user_entry.get('trip_history', [])]

	def set_trip_rating(
		self, user_id: str, trip_id: str, day_index: int, place_index: int, rating: float
	):
		"""Update rating for a place within a stored trip."""
		data = self._load()
		user_entry = data.get('users', {}).get(user_id)
		if not user_entry:
			raise ValueError(f'User {user_id} not found')
		for trip in user_entry.get('trip_history', []):
			if trip.get('id') != trip_id:
				continue
			days = trip.get('days', [])
			if day_index >= len(days):
				raise IndexError('Invalid day index')
			places = days[day_index].get('places', [])
			if place_index >= len(places):
				raise IndexError('Invalid place index')
			places[place_index]['user_rating'] = rating
			self._persist(data)
			return
		raise ValueError(f'Trip {trip_id} not found for user {user_id}')

	def get_all_users(self):
		"""Return all stored user profiles."""
		data = self._load()
		return list(data.get('users', {}).values())
