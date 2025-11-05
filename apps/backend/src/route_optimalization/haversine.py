import math
from typing import List, Dict, Union
from numpy import Infinity


def calculate_distance(lat1, lng1, lat2, lng2) -> float:
    """Calculate distance between two points on Earth.
    Uses Haversine formula. Returns distance in kilometers.
    """
    earth_radius = 6371.0
    lng1, lat1, lng2, lat2 = float(lng1), float(lat1), float(lng2), float(lat2)
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)

    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = earth_radius * c
    return distance


def calculate_nearest_place(user_location, places: List[dict]) -> Dict[str, Union[str, float]]:
    """Calculate the nearest place to the user."""
    min_distance = Infinity
    nearest_place = None
    for place in places:
        id, lat, lng = place['id'], place['lat'], place['lng']  
        distance = calculate_distance(user_location[0], user_location[1],
                                      lat, lng)
        if distance < min_distance:
            min_distance = distance
            nearest_place = place
    return nearest_place

