"""Local JSON-backed storage for trip history (global, no users)."""

import copy
import json
import os
from pathlib import Path
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv

from src.data_model.city.city import City

load_dotenv()


class DataBaseTrips:
	"""Global persistence for trips, without user scoping."""

	def __init__(self, base_path: str | Path | None = None):
		default_base = Path(__file__).resolve().parents[2] / 'data'
		self.base_path = Path(os.getenv('DATA_DIR', base_path or default_base))
		self.base_path.mkdir(parents=True, exist_ok=True)
		self.trips_file = self.base_path / 'trips.json'
		if not self.trips_file.exists():
			self._persist({'trips': []})

	def _load(self) -> dict[str, Any]:
		with open(self.trips_file, 'r', encoding='utf-8') as handle:
			try:
				return json.load(handle)
			except json.JSONDecodeError:
				return {'trips': []}

	def _persist(self, payload: dict[str, Any]):
		self.trips_file.parent.mkdir(parents=True, exist_ok=True)
		with open(self.trips_file, 'w', encoding='utf-8') as handle:
			json.dump(payload, handle)

	def save_trip_history(self, city: City, itinerary: dict) -> str:
		"""Persist a trip itinerary globally."""
		data = self._load()
		trips = data.setdefault('trips', [])

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

		trips = [t for t in trips if t.get('id') != trip_id]
		trips.append(payload)
		data['trips'] = trips
		self._persist(data)
		return trip_id

	@staticmethod
	def _trip_to_dict(trip: dict[str, Any]):
		"""Normalize trip payload to expected shape."""
		trip_info = {'id': trip.get('id'), 'days': trip.get('days', []), **trip}
		trip_info.pop('trip_history', None)
		return trip_info

	def get_trip(self, trip_id: str):
		data = self._load()
		for trip in data.get('trips', []):
			if trip.get('id') == trip_id:
				return self._trip_to_dict(trip)
		raise ValueError(f'Trip {trip_id} not found')

	def get_trip_history(self):
		data = self._load()
		return [self._trip_to_dict(trip) for trip in data.get('trips', [])]

	def set_trip_rating(
		self, trip_id: str, day_index: int, place_index: int, rating: float
	):
		"""Update rating for a place within a stored trip."""
		data = self._load()
		trips = data.get('trips', [])
		for trip in trips:
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
		raise ValueError(f'Trip {trip_id} not found')
