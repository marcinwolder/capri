import json
import logging

import requests

from src.data_model.places.places import Places


class Llama:
	API_URL = 'http://localhost:3001/v1/chat/completions'

	@classmethod
	def get_summary(cls, city: str, trip: list[Places]):
		trip_str = ''
		for i, day in enumerate(trip):
			trip_str += f'Day {i + 1}: '
			for place in day.get_list():
				trip_str += f'{place.placeInfo.displayName}, '
		modified_messages = [
			{
				'content': """Create a vivid summary of a future trip based on a list of specific locations 
            provided by the user. Summary should be few paragraphs not a list.  
            The journey should encapsulate the essence of a city, weaving through its historical, 
            cultural, and spiritual landscapes. 
            Do not write anything that is not directly related to the task. Do not make introductions or conclusions.""",
				'role': 'system',
			}
		] + [{'content': f'City: {city}, Places: {trip_str}', 'role': 'user'}]

		try:
			response = requests.post(
				cls.API_URL,
				json={
					'messages': modified_messages,
					'max_tokens': 1000,
					'temperature': 0.5,
				},
			)

			if response.encoding is None:
				response.encoding = 'utf-8'

			response_dict = json.loads(response.text)
			return response_dict['choices'][0]['message']['content']
		except Exception as e:
			logging.exception(e.__str__())
			return ''
