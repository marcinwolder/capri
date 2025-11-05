from src.constants import default_categories
from src.data_model.place.place import Place
from src.data_model.places.places import Places
from src.data_model.user.user_preferences import UserPreferences
from src.rating.user_preferences_rating import UserPreferencesRating


def calculate_cumulative_rating(places: Places, user_needs: UserPreferences):
    """Calculates cumulative rating for each place in the list"""
    user_preferences_rating = UserPreferencesRating(user_needs)
    for key, attraction in places.places.items():
        rating = _calculate_cumulative_rating(attraction, user_preferences_rating=user_preferences_rating)
        attraction.ratings.cumulative_rating = rating if rating is not None else 0
        places.set_place(attraction)


def calculate_cumulative_rating_for_restaurants(restaurants: Places, user_needs: UserPreferences):
    """Calculates cumulative rating for each place in the list"""
    user_preferences_rating = UserPreferencesRating(user_needs)
    for key, restaurant in restaurants.places.items():
        rating = _calculate_cumulative_rating(restaurant, user_preferences_rating=user_preferences_rating)
        restaurant.ratings.cumulative_rating = rating if rating is not None else 0
        restaurants.set_place(restaurant)


def _calculate_cumulative_rating(place, user_preferences_rating) -> float:
    """Calculates rating for a place based on its attributes."""

    alcohol = user_preferences_rating.alcohol_rating(place.alcohol)
    dogs = user_preferences_rating.allowsDogs_rating(place.allowsDogs)
    vegan = user_preferences_rating.servesVegetarianFood_rating(place.servesVegetarianFood)
    children = user_preferences_rating.children_rating(place.children)
    accessibility = user_preferences_rating.accessibilityOptions_rating(place.accessibilityOptions)
    group = user_preferences_rating.goodForGroups_rating(place.goodForGroups)

    price_level = user_preferences_rating.priceLevel_rating(place.priceLevel)
    if price_level == 0:
        return 0

    if len(user_preferences_rating.user_preferences.categories) == 0:
        
        user_preferences_rating.user_preferences.categories = default_categories 

    if place.must_see:
        return 1

    category = user_preferences_rating.category_rating(place.types)
    if category == 0:
        return 0

    statisticalRating = place.ratings.statisticalRating

    needs = [alcohol, dogs, vegan, children, accessibility, group]
    lst = [need for need in needs if need != -1]
    needs_rating = sum(lst) / len(lst) if len(lst) > 0 else 0

    rating_weight = 0.3
    category_weight = 0.3
    needs_weight = 0.4

    weighted_sum = needs_rating * needs_weight + category * category_weight + statisticalRating / 5 * rating_weight
    if len(lst) == 0:
        cumulative_rating = weighted_sum / (category_weight + rating_weight)
    else:
        cumulative_rating = weighted_sum / (needs_weight + category_weight + rating_weight)

    return cumulative_rating


def calculate_rating_for_restaurant(restaurant: Place, user_preferences_rating):
    """ Calculates rating for a restaurant based on its attributes."""

    restaurant = user_preferences_rating.dining_rating(restaurant.dining)
    if restaurant == -1:
        restaurant = user_preferences_rating.priceLevel_rating(restaurant.priceLevel)
        rating = restaurant.ratings.confidenceRating
        lst = [restaurant, rating]
    else:
        price_level = user_preferences_rating.priceLevel_rating(restaurant.priceLevel)
        normalizedRating = restaurant.ratings.confidenceRating
        lst = [restaurant, price_level, normalizedRating]

    lst = [i for i in lst if i != -1]
    rating = sum(lst) / len(lst)
    return rating

