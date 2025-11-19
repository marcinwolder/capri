from src.data_model import PlaceFromAPI
from src.data_model.city.city import City


def test_place():
	place = PlaceFromAPI(
		{
			'id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
			'name': 'Eiffel Tower',
			'types': ['tourist_attraction', 'point_of_interest', 'establishment'],
			'rating': 4.6,
			'user_ratings_total': 141575,
			'lat': 48.85837009999999,
			'lng': 2.2944813,
			'address': 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France',
			'photo': 'https://lh5.googleusercontent.com/p/AF1QipO0l8bqk4Yy2W7l3f0Ygk3lX7xYyqIi7R4V7H0=w213-h160-k-no',
			'description': 'Iconic, 19th-century, wrought-iron lattice tower on the Champ de Mars with panoramic city views.',
			'opening_hours': 'Monday: Open 24 hours\nTuesday: Open 24 hours\nWednesday: Open 24 hours\nThursday: Open 24 hours\nFriday: Open 24 hours\nSaturday: Open 24 hours\nSunday: Open 24 hours',
			'website': 'https://www.toureiffel.paris/en',
			'phone_number': '+33 892 70 12 39',
		},
		city=City.get_const_krakow(),
	)
	assert place.id == 'ChIJN1t_tDeuEmsRUsoyG83frY4'
	assert place.name == 'Eiffel Tower'
	assert place.types == ['tourist_attraction', 'point_of_interest', 'establishment']
	assert place.rating == 4.6
	assert place.user_ratings_total == 141575
	assert place.lat == 48.85837009999999
	assert place.lng == 2.2944813
	assert (
		place.address == 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France'
	)
	assert (
		place.photo
		== 'https://lh5.googleusercontent.com/p/AF1QipO0l8bqk4Yy2W7l3f0Ygk3lX7xYyqIi7R4V7H0=w213-h160-k-no'
	)
	assert place.description
	assert (
		place.opening_hours
		== 'Monday: Open 24 hours\nTuesday: Open 24 hours\nWednesday: Open 24 hours\nThursday: Open 24 hours\nFriday: Open 24 hours\nSaturday: Open 24 hours\nSunday: Open 24 hours'
	)
	assert place.website == 'https://www.toureiffel.paris/en'
	assert place.phone_number == '+33 892 70 12 39'

	place = PlaceFromAPI(
		{
			'id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
			'name': 'Eiffel Tower',
			'types': ['tourist_attraction', 'point_of_interest', 'establishment'],
			'rating': 4.6,
			'user_ratings_total': 141575,
			'lat': 48.85837009999999,
			'lng': 2.2944813,
			'address': 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France',
			'photo': 'https://lh5.googleusercontent.com/p/AF1QipO0l8bqk4Yy2W7l3f0Ygk3lX7xYyqIi7R4V7H0=w213-h160-k-no',
			'description': 'Iconic, 19th-century, wrought-iron lattice tower on the Champ de Mars with panoramic city views.',
			'opening_hours': 'Monday: Open 24 hours\nTuesday: Open 24 hours\nWednesday: Open 24 hours\nThursday: Open 24 hours\nFriday: Open 24 hours\nSaturday: Open 24 hours\nSunday: Open 24 hours',
			'website': 'https://www.toureiffel.paris/en',
			'phone_number': '+33 892 70 12 39',
		},
		city=City.get_const_krakow(),
	)
	assert place.id == 'ChIJN1t_tDeuEmsRUsoyG83frY4'
	assert place.name == 'Eiffel Tower'
	assert place.types == ['tourist_attraction', 'point_of_interest', 'establishment']
	assert place.rating == 4.6
	assert place.user_ratings_total == 141575
	assert place.lat == 48.85837009999999
	assert place.lng == 2.2944813
	assert (
		place.address == 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France'
	)
	assert (
		place.photo
		== 'https://lh5.googleusercontent.com/p/AF1QipO0l8bqk4Yy2W7l3f0Ygk3lX7xYyqIi7R4V7H0=w213-h160-k-no'
	)
	assert place.description
	assert (
		place.opening_hours
		== 'Monday: Open 24 hours\nTuesday: Open 24 hours\nWednesday: Open 24 hours\nThursday: Open 24 hours\nFriday: Open 24 hours\nSaturday: Open 24 hours\nSunday: Open 24 hours'
	)
	assert place.website == 'https://www.toureiffel.paris/en'
	assert place.phone_number == '+33 892 70 12 39'
