import json
import logging
import os
import re
from collections import Counter
from typing import Any, Iterable

import requests

from src.data_model.places.places import Places
from src.constants import all_categories, default_categories, default_subcategories
from src.constants import dining_subcategories

SUMMARY_PROMPT = """
<ROLE>
    You are a travel summarizer. You must write a short factual summary of a trip from the provided places.
</ROLE>
<RULES>
    - Output a single paragraph, exactly 3 sentences, ~45-75 words.
    - Start with "On this trip, you will..." or "This trip includes..." and keep it summary-like.
    - Use periods to end each sentence; do not use semicolons; avoid abbreviations with periods.
    - Do not include "Day 1/Day 2" or numbered sections; never mirror day labels from input.
    - Ignore any "Day X" labels in the input; treat them only as grouping hints.
    - Do not include any place names or specific landmarks; do not use proper nouns except the city name.
    - Prefer describing categories of activities and overall atmosphere at a high level.
    - Use only the provided city and category mix; do not invent places or activities.
    - Avoid comma-separated lists; do not provide an itinerary.
    - Count sentences before output; if you have more or fewer than 3, revise to exactly 3.
</RULES>
<OUTPUT>
    A concise, factual, non-narrative summary of the trip in the provided city.
</OUTPUT>
"""


class Llama:
	# In Docker the LLM container is reachable as `llama`; override via LLAMA_API_URL for host runs.
	API_URL = os.getenv('LLAMA_API_URL', 'http://llama:3000/v1/chat/completions')
	# Allow long-running generations; override via LLAMA_API_TIMEOUT (seconds).
	API_TIMEOUT = float(os.getenv('LLAMA_API_TIMEOUT', '180'))

	CATEGORY_RULES = [
		(
			{
				'historical_landmark',
				'monument',
				'castle',
				'fort',
				'ruins',
				'archaeological_site',
			},
			'historic landmarks',
		),
		({'museum', 'art_gallery'}, 'museums and arts'),
		({'viewpoint', 'scenic_lookout', 'observation_deck'}, 'viewpoints'),
		({'park', 'garden', 'national_park', 'arboretum'}, 'parks and gardens'),
		({'beach', 'marina', 'pier', 'harbor', 'port'}, 'waterfront areas'),
		(
			{
				'church',
				'mosque',
				'synagogue',
				'hindu_temple',
				'place_of_worship',
				'cathedral',
			},
			'religious sites',
		),
		({'restaurant', 'cafe', 'bakery', 'bar', 'night_club'}, 'food and nightlife'),
		(
			{'shopping_mall', 'market', 'store', 'shopping_center', 'department_store'},
			'shopping and markets',
		),
		({'neighborhood', 'plaza', 'square'}, 'neighborhoods and public squares'),
		(
			{'theater', 'concert_hall', 'performing_arts_theater', 'cultural_center'},
			'cultural venues',
		),
		({'zoo', 'aquarium'}, 'wildlife attractions'),
		({'amusement_park', 'theme_park'}, 'family attractions'),
		({'tourist_attraction'}, 'sightseeing highlights'),
	]

	@staticmethod
	def _count_sentences(text: str) -> int:
		cleaned = ' '.join(text.strip().split())
		if not cleaned:
			return 0
		parts = re.split(r'(?<=[.!?])\s+', cleaned)
		return len([part for part in parts if part])

	@classmethod
	def _categorize_place(cls, place) -> str:
		types = set(place.types or [])
		if getattr(place, 'primaryType', ''):
			types.add(place.primaryType)
		for type_set, label in cls.CATEGORY_RULES:
			if types & type_set:
				return label
		return 'sightseeing highlights'

	@classmethod
	def _build_category_counts(cls, trip: list[Places]) -> Counter:
		counts = Counter()
		for day in trip:
			for place in day.get_list():
				counts[cls._categorize_place(place)] += 1
		return counts

	@staticmethod
	def _build_category_mix(counts: Counter) -> str:
		if not counts:
			return 'general sightseeing'
		items = [f'{label} ({count})' for label, count in counts.most_common(6)]
		return '; '.join(items)

	@staticmethod
	def _extract_place_names(trip: list[Places]) -> list[str]:
		names = []
		for day in trip:
			for place in day.get_list():
				name = getattr(place.placeInfo, 'displayName', '')
				if name:
					names.append(name)
		return names

	@staticmethod
	def _contains_place_name(text: str, names: list[str]) -> bool:
		lower_text = text.lower()
		for name in names:
			normalized = re.sub(r'[^a-z0-9 ]+', '', name.lower()).strip()
			if len(normalized) < 6:
				continue
			if normalized and normalized in lower_text:
				return True
		return False

	@staticmethod
	def _contains_unwanted_proper_noun(text: str, city: str) -> bool:
		cleaned = ' '.join(text.strip().split())
		city_tokens = {token.lower() for token in re.findall(r'\b[A-Za-z]+\b', city)}
		sentences = re.split(r'(?<=[.!?])\s+', cleaned)
		for sentence in sentences:
			tokens = re.findall(r'\b[A-Za-z]+\b', sentence)
			for token in tokens[1:]:
				if len(token) < 2:
					continue
				if token[0].isupper() and token.lower() not in city_tokens:
					return True
		return False

	@staticmethod
	def _word_count(text: str) -> int:
		return len(re.findall(r'\b\w+\b', text))

	@staticmethod
	def _needs_fallback(text: str, names: list[str], city: str) -> bool:
		if Llama._count_sentences(text) != 3:
			return True
		if re.search(r'\bDay\s+\d+', text):
			return True
		if Llama._contains_place_name(text, names):
			return True
		if Llama._contains_unwanted_proper_noun(text, city):
			return True
		word_count = Llama._word_count(text)
		return word_count < 45 or word_count > 75

	@staticmethod
	def _generate_template_summary(city: str, counts: Counter) -> str:
		primary = [label for label, _ in counts.most_common(4)]
		fallback = [
			'cultural sites',
			'scenic areas',
			'neighborhoods',
			'parks and gardens',
			'food spots',
		]
		for label in fallback:
			if len(primary) >= 3:
				break
			if label not in primary:
				primary.append(label)
		if not primary:
			primary = fallback[:3]
		cat_one = primary[0]
		cat_two = primary[1] if len(primary) > 1 else 'cultural sites'
		cat_three = primary[2] if len(primary) > 2 else 'scenic areas'
		return (
			f'On this trip, you will explore a mix of {cat_one} and {cat_two} with time for {cat_three}. '
			'The overall pace stays balanced and varied and blends cultural stops with relaxed movement through the city. '
			f'Expect a cohesive overview of {city} that highlights its atmosphere without focusing on individual locations.'
		)

	@classmethod
	def get_summary(cls, city: str, trip: list[Places]):
		category_counts = cls._build_category_counts(trip)
		category_mix = cls._build_category_mix(category_counts)
		place_names = cls._extract_place_names(trip)
		modified_messages = [
			{
				'content': SUMMARY_PROMPT,
				'role': 'system',
			}
		] + [
			{
				'content': f'City: {city}\nCategory mix: {category_mix}',
				'role': 'user',
			}
		]

		try:
			response = requests.post(
				cls.API_URL,
				json={
					'messages': modified_messages,
					'max_tokens': 180,
					'temperature': 0.2,
				},
			)

			content = cls._extract_llm_content(response)
			if not content:
				logging.warning('LLM returned empty summary content.')
				return ''
			if cls._needs_fallback(content, place_names, city):
				return cls._generate_template_summary(city, category_counts)
			return content
		except Exception as e:
			logging.exception(e.__str__())
			return ''

	@staticmethod
	def _normalize_preferences(raw: dict[str, Any]) -> dict[str, Any]:
		money = raw.get('money', 1)
		try:
			money = int(money)
		except (TypeError, ValueError):
			money = 1
		money = min(max(money, 0), 3)

		needs = raw.get('needs', [])
		if not isinstance(needs, list):
			needs = []
		allowed_needs = {
			'wheelchairAccessible',
			'goodForGroups',
			'vegan',
			'children',
			'alcohol',
			'allowsDogs',
		}
		needs = [need for need in needs if need in allowed_needs]

		categories_map = raw.get('categories', {})
		if not isinstance(categories_map, dict):
			categories_map = {}

		clean_categories: dict[str, list[str]] = {}
		for category, subcats in categories_map.items():
			if category not in all_categories:
				continue
			if not isinstance(subcats, list):
				subcats = []
			allowed_subcats = set(default_subcategories.get(category, []))
			clean_subcats = [
				subcat for subcat in subcats if subcat in allowed_subcats
			]
			clean_categories[category] = clean_subcats

		if not clean_categories:
			clean_categories = {category: [] for category in default_categories}

		restaurant_categories = raw.get('restaurant_categories', [])
		if not isinstance(restaurant_categories, list):
			restaurant_categories = []
		allowed_restaurants = set(dining_subcategories.keys())
		restaurant_categories = [
			category
			for category in restaurant_categories
			if category in allowed_restaurants
		]

		return {
			'money': money,
			'categories': clean_categories,
			'restaurant_categories': restaurant_categories,
			'needs': needs,
		}

	@staticmethod
	def _build_transcript_text(messages: Iterable[dict[str, Any]]) -> str:
		parts: list[str] = []
		for message in messages or []:
			if not isinstance(message, dict):
				continue
			role = str(message.get('role', 'unknown')).strip()
			content = str(message.get('content', '')).strip()
			if not content:
				continue
			parts.append(f'{role}: {content}')
		return '\n'.join(parts)

	@staticmethod
	def _safe_json_loads(text: str) -> Any | None:
		if not text or not text.strip():
			return None
		try:
			return json.loads(text)
		except json.JSONDecodeError:
			start = text.find('{')
			end = text.rfind('}')
			if start == -1 or end == -1 or end <= start:
				return None
			try:
				return json.loads(text[start:end + 1])
			except json.JSONDecodeError:
				return None

	@staticmethod
	def _extract_llm_content(response: requests.Response) -> str:
		if response.encoding is None:
			response.encoding = 'utf-8'
		response_text = response.text or ''
		response_dict: dict[str, Any] | None = None
		try:
			response_dict = response.json()
		except ValueError:
			parsed = Llama._safe_json_loads(response_text)
			if isinstance(parsed, dict):
				response_dict = parsed
		if not response_dict:
			return ''
		choices = response_dict.get('choices', [])
		if not choices:
			return ''
		message = choices[0].get('message', {})
		if not isinstance(message, dict):
			return ''
		content = message.get('content', '')
		return str(content).strip()

	@classmethod
	def get_preferences_from_text(cls, text: str) -> dict[str, Any]:
		categories_hint = ', '.join(all_categories)
		prompt = (
			'You are a travel preferences extractor. Return JSON only with keys: '
			'money (0-3 integer), categories (object mapping category to subcategories array), '
			'restaurant_categories (array), needs (array of '
			'[wheelchairAccessible, goodForGroups, vegan, children, alcohol, allowsDogs]). '
			f'Known categories: [{categories_hint}]. '
			'Use only known categories and subcategories. If unsure, leave empty arrays.'
		)
		try:
			response = requests.post(
				cls.API_URL,
				json={
					'messages': [
						{'role': 'system', 'content': prompt},
						{'role': 'user', 'content': text},
					],
					'max_tokens': 300,
					'temperature': 0.2,
				},
				timeout=cls.API_TIMEOUT,
			)
			content = cls._extract_llm_content(response)
			if not content:
				logging.warning('LLM returned empty preferences content.')
				return cls._normalize_preferences({})
			parsed = cls._safe_json_loads(content)
			if not isinstance(parsed, dict):
				logging.warning('LLM preferences response is not valid JSON: %s', content[:200])
				return cls._normalize_preferences({})
			normalized = cls._normalize_preferences(parsed)
			return cls._apply_text_fallbacks(text, normalized)
		except Exception as exc:
			logging.exception(exc.__str__())
			return cls._normalize_preferences({})

	@staticmethod
	def _apply_text_fallbacks(text: str, normalized: dict[str, Any]) -> dict[str, Any]:
		if not text:
			return normalized
		lowered = text.lower()
		categories = normalized.get('categories', {})
		if categories == {category: [] for category in default_categories}:
			nightlife_markers = [
				'club',
				'clubbing',
				'nightlife',
				'dj',
				'party',
				'rave',
				'dancefloor',
				'bas',
				'imprez',
				'klub',
				'noc',
				'parkiet',
				'neon',
			]
			if any(marker in lowered for marker in nightlife_markers):
				normalized['categories'] = {'night_club': []}
		return normalized

	@classmethod
	def get_preferences_from_messages(cls, messages: list[dict[str, Any]]) -> dict[str, Any]:
		text = cls._build_transcript_text(messages)
		return cls.get_preferences_from_text(text)
