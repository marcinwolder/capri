def divide_text_to_sentences(text: str, nlp):
	"""Function that divides text into sentences."""
	sentences = [sentence.text for sentence in nlp(text).sents]
	return sentences


def process_sentiment_data(sentiment_data):
	list_of_aspects = []

	for lst in sentiment_data:
		for idx, j in enumerate(lst['aspect']):
			if lst['sentiment'][idx] == 'Negative':
				lst['sentiment'][idx] = -1
			elif lst['sentiment'][idx] == 'Neutral':
				lst['sentiment'][idx] = 0
			elif lst['sentiment'][idx] == 'Positive':
				lst['sentiment'][idx] = 1
			list_of_aspects.append((j, lst['sentiment'][idx]))
			print(j, lst['sentiment'][idx])
	return list_of_aspects
