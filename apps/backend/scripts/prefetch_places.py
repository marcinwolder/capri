"""CLI helper for creating offline places JSON files.

This script fetches Places data for a list of city identifiers using the
existing Google Places integration and persists the normalized payload into the
`apps/backend/data/places` directory (or any directory provided through
``--data-dir``). Shipping those JSON files with the backend lets the API serve
recommendations without hitting Google Places at runtime.

Usage examples:
    # Fetch Krakow (1616172264) and Paris (2988507) into the default data dir
    python -m scripts.prefetch_places --city 1616172264 --city 2988507

    # Read a list of ids from a text file and overwrite existing exports
    python -m scripts.prefetch_places --city-file ./cities.txt --force
"""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Iterable, Sequence

from dotenv import load_dotenv

from src.api_calls.google_places import get_places_for_city
from src.data_model.city.city import City
from src.data_model.place.place import PlaceCreatorAPI
from src.data_model.place.place_visitor import PlaceVisitor
from src.database import DataBase

load_dotenv()

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / 'data'


def _parse_city_tokens(raw_values: Iterable[str]) -> list[int]:
    """Normalize multiple tokens (commas, whitespace) into unique ids."""
    city_ids: list[int] = []
    seen: set[int] = set()
    for raw in raw_values:
        for token in str(raw).replace(',', ' ').split():
            if not token:
                continue
            try:
                city_id = int(token)
            except ValueError as exc:  # pragma: no cover - defensive guardrail
                raise SystemExit(f'Invalid city id "{token}". Use integers only.') from exc
            if city_id not in seen:
                city_ids.append(city_id)
                seen.add(city_id)
    return city_ids


def _load_city_ids(args: argparse.Namespace) -> list[int]:
    tokens: list[str] = []
    if args.cities:
        tokens.extend(args.cities)
    if args.city_file:
        file_path = args.city_file.expanduser().resolve()
        if not file_path.exists():
            raise SystemExit(f'City file "{file_path}" was not found.')
        tokens.extend(file_path.read_text(encoding='utf-8').splitlines())

    if not tokens:
        raise SystemExit('Provide at least one city id via --city or --city-file.')

    return _parse_city_tokens(tokens)


def _ensure_api_key():
    if not os.getenv('GOOGLE_PLACES_API_KEY'):
        raise SystemExit(
            'GOOGLE_PLACES_API_KEY is missing. Export the key or place it in apps/backend/.env.'
        )


def _configure_logging(level: str):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='%(asctime)s %(levelname)s %(message)s',
    )


def fetch_city_data(
    db: DataBase, city_id: int, force: bool = False, save_raw: bool = False
) -> bool:
    """Fetch and persist data for a single city. Returns True on success."""
    city = City(city_id)
    if not force and db.check_if_city_exist(city):
        logging.info(
            'Skipping %s (%s) because a cached file already exists. Use --force to refresh.',
            city.name,
            city.id,
        )
        return False

    logging.info('Fetching Google Places data for %s (%s)...', city.name, city.id)
    places = get_places_for_city(
        db=db,
        city=city,
        placeCreator=PlaceCreatorAPI,
        placeVisitor=PlaceVisitor,
        save_raw=save_raw,
    )
    logging.info(
        'Saved %s places for %s (%s).',
        places.count,
        city.name,
        city.id,
    )
    return True


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Pre-fetch Google Places results and persist them to JSON.'
    )
    parser.add_argument(
        '--city',
        dest='cities',
        action='append',
        metavar='CITY_ID',
        help='City id from src/constants/worldcities/worldcities.csv. Can be repeated.',
    )
    parser.add_argument(
        '--city-file',
        type=Path,
        help='Path to a file with one city id per line (commas and whitespace are ignored).',
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=None,
        help=f'Output directory for the data cache (default: "{DEFAULT_DATA_DIR}").',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Re-fetch data even if a cached JSON file already exists.',
    )
    parser.add_argument(
        '--save-raw',
        action='store_true',
        help='Also dump the raw Google Places payload to data/raw.json for inspection.',
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Verbosity for the script logging output.',
    )

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None):
    args = parse_args(argv)
    _configure_logging(args.log_level)
    _ensure_api_key()

    if args.data_dir:
        target_dir = args.data_dir.expanduser().resolve()
        os.environ['DATA_DIR'] = str(target_dir)
        logging.debug('Overriding DATA_DIR with %s', target_dir)
    else:
        target_dir = DEFAULT_DATA_DIR

    db = DataBase(base_path=target_dir)
    city_ids = _load_city_ids(args)

    successful, skipped = 0, 0
    for city_id in city_ids:
        try:
            if fetch_city_data(db, city_id, force=args.force, save_raw=args.save_raw):
                successful += 1
            else:
                skipped += 1
        except Exception as exc:  # pragma: no cover - defensive top-level guard
            logging.exception('Failed to fetch data for city %s: %s', city_id, exc)

    logging.info(
        'Finished processing %s cities (%s updated, %s skipped).',
        len(city_ids),
        successful,
        skipped,
    )


if __name__ == '__main__':
    main()
