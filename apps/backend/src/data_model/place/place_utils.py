def miniman_review_count(population):
	"""Minimal number of reviews for a place to be considered.

	:param population: population of the city
	:return: minimal number of reviews
	"""
	if population < 50000:
		return 10
	if 50000 <= population < 200000:
		return 20
	if 200000 <= population < 1000000:
		return 50
	return 100


def map_prices(priceLevel):
	"""Function that maps price level to a number."""
	if isinstance(priceLevel, int):
		return priceLevel
	match priceLevel:
		case 'PRICE_LEVEL_FREE':
			return 0
		case 'PRICE_LEVEL_INEXPENSIVE':
			return 1
		case 'PRICE_LEVEL_MODERATE':
			return 2
		case 'PRICE_LEVEL_EXPENSIVE':
			return 3
		case 'PRICE_LEVEL_VERY_EXPENSIVE':
			return 4
		case _:
			return 0
