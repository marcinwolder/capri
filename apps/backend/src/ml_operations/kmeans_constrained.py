import numpy as np


def initialize_centroids_kmeans_plusplus(data, k):
    n, features = data.shape
    centroids = np.zeros((k, features))
    
    initial_idx = np.random.choice(n)
    centroids[0] = data[initial_idx]

    for i in range(1, k):
        
        distances = np.array([min([np.linalg.norm(x - c) for c in centroids[:i]]) for x in data])
        
        probabilities = distances ** 2 / np.sum(distances ** 2)
        
        centroids[i] = data[np.random.choice(n, p=probabilities)]

    return centroids


def constrained_kmeans(data, k, fixed_clusters, flexible_clusters, max_iter=100):
    n, features = data.shape
    cluster_assignment = np.full(n, -1)
    for idx, cluster in fixed_clusters.items():
        cluster_assignment[idx] = cluster

    
    centroids = initialize_centroids_kmeans_plusplus(data, k)

    
    for _ in range(max_iter):
        
        spatial_distances = np.sqrt(((data[:, np.newaxis, :-1] - centroids[:, :-1]) ** 2).sum(axis=2))

        
        for i in range(n):
            if i in flexible_clusters:
                valid_clusters = flexible_clusters[i]
                valid_distances = spatial_distances[i, valid_clusters]
                cluster_assignment[i] = valid_clusters[np.argmin(valid_distances)]
            elif i not in fixed_clusters:
                cluster_assignment[i] = np.argmin(spatial_distances[i])

        
        new_centroids = np.array(
            [data[cluster_assignment == i].mean(axis=0) if np.any(cluster_assignment == i) else centroids[i] for i in
             range(k)])
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids

    w_averages = np.array([data[cluster_assignment == i, -1].mean() for i in range(k)])
    return centroids, cluster_assignment, w_averages
