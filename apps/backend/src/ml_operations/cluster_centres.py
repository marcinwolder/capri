import numpy as np


def get_cluster_centres(data):
	"""Calculate cluster centres for given data.
	:param data: list of lists of dict { 'ids': ids, 'lat': lat, 'lng': lng}
	:return: list of cluster centres
	"""
	centers_for_days = []
	for day in data:
		coordinates = []
		for place in day:
			coordinates.append([place['lat'], place['lng']])
		coordinates = np.array(coordinates)
		mean_lat, mean_lng = np.mean(coordinates, axis=0)
		centers_for_days.append([mean_lat, mean_lng])
	return centers_for_days
