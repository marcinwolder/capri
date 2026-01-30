import csv
import logging
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

from src.constants import all_categories
from src.data_model.place.place import Place
from src.data_model.places.places import Places
from src.data_model.user.user_preferences import UserPreferences
from src.route_optimalization.haversine import calculate_distance
from src.travel_time import travel_estimator
from src.path import get_path

DEFAULT_DAY_START_MIN = 600
DEFAULT_DAY_END_MIN = 22 * 60


def weekday_indices_from_dates(start: date, end: date) -> list[int]:
	current_date = start
	weekdays: list[int] = []
	while current_date <= end:
		weekday_index = (current_date.weekday() + 1) % 7
		weekdays.append(weekday_index)
		current_date += timedelta(days=1)
	return weekdays


def _normalize_places_by_day(
	places_by_day: Iterable[Places] | Iterable[Iterable[Place]],
) -> list[list[Place]]:
	if not places_by_day:
		return []
	places_by_day_list = list(places_by_day)
	if not places_by_day_list:
		return []
	first = places_by_day_list[0]
	if isinstance(first, Places):
		return [day.get_list() for day in places_by_day_list]
	return [list(day) for day in places_by_day_list]


def _pairwise_distance_km(places: list[Place]) -> float:
	count = 0
	if len(places) < 2:
		return 0.0
	acc = 0.0
	for i in range(len(places)):
		for j in range(i + 1, len(places)):
			place_a = places[i]
			place_b = places[j]
			acc += calculate_distance(
				place_a.location.latitude,
				place_a.location.longitude,
				place_b.location.latitude,
				place_b.location.longitude,
			)
			count += 1
	return acc / count if count else 0.0


def _route_length_km(places: list[Place]) -> float:
	if len(places) < 2:
		return 0.0
	total = 0.0
	for idx in range(1, len(places)):
		prev_place = places[idx - 1]
		curr_place = places[idx]
		total += calculate_distance(
			prev_place.location.latitude,
			prev_place.location.longitude,
			curr_place.location.latitude,
			curr_place.location.longitude,
		)
	return total


def _preference_categories(preferences: UserPreferences | None) -> tuple[set[str], set[str]]:
	if preferences is None:
		return set(), set()
	categories = set(preferences.categories or [])
	from_subcategories: set[str] = set()
	for sub_list in preferences.subcategories.values():
		from_subcategories.update([item for item in sub_list if item])
	return categories, from_subcategories


def _avoid_categories(preferences: UserPreferences | None) -> set[str]:
	if preferences is None:
		return set()
	avoid = getattr(preferences, 'avoid_categories', None)
	if not avoid:
		return set()
	return {item for item in avoid if item}


def _place_category_tokens(place: Place) -> set[str]:
	tokens = set(place.types or [])
	primary = getattr(place, 'primaryType', '')
	if primary:
		tokens.add(primary)
	if place.subcategories:
		tokens.update(place.subcategories)
	return {token for token in tokens if token}


def _sentiment_alignment_percent(places: list[Place], preferences: UserPreferences | None) -> float:
	if not places:
		return 0.0
	categories, subcategories = _preference_categories(preferences)
	positive = categories | subcategories
	if not positive:
		return 0.0
	match_count = 0
	for place in places:
		if _place_category_tokens(place) & positive:
			match_count += 1
	return (match_count / len(places)) * 100.0


def _avoidance_rate(places: list[Place], preferences: UserPreferences | None) -> int:
	avoid = _avoid_categories(preferences)
	if not places or not avoid:
		return 0
	count = 0
	for place in places:
		if _place_category_tokens(place) & avoid:
			count += 1
	return count


def _diversity_score(places: list[Place], preferences: UserPreferences | None) -> float:
	if not places:
		return 0.0
	plan_categories: set[str] = set()
	for place in places:
		for token in _place_category_tokens(place):
			if token in all_categories:
				plan_categories.add(token)
	categories, subcategories = _preference_categories(preferences)
	source_categories = categories | subcategories
	source_count = len(source_categories)
	if source_count == 0:
		return 0.0
	return len(plan_categories) / source_count


def _temporal_conflicts(
	places: list[Place],
	weekday_index: int | None,
	day_start_min: int,
	day_end_min: int,
	city,
) -> int:
	if not places:
		return 0
	current_time = day_start_min
	conflicts = 0
	prev_place = None
	for place in places:
		if prev_place is not None:
			travel_minutes, _ = travel_estimator.get_estimated_time(
				prev_place.location,
				place.location,
				city,
			)
			current_time += int(travel_minutes)
		period_idx = weekday_index if weekday_index is not None else 0
		periods = place.regularOpeningHours.periods
		if period_idx >= len(periods):
			period_idx = 0
		period = periods[period_idx]
		open_min = period.open_in_minutes
		close_min = period.close_in_minutes
		estimated_time = place.estimatedTime
		if current_time < open_min or current_time + estimated_time > close_min:
			conflicts += 1
		current_time = max(current_time, open_min) + estimated_time
		if current_time > day_end_min:
			conflicts += 1
		prev_place = place
	return conflicts


def build_trip_day_metrics(
	places_by_day: Iterable[Places] | Iterable[Iterable[Place]],
	preferences: UserPreferences | None,
	weekday_indices: list[int] | None,
	city=None,
	day_start_minutes: int = DEFAULT_DAY_START_MIN,
	day_end_minutes: int = DEFAULT_DAY_END_MIN,
) -> list[dict[str, float | int]]:
	places_list = _normalize_places_by_day(places_by_day)
	metrics: list[dict[str, float | int]] = []
	for day_idx, places in enumerate(places_list):
		weekday_index = None
		if weekday_indices and day_idx < len(weekday_indices):
			weekday_index = weekday_indices[day_idx]
		metrics.append(
			{
				'day': day_idx + 1,
				'total_route_km': round(_route_length_km(places), 3),
				'time_conflicts': _temporal_conflicts(
					places,
					weekday_index,
					day_start_minutes,
					day_end_minutes,
					city,
				),
				'cluster_distance_km': round(_pairwise_distance_km(places), 3),
				'sentiment_alignment_pct': round(
					_sentiment_alignment_percent(places, preferences),
					2,
				),
				'avoidance_rate': _avoidance_rate(places, preferences),
				'diversity_score': round(_diversity_score(places, preferences), 3),
			}
		)
	return metrics


def write_trip_metrics_csv(
	trip_id: str,
	day_metrics: list[dict[str, float | int]],
	output_dir: Path | None = None,
) -> Path:
	if output_dir is None:
		output_dir = Path(get_path('metrics', 'logs'))
	output_dir.mkdir(parents=True, exist_ok=True)
	file_path = output_dir / f'{trip_id}.csv'
	fieldnames = [
		'day',
		'total_route_km',
		'time_conflicts',
		'cluster_distance_km',
		'sentiment_alignment_pct',
		'avoidance_rate',
		'diversity_score',
	]
	try:
		with open(file_path, 'w', newline='', encoding='utf-8') as handle:
			writer = csv.DictWriter(handle, fieldnames=fieldnames)
			writer.writeheader()
			for row in day_metrics:
				writer.writerow(row)
	except Exception as exc:
		logging.exception('Failed to write metrics CSV: %s', exc)
	return file_path
