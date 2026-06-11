from src.recommendation_wibit.engine import (
    build_visit_order,
    cycle_to_open_path_by_removing_max_edge,
    enforce_triangle_inequality_metric_closure,
    solve_open_tsp_bruteforce,
    symmetrize_cost_matrix_avg,
)


def test_symmetrize_cost_matrix_avg_uses_mean_for_asymmetric_edges():
    directed = [
        [0.0, 10.0, 4.0],
        [6.0, 0.0, 8.0],
        [2.0, 12.0, 0.0],
    ]
    sym = symmetrize_cost_matrix_avg(directed)
    assert sym[0][1] == 8.0
    assert sym[1][0] == 8.0
    assert sym[1][2] == 10.0
    assert sym[2][1] == 10.0
    assert sym[0][0] == 0.0


def test_metric_closure_fixes_triangle_inequality():
    matrix = [
        [0.0, 3.0, 10.0],
        [3.0, 0.0, 4.0],
        [10.0, 4.0, 0.0],
    ]
    fixed = enforce_triangle_inequality_metric_closure(matrix)
    assert fixed[0][2] == 7.0
    assert fixed[2][0] == 7.0
    assert fixed[0][2] <= fixed[0][1] + fixed[1][2]


def test_cycle_to_open_path_removes_max_edge():
    graph = [
        [0.0, 1.0, 5.0, 1.0],
        [1.0, 0.0, 1.0, 5.0],
        [5.0, 1.0, 0.0, 1.0],
        [1.0, 5.0, 1.0, 0.0],
    ]
    cycle = [0, 1, 2, 3]
    path = cycle_to_open_path_by_removing_max_edge(cycle, graph)
    assert len(path) == 4
    assert set(path) == {0, 1, 2, 3}
    assert path in ([1, 2, 3, 0], [0, 3, 2, 1])


def test_bruteforce_finds_best_open_path():
    graph = [
        [0.0, 1.0, 10.0, 10.0],
        [1.0, 0.0, 1.0, 10.0],
        [10.0, 1.0, 0.0, 1.0],
        [10.0, 10.0, 1.0, 0.0],
    ]
    order = solve_open_tsp_bruteforce(graph)
    assert order in ([0, 1, 2, 3], [3, 2, 1, 0])


def test_build_visit_order_falls_back_on_anomalous_matrix():
    graph = [
        [0.0, 1.0, 2.0, 3.0],
        [1.0, 0.0, -4.0, 5.0],
        [2.0, -4.0, 0.0, 6.0],
        [3.0, 5.0, 6.0, 0.0],
    ]
    order = build_visit_order(graph)
    assert len(order) == 4
    assert set(order) == {0, 1, 2, 3}
