import numpy as np
import requests
from joblib import load

from src.data_model.city.city import City
from src.data_model.place.place_subclasses import Location
from src.path import get_path
from src.route_optimalization.haversine import calculate_distance


class TravelEstimator:
	def __init__(
		self,
		car_model_path=get_path('car_model.joblib', 'time_estimation_models'),
		foot_model_path=get_path('foot_model.joblib', 'time_estimation_models'),
	):
		self.car_model = load(car_model_path)
		self.foot_model = load(foot_model_path)

	@staticmethod
	def _model_predict(model, distance):
		"""Zwraca czas w sekundach na podstawie modelu regresji liniowej.

		:param model: Model regresji liniowej.
		:param distance: Dystans w kilometrach.
		:return: time in seconds
		"""
		if distance == 0:
			return 0
		prediction = model.predict(np.array([[distance]])).tolist()[0]
		return prediction * 60 * 60

	def get_estimated_time(
		self, start_coordinates: Location, end_coordinates: Location, city: City = None
	):
		"""Zwraca czas w minutach i środek transportu"""
		distance = calculate_distance(
			start_coordinates.latitude,
			start_coordinates.longitude,
			end_coordinates.latitude,
			end_coordinates.longitude,
		)
		if distance > 5:
			if city is not None and city.country == 'Poland':
				try:
					return int(
						self.get_travel_time(start_coordinates, end_coordinates) / 60
					) * 2, 'CAR'
				except Exception as _:
					pass
			return int(self._model_predict(self.car_model, distance) / 60) * 2, 'CAR'
		return int(self._model_predict(self.foot_model, distance) / 60), 'FOOT'

	@staticmethod
	def get_travel_time(
		start_coordinates, end_coordinates, server_url='http://127.0.0.1:5002'
	):
		"""Calculate travel time using OSRM (Open Source Routing Machine) with OpenStreetMap data.

		:param start_coordinates: Tuple of (latitude, longitude) for the start location.
		:param end_coordinates: Tuple of (latitude, longitude) for the end location.
		:param server_url: URL of the OSRM server instance.
		:return: Travel time in seconds and the route distance in meters.
		"""
		coordinates = (
			f'{start_coordinates.longitude},{start_coordinates.latitude};'
			f'{end_coordinates.longitude},{end_coordinates.latitude}'
		)
		request_url = f'{server_url}/route/v1/driving/{coordinates}'

		response = requests.get(request_url, timeout=0.1)
		if response.status_code == 200:
			data = response.json()
			route = data['routes'][0]
			travel_time = route['duration']
			if travel_time <= 0:
				raise Exception(
					f'Error: Negative travel time or distance. Travel time: {travel_time}'
				)
			return travel_time
		raise Exception(
			f'Error: Unable to fetch data from OSRM. Status code: {response.status_code}'
		)


travel_estimator = TravelEstimator()

if __name__ == '__main__':
	start_coordinates = Location(latitude=50.0647, longitude=19.9450)
	end_coordinates = Location(latitude=50.0647, longitude=19.9450)
	print(
		travel_estimator.get_estimated_time(
			start_coordinates=start_coordinates,
			end_coordinates=end_coordinates,
			city=City.get_const_krakow(),
		)
	)
