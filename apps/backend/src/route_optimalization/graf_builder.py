import matplotlib.pyplot as plt
import networkx as nx

from src.route_optimalization.haversine import calculate_distance


class Graph:
	"""Class that represents a graph."""

	def __init__(self, nodes):
		self.nodes = nodes
		self.size = len(nodes)
		self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
		self.node_index = {node: i for i, node in enumerate(nodes)}

	def add_edge(self, u, v, weight):
		"""Function that adds an edge to the graph."""
		u_index = self.node_index[u]
		v_index = self.node_index[v]
		self.matrix[u_index][v_index] = weight
		self.matrix[v_index][u_index] = weight

	def print_matrix(self):
		"""Function that prints the graph's adjacency matrix."""
		print('   ', '  '.join(self.nodes))

		for i, row in enumerate(self.matrix):
			print(self.nodes[i], row)


def initialize_graph(places):
	"""Function that initializes a graph based on the list of tourist attractions.
	:param places: list of tourist attractions id: str, lat: float, lng: float
	:return: graph
	"""
	nodes = [place['id'] for place in places]
	graph = Graph(nodes)
	for idx, place in enumerate(places):
		for j in places[idx + 1 :]:
			graph.add_edge(
				place['id'],
				j['id'],
				calculate_distance(place['lat'], place['lng'], j['lat'], j['lng']),
			)
	graph.print_matrix()
	return graph


def visualize_graph(graph):
	"""Function that visualizes the graph using the networkx library."""
	G = nx.Graph()
	for i in range(graph.size):
		for j in range(graph.size):
			if graph.matrix[i][j] > 0:
				G.add_edge(graph.nodes[i], graph.nodes[j], weight=graph.matrix[i][j])

	pos = nx.spring_layout(G)
	nx.draw_networkx_nodes(G, pos, node_size=700)
	nx.draw_networkx_edges(G, pos, width=6)
	nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
	edge_labels = nx.get_edge_attributes(G, 'weight')
	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
	plt.axis('off')
	plt.show()
