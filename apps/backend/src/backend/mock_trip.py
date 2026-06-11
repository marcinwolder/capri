import csv
from pathlib import Path
from uuid import uuid4


DEFAULT_MOCK_TRIPS_DIR = Path(__file__).resolve().parents[2] / 'data' / 'mock_trips'
DEFAULT_CITY_ID = 'mock-city'
DEFAULT_CITY_NAME = 'Mock City'
DEFAULT_SUMMARY = 'Sample itinerary loaded from CSV.'


def _parse_int(value: str | None, default: int = 0) -> int:
	if value is None or value == '':
		return default
	return int(value)


def _parse_float(value: str | None, default: float = 0.0) -> float:
	if value is None or value == '':
		return default
	return float(value)


def _get_mock_trip_path(file_name: str, base_path: Path | None = None) -> Path:
	mock_dir = (base_path or DEFAULT_MOCK_TRIPS_DIR).resolve()
	path = (mock_dir / file_name).resolve()
	if path.parent != mock_dir:
		raise ValueError('Invalid mock CSV path.')
	if path.suffix.lower() != '.csv':
		raise ValueError('Mock trip file must be a CSV.')
	if not path.exists():
		raise FileNotFoundError(f'Mock trip file not found: {file_name}')
	return path


def load_mock_trip(file_name: str, base_path: Path | None = None) -> dict:
	path = _get_mock_trip_path(file_name, base_path=base_path)
	with open(path, 'r', encoding='utf-8', newline='') as handle:
		rows = list(csv.DictReader(handle))

	if not rows:
		raise ValueError('Mock trip CSV is empty.')

	required_columns = {'day_number', 'place_order', 'place_name'}
	missing_columns = required_columns - set(rows[0].keys())
	if missing_columns:
		raise ValueError(
			f'Mock trip CSV is missing required columns: {", ".join(sorted(missing_columns))}'
		)

	sorted_rows = sorted(
		rows,
		key=lambda row: (
			_parse_int(row.get('day_number')),
			_parse_int(row.get('place_order')),
		),
	)

	first_row = sorted_rows[0]
	city_id = first_row.get('city_id') or DEFAULT_CITY_ID
	city_name = first_row.get('city_name') or DEFAULT_CITY_NAME
	summary = first_row.get('summary') or DEFAULT_SUMMARY
	dates = [
		date_value
		for date_value in dict.fromkeys(
			row.get('date') for row in sorted_rows if row.get('date')
		)
	]

	days_map: dict[int, dict] = {}
	for row in sorted_rows:
		day_number = _parse_int(row.get('day_number'))
		if day_number <= 0:
			raise ValueError('day_number must be a positive integer.')

		day_entry = days_map.setdefault(
			day_number,
			{
				'places': [],
				'weather': _parse_int(row.get('weather_code')),
			},
		)
		if not day_entry['weather'] and row.get('weather_code'):
			day_entry['weather'] = _parse_int(row.get('weather_code'))

		travel_minutes = row.get('travel_minutes_from_prev')
		travel_mode = row.get('travel_mode_from_prev')
		transportation = None
		if travel_minutes not in (None, '') or travel_mode not in (None, ''):
			transportation = [_parse_int(travel_minutes), travel_mode or 'walking']

		place_slug = row.get('place_id') or f'd{day_number}-p{_parse_int(row.get("place_order"))}'
		day_entry['places'].append(
			{
				'id': place_slug,
				'name': row.get('place_name', '').strip(),
				'description': (row.get('description') or '').strip(),
				'formattedAddress': (row.get('formatted_address') or '').strip(),
				'types': [],
				'price': 0,
				'rating': 0,
				'reviews': 0,
				'image': {'name': '', 'url': '', 'widthPx': 0, 'heightPx': 0},
				'googleMapsUri': (row.get('google_maps_uri') or '').strip(),
				'latitude': _parse_float(row.get('latitude')),
				'longitude': _parse_float(row.get('longitude')),
				'transportation': transportation,
			}
		)

	days = [days_map[day_number] for day_number in sorted(days_map)]
	return {
		'id': f'mock-{path.stem}-{uuid4().hex[:8]}',
		'city_id': city_id,
		'city_name': city_name,
		'summary': summary,
		'dates': dates,
		'days': days,
		'is_mock': True,
	}
