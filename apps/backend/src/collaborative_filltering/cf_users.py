import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from src.collaborative_filltering.dct import matrix


def get_similarity_between_users(data: dict):
	"""Pivot table, aby uzyskać macierz użytkownik-produkt
	Oblicz podobieństwo cosinusowe
	"""
	ratings = pd.DataFrame(data)
	ratings_matrix = ratings.pivot_table(
		index='user_id', columns='item_id', values='rating'
	).fillna(0)

	user_similarity = cosine_similarity(ratings_matrix)
	user_similarity_df = pd.DataFrame(
		user_similarity, index=ratings_matrix.index, columns=ratings_matrix.index
	)

	return user_similarity_df, ratings_matrix


def find_top_n_neighbors(user_similarity_df, n_neighbors):
	"""Znajdź N najbardziej podobnych sąsiadów dla każdego użytkownika.

	Args:
	- user_similarity_df: DataFrame zawierający podobieństwo między użytkownikami.
	- n_neighbors: Liczba sąsiadów do znalezienia.

	Returns:
	- top_neighbors_df: DataFrame zawierający N najbardziej podobnych sąsiadów dla każdego użytkownika.

	"""
	top_neighbors = np.argsort(-user_similarity_df.values, axis=1)[
		:, 1 : n_neighbors + 1
	]
	top_neighbors_df = pd.DataFrame(
		top_neighbors,
		index=user_similarity_df.index,
		columns=[f'Neighbor_{i + 1}' for i in range(n_neighbors)],
	)

	return top_neighbors_df


def predict_ratings_with_neighbors(
	ratings_matrix, user_similarity_df, top_neighbors_df
):
	"""Przewidywanie ocen używając N najbardziej podobnych sąsiadów.

	Args:
	- ratings_matrix: Macierz ocen użytkownik-produkt.
	- user_similarity_df: DataFrame zawierający podobieństwo między użytkownikami.
	- top_neighbors_df: DataFrame zawierający N najbardziej podobnych sąsiadów dla każdego użytkownika.

	Returns:
	- predictions: Macierz przewidywanych ocen.

	"""
	predictions = np.zeros(ratings_matrix.shape)

	for i in range(ratings_matrix.shape[0]):
		neighbors_idx = top_neighbors_df.iloc[i].values
		neighbor_similarities = user_similarity_df.iloc[i, neighbors_idx]
		neighbor_ratings = ratings_matrix.iloc[neighbors_idx, :]
		sim_sum = np.sum(neighbor_similarities)

		rated_items = neighbor_ratings.T.dot(neighbor_similarities) / sim_sum
		predictions[i, :] = rated_items

	return predictions


def kmeans():
	""""""


def main():
	data = matrix
	user_similarity_df, ratings_matrix = get_similarity_between_users(data)
	print('user_similarity_df\n', user_similarity_df)
	print('ratings_matrix\n', ratings_matrix)
	n_neighbors = 1
	top_neighbors_df = find_top_n_neighbors(user_similarity_df, n_neighbors=n_neighbors)
	ratings_pred = predict_ratings_with_neighbors(
		ratings_matrix, user_similarity_df, top_neighbors_df
	)
	ratings_pred_df = pd.DataFrame(
		ratings_pred, index=ratings_matrix.index, columns=ratings_matrix.columns
	)
	print(top_neighbors_df)
	print('ratings_pred_df\n', ratings_pred_df)
	return ratings_pred_df


if __name__ == '__main__':
	main()
