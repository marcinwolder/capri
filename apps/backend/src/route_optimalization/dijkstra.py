import sys


def dijkstra(graph, start_vertex_name) -> dict:
    """Function that calculates the shortest path
    from the starting vertex to all other vertices in the graph"""
    start_vertex = graph.node_index[start_vertex_name]
    n = graph.size
    visited = [False] * n
    distance = [sys.maxsize] * n
    distance[start_vertex] = 0

    for _ in range(n):
        u = min_distance(distance, visited)
        visited[u] = True

        for v in range(n):
            if (graph.matrix[u][v] > 0 and not visited[v] and
                    distance[v] > distance[u] + graph.matrix[u][v]):
                distance[v] = distance[u] + graph.matrix[u][v]

    return {graph.nodes[i]: distance[i] for i in range(n)}


def min_distance(distance, visited: list) -> int:
    """Function that returns the index of the vertex with the smallest distance."""
    min_val = sys.maxsize
    min_index = -1

    for i, _ in enumerate(distance):
        if distance[i] < min_val and not visited[i]:
            min_val = distance[i]
            min_index = i

    return min_index

