"""How user1 is similar to user2 based on their preferences."""

import numpy as np

from src.collaborative_filltering.main import cosine_similarity
from src.data_model.user.user_preferences import UserPreferences


def calculate_similarity_between_users(user1_preferences, user2_preferences):
	"""Calculate similarity between users based on their preferences.

	:param user1_preferences: dictionary with user1 preferences
	:param user2_preferences: dictionary with user2 preferences
	:return: similarity between users
	"""
	user1_ratings = np.array(list(user1_preferences.values()))
	user2_ratings = np.array(list(user2_preferences.values()))
	cosine_sim = cosine_similarity(user1_ratings, user2_ratings)
	return cosine_sim


def debug():
	userPreferences = UserPreferences(
		needs=[],
		priceLevel=5,
		categories=['museum', 'park', 'zoo', 'church'],
		subcategories={
			'museum': ['Art', 'History', 'Science', 'War', 'Maritime'],
			'park': [],
			'zoo': [],
			'church': [],
		},
	)

	user_preferences2 = UserPreferences(
		needs=[],
		priceLevel=5,
		categories=['museum', 'park', 'zoo', 'church'],
		subcategories={
			'museum': ['Art', 'History', 'Science', 'War', 'Maritime'],
			'park': [],
			'zoo': [],
			'church': [],
		},
	)
	return user1, user2


if __name__ == '__main__':
	user1, user2 = debug()

	print(user1.user_preferences.categories)
	print(user2.user_preferences.categories)
	similarity = calculate_similarity_between_users(
		user1.user_preferences.categories, user2.user_preferences.categories
	)
	print(similarity)
