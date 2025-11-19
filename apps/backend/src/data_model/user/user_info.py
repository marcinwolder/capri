from dataclasses import dataclass
from datetime import date

from dataclasses_json import dataclass_json

from src.data_model.city.city import City
from src.data_model.place.place import Place
from src.data_model.place.place_subclasses import (
	Location,
	Period,
	PlaceInfo,
	RegularOpeningHours,
	TimePoint,
)
from src.data_model.user.user_preferences import UserPreferences


@dataclass_json
@dataclass
class TripInfo:
	"""Class representing user with his preferences and location"""

	user_id: str
	user_preferences: UserPreferences

	def __init__(
		self,
		user_id='',
		location=None,
		user_preferences=None,
		city=City(),
		days=1,
		dates: [date, date] = None,
	):
		self.user_id = user_id
		self.location = location
		self.user_preferences = user_preferences
		self.city = city
		self.days = days

		self.hotel = self._init_hotel()
		self.dates = dates

	def _init_hotel(self):
		return Place(
			placeInfo=PlaceInfo(displayName='Hotel', id='0'),
			location=Location(latitude=self.city.lat, longitude=self.city.lng),
			regularOpeningHours=RegularOpeningHours(
				periods=[
					Period(open=TimePoint(), close=TimePoint(23)) for _ in range(7)
				],
				weekdayDescriptions=[''],
			),
			estimatedTime=0,
		)

	def to_json(self):
		return self.to_dict()

	def to_dict(self):
		return {
			'user_id': self.user_id,
			'location': self.location,
			'user_preferences': self.user_preferences.to_dict(),
			'days': self.days,
		}

	def __repr__(self):
		return str(self.__dict__)
