import requests

from src.backend.get_recommendation import _get_from_file
from src.data_model.city.city import City


def get_subcategories():
	"""Function that gets subcategories from the NLP module.

	For a specific location,
	we retrieve reviews and pass them to the NLP module
	along with subcategories to determine their belonging to a
	particular subcategory. We fetch places from the database and
	update them if the place belongs to a specific subcategory.
	"""
	city = City(1840014613)
	places, _ = _get_from_file(city)
	place = places.get_list()[0]
	reviews = [review.text for review in place.reviews]
	categories = place.types
	data = {
		'subcategories': categories,
		'reviews': reviews,
	}
	url = 'http://127.0.0.1:5001/get_place'
	ret = requests.post(url, json=data)
	print('reviews', reviews)
	print('ret', ret.json())
	print('cat ', place.types)

	return places


def main():
	get_subcategories()


if __name__ == '__main__':
	main()
