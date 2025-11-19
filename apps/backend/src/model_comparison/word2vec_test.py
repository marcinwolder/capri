import time

from gensim.models import KeyedVectors

from src.constants import (
	all_categories,
	default_subcategories,
	dining,
	dining_subcategories,
)

model_names = [
	'glove-twitter-25',
	'glove-twitter-50',
	'glove-twitter-100',
	'glove-twitter-200',
	'glove-wiki-gigaword-50',
	'glove-wiki-gigaword-100',
	'glove-wiki-gigaword-200',
	'glove-wiki-gigaword-300',
	'GoogleNews-vectors-negative300',
	'fasttext-wiki-news-subwords-300',
]


base_path = '../../new_models/'


def multi_label_classification(model, categories, subcategories):
	pass


def single_label_classification(model):
	"""Dla każdej katogorii sprawdza dokładność modelu.
	Zwraca średnią dokładność modelu, słownik dokładności dla każdej kategorii oraz zbiór brakujących słów.

	Dla każdej katogorii testuje słowa z podkategorii. Dla każdego słowa z listy słów, należacych do danej kategorii,
	sprawdza, do której kategorii jest najbardziej podobne. Zapisuje wynik do słownika accuracy_dict.
	Zlicza brakujące słowa.

	Jeżeli dane słowo zostało poprawnie zaklasyfikowane, to zwiększa licznik poprawnych klasyfikacji.
	Na koniec zwraca średnią dokładność modelu.
	"""
	missing_words = set()
	accuracy_dict = {}
	count_missing_words = 0
	categories = all_categories + dining
	subcategories = {**default_subcategories, **dining_subcategories}

	categories = [category for category in categories if category.find('_') == -1]
	for category in categories:
		test_words = subcategories[category]
		if category not in model.index_to_key:
			accuracy_dict[category] = -1
			for word in test_words:
				if word not in model.index_to_key:
					missing_words.add(word)
					count_missing_words += 1
			continue
		test_dict = {word: [0, None] for word in subcategories[category]}
		for test_word in test_words:
			if test_word not in model.index_to_key:
				missing_words.add(test_word)
				count_missing_words += 1
				continue
			for cat in categories:
				similarity = model.similarity(test_word, cat)
				if similarity > test_dict[test_word][0]:
					test_dict[test_word] = [similarity, cat]

		accuracy_dict[category] = sum(
			[1 for word in test_dict if test_dict[word][1] == category]
		) / len(test_dict)
	accuracy_counter, cumulative_acc = 0, 0
	for category in accuracy_dict:
		if accuracy_dict[category] != -1:
			accuracy_counter += 1
			cumulative_acc += accuracy_dict[category]
	avg_accuracy = cumulative_acc / accuracy_counter

	missing_word_ratio = count_missing_words / (len(categories) * len(subcategories))

	return avg_accuracy, accuracy_dict, missing_words, missing_word_ratio


def load_models(model_name):
	"""Pomiar czasu ładowania modelu.
	Wczytanie modelu Word2Vec
	"""
	start_loading_time = time.time()
	if model_name == 'GoogleNews-vectors-negative300':
		path = base_path + model_name + '.bin'
		model = KeyedVectors.load_word2vec_format(path, binary=True)
	else:
		if model_name == 'fasttext-wiki-news-subwords-300':
			path = base_path + model_name
		else:
			path = base_path + model_name + '.model'
		model = KeyedVectors.load_word2vec_format(path)
	end_loading_time = time.time()
	loading_time = end_loading_time - start_loading_time

	word = 'example'
	result = None
	start_inference_time = time.time()
	if word in model:
		result = model.most_similar(word)
	end_inference_time = time.time()
	generation_time = end_inference_time - start_inference_time

	avg_accuracy, accuracy_dict, missing_words, missing_word_ratio = (
		single_label_classification(model)
	)

	model_dict = {
		model_name: {
			'loading_time': loading_time,
			'inference_time': generation_time,
			'avg_accuracy': avg_accuracy,
			'accuracy': accuracy_dict,
			'missing_words': missing_words,
			'missing_word_ratio': missing_word_ratio,
		},
	}

	with open('word2vec/detailed_info/' + model_name + '.txt', 'w') as output_file:
		output_file.write(str(model_dict))

	return model_dict


def main():
	model_dict = {}
	for model_name in model_names:
		model_dict.update(load_models(model_name))
	with open('word2vec/results.txt', 'w') as output_file:
		output_file.write(str(model_dict))


if __name__ == '__main__':
	main()
