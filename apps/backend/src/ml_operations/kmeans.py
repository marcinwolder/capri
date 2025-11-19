import logging

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

from src.data_model.places.places import Places


def kmens_plot(data, cluster_labels, cluster_centers, labels):
	"""Plotting the clusters correctly"""
	plt.scatter(data[:, 1], data[:, 0], c=cluster_labels, cmap='viridis')
	plt.scatter(cluster_centers[:, 1], cluster_centers[:, 0], c='red', marker='X')

	for i, label in enumerate(labels):
		plt.annotate(label, (data[i][1], data[i][0]))

	plt.xlabel('Longitude')
	plt.ylabel('Latitude')
	plt.title('K-Means Clustering of Cities with Correct Geographic Representation')
	plt.show()


def kmeans_clustering(places: Places, days: int = 3) -> list[Places]:
	"""Performs K-Means Clustering on a list of places to group them based on geographic proximity.

	:param places: List of Place objects.
	:param days: Number of clusters (days) for the K-Means algorithm.
	:return: A list of clusters, each containing places' IDs, latitudes, and longitudes.
	"""
	if not places or days <= 0 or len(places) < days:
		logging.error('Invalid input data or number of days.')
		return []

	coordinates = np.array(
		[
			[place.location.latitude, place.location.longitude]
			for place in places.get_list()
		]
	)
	place_ids = [place.placeInfo.id for place in places.get_list()]

	kmeans = KMeans(n_clusters=days)
	kmeans.fit(coordinates)
	cluster_labels = kmeans.labels_

	places_ids_list = [[] for _ in range(days)]
	for place_id, cluster_label in zip(place_ids, cluster_labels):
		places_ids_list[cluster_label].append(place_id)

	trips = [
		places.create_new_places_with_id_list(places_ids)
		for places_ids in places_ids_list
	]

	return trips
