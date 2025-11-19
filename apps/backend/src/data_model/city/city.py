import math
import pathlib
from dataclasses import dataclass
from random import random
from typing import Any

import pandas as pd
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class City:
	"""City data model.

	Methods:
	get_radius() - returns the radius of the city

	"""

	name: str
	country: str
	lat: float
	lng: float
	id: int
	population: int

	def __init__(self, city_id=None):
		if city_id is None:
			city_id = self.get_random_city_id()
		self.id = city_id
		attributes = self._get_city()
		attributes['name'] = attributes['city']
		for key, value in attributes.items():
			setattr(self, key, value)

	def get_radius(self):
		"""Function that returns the radius of the city."""
		if self.population < 50000:
			return 5000
		if 50000 <= self.population < 200000:
			return 10000
		if 200000 <= self.population < 1000000:
			return 15000
		return 20000

	def _get_city(self) -> dict[str, Any]:
		"""Function that returns a city object."""
		path = get_cities()
		data = pd.read_csv(path)
		data = data[data['id'] == self.id]
		attributes = ['id', 'city', 'country', 'population', 'lat', 'lng']
		data = data[attributes].to_dict('records')[0]
		return {str(k): v for k, v in data.items()}

	@staticmethod
	def get_const_krakow():
		"""Function that returns a city object."""
		return City(1616172264)

	@staticmethod
	def get_random_city_id():
		"""Function that returns a city object."""
		path: pathlib.Path = get_cities()
		data: pd.DataFrame = pd.read_csv(path)
		return data[['id']].to_dict('records')[math.floor(random() * len(data))]['id']

	def __str__(self):
		return f'City: {self.name}, {self.country}, {self.lat}, {self.lng}, {self.id}, {self.population}'

	def __repr__(self):
		return f'City: {self.name}, {self.country}, {self.lat}, {self.lng}, {self.id}, {self.population}'

	def to_json(self):
		return self.to_dict()

	def to_dict(self):
		return {
			'name': self.name,
			'country': self.country,
			'lat': self.lat,
			'lng': self.lng,
			'id': self.id,
			'population': self.population,
		}


def get_cities():
	"""Function that returns the path to the file worldcities"""
	management_path = pathlib.Path(__file__).parent
	parent_path = management_path.parent.parent
	project_path = parent_path / 'constants'
	path = project_path / 'worldcities/worldcities.csv'
	return path
