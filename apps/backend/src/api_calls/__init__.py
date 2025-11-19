"""Module for management of the project."""

from .google_places import (
	get_one_attraction_by_id,
	get_places_for_city,
	get_restaurants_for_city,
	nearby_search,
)
from .wikipedia_description import get_summary_wikipedia_api
