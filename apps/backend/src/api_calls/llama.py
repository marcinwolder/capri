import json
import logging
import os

import requests

from src.data_model.places.places import Places

SUMMARY_PROMPT = """
<ROLE>
    You are a travel summarizer. You must write a short factual summary of a trip from the provided places.
</ROLE>
<RULES>
    - Output a single paragraph, exactly 3 sentences, ~45-75 words.
    - Start with "On this trip, you will..." or "This trip includes..." and keep it summary-like.
    - Do not include "Day 1/Day 2" or numbered sections; never mirror day labels from input.
    - Ignore any "Day X" labels in the input; treat them only as grouping hints.
    - Do not list place names; allow at most 1-2 place names total for flavor when helpful.
    - Prefer describing categories of activities and overall atmosphere at a high level.
    - Use only the provided city and trip content; do not invent places or activities.
    - Avoid comma-separated lists; do not provide an itinerary.
    - Keep to the provided names and city.
</RULES>
<OUTPUT>
    A concise, factual, non-narrative summary of the trip in the provided city.
</OUTPUT>
"""


class Llama:
	# In Docker the LLM container is reachable as `llama`; override via LLAMA_API_URL for host runs.
	API_URL = os.getenv('LLAMA_API_URL', 'http://llama:3000/v1/chat/completions')

	@classmethod
	def get_summary(cls, city: str, trip: list[Places]):
		trip_groups = []
		for day in trip:
			day_places = ', '.join(
				place.placeInfo.displayName for place in day.get_list()
			)
			if day_places:
				trip_groups.append(day_places)
		trip_str = '; '.join(trip_groups)
		modified_messages = [
			{
				'content': SUMMARY_PROMPT,
				'role': 'system',
			}
		] + [{'content': f'City: {city}, Places: {trip_str}', 'role': 'user'}]

		try:
			response = requests.post(
				cls.API_URL,
				json={
					'messages': modified_messages,
					'max_tokens': 140,
					'temperature': 0.3,
				},
			)

			if response.encoding is None:
				response.encoding = 'utf-8'

			response_dict = json.loads(response.text)
			return response_dict['choices'][0]['message']['content']
		except Exception as e:
			logging.exception(e.__str__())
			return ''
