from src.recommendation import calculate_nearest_place


def test():
    user_location = [50.06143, 19.93658]
    places = [
        {'id': '1', 'lat': 50.06143, 'lng': 19.93658},
        {'id': '2', 'lat': 50.06143, 'lng': 19.93658},
        {'id': '3', 'lat': 50.06143, 'lng': 19.93658},
        {'id': '4', 'lat': 50.06143, 'lng': 19.93658},
        {'id': '5', 'lat': 50.06143, 'lng': 19.93658},
    ]
    nearest_place = calculate_nearest_place(user_location, places)
    assert nearest_place['id'] == '1'
    assert nearest_place['lat'] == 50.06143
    assert nearest_place['lng'] == 19.93658

    user_location = [50.06143, 19.93658]
    places = [
        {'id': '1', 'lat': 50.06143, 'lng': 19.93658},
        {'id': '2', 'lat': 50.06143, 'lng': 19.93658},
        {'id': '3', 'lat': 50.06143, 'lng': 19.93658},
        {'id': '4', 'lat': 50.06143, 'lng': 19.93658},
        {'id': '5', 'lat': 50.06143, 'lng': 19.93658},
    ]
    nearest_place = calculate_nearest_place(user_location, places)
    assert nearest_place['id'] == '1'
    assert nearest_place['lat'] == 50.06143
    assert nearest_place['lng'] == 19.93658
