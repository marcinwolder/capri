"""Module for management of the project."""
from .google_places import (get_one_attraction_by_id, nearby_search,
                            get_restaurants_for_city, get_places_for_city)
from .wikipedia_description import get_summary_wikipedia_api
