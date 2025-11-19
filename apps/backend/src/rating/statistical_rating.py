from src.data_model.city.city import City


class StatisticalRating:
	city: City
	_average_rating: float = -1
	_average_rating_count: float = -1

	def __init__(self, _places):
		print('places', _places, type(_places))
		self._places = _places.places

	@property
	def count(self):
		"""Returns the number of places"""
		return len(self._places)

	def calculate_bayesian_rating(self, place, average_review_count, average_rating):
		"""Calculates Bayesian rating for a place.

		Takes into account average number of reviews and average rating to get statistical rating.

		:param place: place to be rated
		:param average_review_count: average number of reviews
		:param average_rating: average rating
		:return: Bayesian rating
		"""
		print(
			place.placeInfo.id,
			average_review_count,
			average_rating,
			place.ratings.userRatingCount,
			place.ratings.rating,
		)
		sum_review_count = average_review_count + place.ratings.userRatingCount
		print(sum_review_count)
		if sum_review_count == 0:
			return 0
		return (
			average_review_count * average_rating
			+ place.ratings.userRatingCount * place.ratings.rating
		) / sum_review_count

	def _calculate_average(self, attr_func):
		"""Helper method to calculate average."""
		total = 0
		for place in self._places.values():
			total += attr_func(place)
		return total / len(self._places)

	@property
	def average_rating(self) -> float:
		"""Returns an average rating of all places"""
		if self.count == 0:
			return 0
		if self._average_rating == -1:
			self._average_rating = self._calculate_average(
				lambda place: place.ratings.cumulative_rating
			)
		return self._average_rating

	@property
	def average_rating_count(self) -> float:
		"""Returns an average rating count of all places"""
		if self.count == 0:
			return 0
		if self._average_rating_count == -1:
			self._average_rating_count = self._calculate_average(
				lambda place: place.ratings.userRatingCount
			)
		return self._average_rating_count

	def calculate_statistical_rating(self):
		"""Returns a Bayesian normalized rating of all places"""
		for place in self._places.values():
			place.ratings.statisticalRating = self.calculate_bayesian_rating(
				place, self.average_rating_count, self.average_rating
			)
