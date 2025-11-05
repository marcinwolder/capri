from scipy import stats


def _calculate_confidence(population):
    """Calculates confidence based on population.

    Adjust confidence based on population.
    Lower confidence for smaller populations

    :param population: population of the city
    :return: confidence
    """

    if population < 200000:
        return 0.95
    elif 200000 <= population < 1000000:
        return 0.975
    else:
        return 0.999


def confidence_rating_by_population(rating, user_rating_count, population=200000):
    """Calculates normalized rating for a place.

    Calculates minimal rating for place based on its rating and number of user ratings.
    Confidence increases with the population of the city.

    :param rating: rating of the place
    :param user_rating_count: number of user ratings
    :param population: population of the city
    :return: normalized rating
    """

    if user_rating_count == 0:
        return 0

    confidence = _calculate_confidence(population)
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    avg_rating_normalized = rating / 5
    factor = z ** 2 / (2 * user_rating_count)
    confidence_interval = z * ((avg_rating_normalized * (1 - avg_rating_normalized) + z ** 2 / (
            4 * user_rating_count)) / user_rating_count) ** 0.5
    lower_bound = (avg_rating_normalized + factor - confidence_interval) / (1 + z ** 2 / user_rating_count)
    return max(1, min(5, lower_bound * 5))  
