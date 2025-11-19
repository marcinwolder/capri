import logging
import time
from math import inf

from src.data_model import PlaceVisitor

from ..api_calls import get_restaurants_for_city
from ..api_calls.llama import Llama
from ..api_calls.weather import get_weather_for_dates
from ..constants._outdoor import outdoor_categories
from ..data_model.places.places import Places
from ..data_model.user.user_info import TripInfo
from ..path import get_path
from ..rating.cumulative_rating import calculate_cumulative_rating
from ..route_optimalization import SplitForDays
from ..route_optimalization.routing import Routing

breakfast_time = 60 * 8
coffee_time = 60 * 10
lunch_time = 60 * 13
dinner_time = 60 * 18
bar_time = 60 * 20
eating_list = [breakfast_time, coffee_time, lunch_time, dinner_time, bar_time]


class Recommendation:
	"""Class that handles the recommendation process."""

	def __init__(self, places: Places, user: TripInfo):
		self.attractions_in_graph = None
		self.user_hotel = user.hotel
		self.days = user.days
		self.graph = None
		self.places = places
		self.user_needs = user.user_preferences
		self.trip_time = 8
		self.summary = ''
		self.recommended_places = []
		self.recommended_restaurants = []
		self.dates = user.dates
		self.weather = []
		self.transportations = []

	def check_good_hours(self):
		for day in range(7):
			for place in self.places.get_list():
				if (
					place.regularOpeningHours.periods[day].open_in_minutes
					< place.regularOpeningHours.periods[day].close_in_minutes
				):
					place.regularOpeningHours.periods[day].open_in_minutes = 0
					place.regularOpeningHours.periods[day].close_in_minutes = 0

	def get_recommendation(self):
		"""Function that gets the recommendation."""
		calculate_cumulative_rating(places=self.places, user_needs=self.user_needs)

		self.check_good_hours()
		self.weather = get_weather_for_dates(
			self.places.city.lat, self.places.city.lng, self.dates[0], self.dates[1]
		)
		print('weather', self.weather)

		places_positive_rating = Places(
			[
				place
				for place in self.places.get_list()
				if place.ratings.cumulative_rating > 0
			]
		)

		splitForDays = SplitForDays(
			from_date=self.dates[0],
			to_date=self.dates[1],
			places=places_positive_rating,
		)
		clustered_places = splitForDays.split()
		print('clustered_places', clustered_places)
		path = get_path('clusters.html', 'outputs')
		# open_map(clustered_places, save_name=path)

		self.recommended_places = []

		for i, places in enumerate(clustered_places):
			route, transportations = Routing(
				places,
				depot=self.user_hotel,
				num_routes=1,
				period_index=splitForDays.weekday_indices[i],
			).get_routes()
			self.recommended_places.append(route)
			self.transportations.append(transportations)

		print('recommended_places', self.recommended_places)

		self._get_summary()

		print('summary', self.summary)

		# open_map(self.recommended_places, city=self.places.city)
		return self

	def check_if_outdoor(self, places: Places, day: int):
		"""Check if the place is outdoor and if the weather is good."""
		good_places = []
		for place in places.get_list():
			for outdoor_cat in outdoor_categories:
				if outdoor_cat in place.types:
					place.regularOpeningHours.periods[0].open_in_minutes = 0
					place.regularOpeningHours.periods[0].close_in_minutes = 0
					place.regularOpeningHours.periods[1].open_in_minutes = 0
					place.regularOpeningHours.periods[1].close_in_minutes = 0

					good_places.append(place)
		return Places(good_places)

	def search_restaurants(self, route: Places):
		"""For each item in eating_list find the closest time to eat
		and search for restaurants nearby

		Dla każdego typu jedzenia znajdź najbliższy czas przyjazdu, by o odpowiedniej godzinie
		zjeść odpowiedni posiłek
		"""
		ret_restaurnats = []
		time, arrival_times = 0, 0

		for eating_time in eating_list:
			diff, id = inf, None
			for place_id, arrival_time in arrival_times.items():
				if abs(arrival_time - eating_time) < diff:
					diff = abs(arrival_time - eating_time)
					id = place_id
			if id is not None:
				place = route.get_place_by_id(id)

				if self.user_needs.servesVegetarianFood:
					params = {'keyword': 'vegetarian'}

				else:
					params = {}
				restaurants = get_restaurants_for_city(
					db=None,
					lat=place.location.latitude,
					lng=place.location.longitude,
					city=self.places.city,
					radius=500,
					included_types=params,
				)

				if restaurants is not None and restaurants.count > 0:
					calculate_cumulative_rating(
						places=restaurants, user_needs=self.user_needs
					)

					ret_restaurnats.append(restaurants.get_list()[0])

			else:
				logging.warning('No place found for eating time: %s', eating_time)
		return Places(ret_restaurnats)

	def _get_summary(self):
		"""Function that returns a summary of the trip."""
		tic = time.perf_counter()
		self.summary = Llama.get_summary(
			city=self.places.city.name, trip=self.recommended_places
		)
		toc = time.perf_counter()
		print(f'Summary in {toc - tic:0.4f} seconds')

	def get_itinerary(self):
		"""Function that returns a list of place for each day."""
		formatted_places = []
		for i, places in enumerate(self.recommended_places):
			day_with_attributes = []
			for j, place in enumerate(places.get_list()):
				try:
					transportation = self.transportations[i][j]
				except IndexError:
					transportation = None
				day_with_attributes.append(
					PlaceVisitor().place_to_itinerary(place, transportation)
				)
			formatted_places.append(day_with_attributes)
		days = [
			{'places': places, 'weather': self.weather[i]}
			for i, places in enumerate(formatted_places)
		]
		itinerary = {
			'days': days,
			'summary': self.summary,
			'dates': [d.isoformat() for d in self.dates],
			'city_name': self.places.city.name,
			'city_id': self.places.city.id,
		}
		logging.info(formatted_places)
		return itinerary
