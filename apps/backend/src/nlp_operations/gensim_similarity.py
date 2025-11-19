"""Calculate similarity between words and categories using word2vec.
Cosine similarity is a measure of similarity between two non-zero vectors of
 an inner product space that measures the cosine of the angle between them.
Cosine similarity is particularly used in positive space, where the outcome is
neatly bounded in [0,1].
The word2vec model is trained on Google News dataset (about 100 billion words);
it contains 3 million words and phrases and was fit using 300-dimensional word vectors.
Gensim is a Python library for topic modelling, document indexing and similarity
retrieval with large corpora.
"""

import gensim

from src.constants import (
	all_categories,
	default_subcategories,
	dining,
	dining_subcategories,
)

# TODO: refactor


def calculate_similarity(
	words: list[tuple[str, int]], model: gensim.models.keyedvectors.Word2VecKeyedVectors
):
	"""Calculate similarity between words and categories using word2vec.

	param words:  list of tuples (word, sentiment)
	:return: list of tuples (category, sentiment) with calculated similarity
	"""
	### TODO: odrzucać słowa poniżej confidence 0.3
	### TODO: słowa z podkreślnikiem ????

	lst = []
	for word_with_sentiment in all_categories:
		if word_with_sentiment.find('_') != -1:
			continue
		lst.append(word_with_sentiment)
	lst.append('art gallery')

	map_words_to_categories = {}  # do debugowania
	categories_with_sentiment = []
	for word_with_sentiment in words:
		word_with_sentiment = word_with_sentiment[0]
		map_words_to_categories[word_with_sentiment] = [0, '']
		for category in lst:
			if (
				model.similarity(
					word_with_sentiment, category
				)  # a to nie powinno być model.wv.similarity('france', 'spain')?
				> map_words_to_categories[word_with_sentiment][0]
			):
				map_words_to_categories[word_with_sentiment][0] = model.similarity(
					word_with_sentiment, category
				)
				map_words_to_categories[word_with_sentiment][1] = category

	for word_with_sentiment in words:
		categories_with_sentiment.append(
			(map_words_to_categories[word_with_sentiment[0]][1], word_with_sentiment[1])
		)

	print(map_words_to_categories)
	return categories_with_sentiment


def get_similarity3(
	words: list[tuple[str, int]],
	model: object,
	categories: list[str] = None,
	subcategories: dict = None,
):
	"""Calculate similarity between words and categories using word2vec.

	param words:  list of tuples (word, sentiment)
	:return: list of tuples (category, sentiment) with calculated similarity
	"""
	### TODO: odrzucać słowa poniżej confidence 0.3

	words_to_categories = {}  # do debugowania
	categories_with_sentiment = []
	# merge dining data with ordinary categories
	categories = all_categories + dining
	subcategories = {**default_subcategories, **dining_subcategories}
	for word_with_sentiment in words:
		word_with_sentiment = word_with_sentiment[0]
		words_to_categories[word_with_sentiment] = [0, '']
		for category in categories:
			if category.find('_') != -1:
				sub = subcategories[category]
				for subcategory in sub:
					try:
						similarity = model.similarity(word_with_sentiment, subcategory)
						if similarity > words_to_categories[word_with_sentiment][0]:
							words_to_categories[word_with_sentiment][0] = similarity
							words_to_categories[word_with_sentiment][1] = category
					except KeyError:
						continue
			else:
				try:
					similarity = model.similarity(word_with_sentiment, category)
					if similarity > words_to_categories[word_with_sentiment][0]:
						words_to_categories[word_with_sentiment][0] = similarity
						words_to_categories[word_with_sentiment][1] = category
				except KeyError:
					continue

	for word_with_sentiment in words:
		if words_to_categories[word_with_sentiment[0]][1] == '':
			continue
		categories_with_sentiment.append(
			(words_to_categories[word_with_sentiment[0]][1], word_with_sentiment[1])
		)

	print('words_to_categories ', words_to_categories)
	# rozdziel dining od default
	ret_dining = []
	ret_default = []
	for category in categories_with_sentiment:
		if category[0] in dining:
			ret_dining.append(category)
		else:
			ret_default.append(category)
	print('ret_dining ', ret_dining)
	print('ret_default ', ret_default)

	return categories_with_sentiment


def get_subcategories(words: list[tuple[str, int]], model: object):
	"""Calculate similarity between words and subcategories using word2vec.

	param words:  list of tuples (word, sentiment)
	:return: list of tuples (subcategory, sentiment) with calculated similarity
	"""
	### TODO: odrzucać słowa poniżej confidence 0.3

	words_to_subcategories = {}
	subcategories_with_sentiment = []
	for word_with_sentiment in words:
		word_with_sentiment = word_with_sentiment[0]
		words_to_subcategories[word_with_sentiment] = [0, '']
		for category in all_categories:
			for subcategory in default_subcategories[category]:
				try:
					similarity = model.similarity(word_with_sentiment, subcategory)
					if similarity > words_to_subcategories[word_with_sentiment][0]:
						words_to_subcategories[word_with_sentiment][0] = similarity
						words_to_subcategories[word_with_sentiment][1] = subcategory
				except KeyError:
					continue
			try:
				similarity = model.similarity(word_with_sentiment, subcategory)
				if similarity > words_to_subcategories[word_with_sentiment][0]:
					words_to_subcategories[word_with_sentiment][0] = similarity
					words_to_subcategories[word_with_sentiment][1] = subcategory
			except KeyError:
				continue

	for word_with_sentiment in words:
		if words_to_subcategories[word_with_sentiment[0]][1] == '':
			continue
		subcategories_with_sentiment.append(
			(words_to_subcategories[word_with_sentiment[0]][1], word_with_sentiment[1])
		)

	print('words_to_subcategories ', words_to_subcategories)
	return subcategories_with_sentiment
