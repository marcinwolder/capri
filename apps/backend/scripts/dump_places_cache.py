#!/usr/bin/env python3
"""Prefetch Google Places data and save it to the local cache."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from src.api_calls.google_places import get_places_for_city  # noqa: E402
from src.data_model.city.city import City  # noqa: E402
from src.data_model.place.place import PlaceCreatorAPI  # noqa: E402
from src.data_model.place.place_visitor import PlaceVisitor  # noqa: E402
from src.database import DataBase  # noqa: E402


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Dump Google Places cache for destination cities.'
    )
    parser.add_argument(
        '--env-file',
        default=str(BACKEND_ROOT / '.env'),
        help='Path to .env file containing GOOGLE_PLACES_API_KEY.',
    )
    parser.add_argument(
        '--cities-file',
        default=str(
            BACKEND_ROOT
            .parent
            / 'frontend'
            / 'src'
            / 'app'
            / 'constants'
            / 'cities.json'
        ),
        help='Path to cities.json list of destinations.',
    )
    parser.add_argument(
        '--data-dir',
        help='Override DATA_DIR for cache output.',
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing cached cities.',
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=0,
        help='Process only the first N cities (0 = no limit).',
    )
    parser.add_argument(
        '--city-ids',
        nargs='*',
        type=int,
        default=None,
        help='Optional list of city ids to process.',
    )
    parser.add_argument(
        '--sleep',
        type=float,
        default=0.0,
        help='Sleep between cities in seconds.',
    )
    parser.add_argument(
        '--retries',
        type=int,
        default=2,
        help='Retries per city on failure.',
    )
    parser.add_argument(
        '--backoff',
        type=float,
        default=2.0,
        help='Base backoff seconds for retry delays.',
    )
    parser.add_argument(
        '--failures-file',
        default=None,
        help='Write failed city ids to this JSON file.',
    )
    return parser.parse_args()


def _load_cities(path: Path) -> list[dict]:
    with path.open('r', encoding='utf-8') as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError('cities.json must be a list of objects.')
    return payload


def _iter_cities(
    cities: list[dict], limit: int, city_ids: list[int] | None
) -> Iterable[dict]:
    count = 0
    for entry in cities:
        if city_ids is not None:
            if entry.get('id') not in city_ids:
                continue
        yield entry
        count += 1
        if limit and count >= limit:
            return


def _fetch_city(
    db: DataBase,
    city: City,
    retries: int,
    backoff: float,
) -> tuple[bool, str | int]:
    for attempt in range(retries + 1):
        try:
            places = get_places_for_city(
                db, city, placeCreator=PlaceCreatorAPI, placeVisitor=PlaceVisitor
            )
            if places.count == 0:
                raise ValueError('No places returned from API.')
            return True, places.count
        except Exception as exc:
            if attempt >= retries:
                return False, str(exc)
            delay = backoff * (2**attempt)
            logging.warning(
                'Retrying city %s after error (%s). Sleeping %.1fs.',
                city.id,
                exc,
                delay,
            )
            time.sleep(delay)
    return False, 'Unknown error'


def main() -> int:
    args = _parse_args()
    load_dotenv(args.env_file)
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        logging.error(
            'GOOGLE_PLACES_API_KEY is required in %s.',
            args.env_file,
        )
        return 2
    os.environ['GOOGLE_PLACES_API_KEY'] = api_key

    if args.data_dir:
        os.environ['DATA_DIR'] = args.data_dir

    cities_path = Path(args.cities_file).expanduser().resolve()
    if not cities_path.exists():
        logging.error('cities.json not found at %s', cities_path)
        return 2

    logging.info('Loading cities from %s', cities_path)
    cities = _load_cities(cities_path)
    db = DataBase()

    success = 0
    skipped = 0
    failures: list[dict] = []

    for entry in _iter_cities(cities, args.limit, args.city_ids):
        city_id = entry.get('id')
        if not city_id:
            continue
        city = City(city_id)

        if db.check_if_city_exist(city) and not args.overwrite:
            skipped += 1
            logging.info('Skip city %s (cache exists).', city_id)
            continue

        ok, detail = _fetch_city(db, city, args.retries, args.backoff)
        if ok:
            success += 1
            logging.info('Cached city %s (%s places).', city_id, detail)
        else:
            failures.append({'id': city_id, 'error': detail})
            logging.error('Failed city %s: %s', city_id, detail)

        if args.sleep:
            time.sleep(args.sleep)

    logging.info(
        'Done. success=%s skipped=%s failed=%s',
        success,
        skipped,
        len(failures),
    )

    if failures:
        failures_path = (
            Path(args.failures_file)
            if args.failures_file
            else BACKEND_ROOT / 'cache_failures.json'
        )
        with failures_path.open('w', encoding='utf-8') as handle:
            json.dump(failures, handle, indent=2)
        logging.info('Wrote failures to %s', failures_path)
    return 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    raise SystemExit(main())
