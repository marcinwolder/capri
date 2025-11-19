import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import jaccard_score

from src.data_model.user.user_info import TripInfo

user1_ratings = np.array([5, 3, 0, 1])
user2_ratings = np.array([4, 0, 3, 1])


def cosine_similarity(u, v):
	return 1 - cosine(u, v)


def pearson_similarity(u, v):
	return pearsonr(u, v)[0]


def jaccard_similarity(u, v):
	u_binary = np.array(u > 0, dtype=int)
	v_binary = np.array(v > 0, dtype=int)
	return jaccard_score(u_binary, v_binary)


def spearman_similarity(u, v):
	return spearmanr(u, v)[0]


def mean_squared_difference(u, v):
	diff = u - v
	non_zero_diff = diff[diff != 0]
	return np.mean(non_zero_diff**2)


def pip_similarity(u, v):
	proximity = 1 - (np.abs(u - v) / 4.0)
	impact = (np.abs(u - 2.5) * np.abs(v - 2.5)) + 1
	popularity = 1 + ((2.5 - np.abs(u - v)) / 2.5)
	return np.sum(proximity * impact * popularity)


def calculate_similarity():
	cosine_sim = cosine_similarity(user1_ratings, user2_ratings)
	pearson_sim = pearson_similarity(user1_ratings, user2_ratings)
	jaccard_sim = jaccard_similarity(user1_ratings, user2_ratings)
	spearman_sim = spearman_similarity(user1_ratings, user2_ratings)
	msd = mean_squared_difference(user1_ratings, user2_ratings)
	pip_sim = pip_similarity(user1_ratings, user2_ratings)


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


def init_users():
	preferences = {
		'art': 1,
		'antique': 1,
		'coffee': 1,
		'nature': 1,
		'museum': 1,
		'theater': 1,
	}

	user1 = TripInfo(
		user_id=1,
		user_preferences=preferences,
	)
	user2 = TripInfo(
		user_id=2,
		user_preferences=dict.fromkeys(preferences.keys(), -1),
	)

	print(user1.user_preferences, user2.user_preferences)

	return user1, user2


if __name__ == '__main__':
	user1, user2 = init_users()
	similarity = calculate_similarity_between_users(
		user1.user_preferences, user2.user_preferences
	)
	print(similarity)
