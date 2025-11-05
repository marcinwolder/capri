from typing import List

import numpy as np
from sklearn.metrics import pairwise_distances_argmin

from src.data_model.place.place import Place


def assign_points_to_clusters(cluster_centers: List[List[float]], places: List[Place]):
    """
    Assign points to the nearest cluster center.

    Parameters:
    - cluster_centers: np.array with shape (n_clusters, n_features)
    - points: np.array with shape (n_points, n_features)

    Returns:
    - assignments: np.array with shape (n_points,), indices of the nearest cluster center
    """
    
    locations = []
    for place in places:
            locations.append([place.location.latitude, place.location.longitude])
    assignments = pairwise_distances_argmin(np.array(locations), np.array(cluster_centers))
    clusters = [[] for _ in range(len(cluster_centers))]
    for i in range(len(assignments)):
        clusters[assignments[i]].append(places[i])
    return clusters


