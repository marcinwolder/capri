from src.route_optimalization import dijkstra, initialize_graph


def test():
	nodes = ['1', '2', '3', '4', '5']
	graph = initialize_graph(nodes)
	graph.add_edge('1', '2', 1)
	graph.add_edge('1', '3', 2)
	graph.add_edge('2', '3', 3)
	graph.add_edge('3', '4', 4)
	graph.add_edge('4', '5', 5)
	graph.add_edge('5', '1', 6)
	graph.add_edge('5', '2', 7)
	graph.add_edge('5', '3', 8)
	graph.add_edge('5', '4', 9)
	graph.print_matrix()
	path = dijkstra(graph, '1')
	assert path == {'1': 0, '2': 1, '3': 2, '4': 6, '5': 7}
	path = dijkstra(graph, '2')
	assert path == {'1': 1, '2': 0, '3': 3, '4': 7, '5': 8}
	path = dijkstra(graph, '3')
	assert path == {'1': 2, '2': 3, '3': 0, '4': 4, '5': 5}
	path = dijkstra(graph, '4')
	assert path == {'1': 6, '2': 7, '3': 4, '4': 0, '5': 1}
	path = dijkstra(graph, '5')
	assert path == {'1': 7, '2': 8, '3': 5, '4': 1, '5': 0}
