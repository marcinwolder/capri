import math
import pathlib
from dataclasses import dataclass
from random import random
import pandas as pd
from dataclasses_json import dataclass_json

from src.data_model.custom_decorators import ToJson


@dataclass_json
@dataclass
class City(ToJson):
    """
    City data model.

    Methods:
    get_radius() - returns the radius of the city
    """

    name: str
    country: str
    lat: float
    lng: float
    id: int
    population: int

    def __init__(self, _id=None):
        if _id is None:
            _id = self.get_random_city_id()
        self.id = _id
        attributes = self._get_city()
        attributes['name'] = attributes['city']
        for key, value in attributes.items():
            setattr(self, key, value)

    def get_radius(self):
        """Function that returns the radius of the city."""
        if self.population < 50000:
            return 5000
        elif 50000 <= self.population < 200000:
            return 10000
        elif 200000 <= self.population < 1000000:
            return 15000
        else:
            return 20000

    def _get_city(self):
        """Function that returns a city object."""
        path = get_cities()
        data = pd.read_csv(path)
        data = data[data['id'] == self.id]
        attributes = ['id', 'city', 'country', 'population', 'lat', 'lng']
        return data[attributes].to_dict('records')[0]

    @staticmethod
    def get_const_krakow():
        """Function that returns a city object."""
        return City(1616172264)

    @staticmethod
    def get_random_city_id():
        """Function that returns a city object."""
        path = get_cities()
        data = pd.read_csv(path)
        return data[['id']].to_dict('records')[math.floor(random() * len(data))]['id']

    def __str__(self):
        return f"City: {self.name}, {self.country}, {self.lat}, {self.lng}, {self.id}, {self.population}"

    def __repr__(self):
        return f"City: {self.name}, {self.country}, {self.lat}, {self.lng}, {self.id}, {self.population}"

    def to_json(self):
        return self.to_dict()

    def to_dict(self):
        return {
            "name": self.name,
            "country": self.country,
            "lat": self.lat,
            "lng": self.lng,
            "id": self.id,
            "population": self.population
        }


def get_cities():
    """Function that returns the path to the file worldcities"""

    management_path = pathlib.Path(__file__).parent
    parent_path = management_path.parent.parent
    project_path = parent_path / 'constants'
    path = project_path / 'worldcities/worldcities.csv'
    return path
