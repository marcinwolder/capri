from src.ml_operations import get_cluster_centres


def test_get_cluster_centres():
    coordinates = [[{'id': 1, 'lat': 50.06143, 'lng': 19.93658},
                  {'id': 2, 'lat': 50.06143, 'lng': 19.93658},
                  {'id': 3, 'lat': 50.06143, 'lng': 19.93658}]]

    center_location = get_cluster_centres(coordinates)
    assert center_location == [[50.06143, 19.93658]]

