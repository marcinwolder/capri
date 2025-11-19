import time
from pprint import pprint

from gensim.models.doc2vec import Doc2Vec

from src.constants import (
	all_categories,
	default_categories,
	default_subcategories,
	dining,
	dining_subcategories,
)


def save(dir_name, model_name, loading_time, generation_time, word, result):
	output_file_path = dir_name + 'results_' + model_name + '.txt'
	with open(output_file_path, 'w', encoding='utf-8') as output_file:
		output_file.write(f'The model loading time: {loading_time:.2f} seconds\n')
		output_file.write(
			f'The result generation time: {generation_time:.2f} seconds\n'
		)
		if result:
			output_file.write(f"The most similar words to '{word}':\n")
			output_file.writelines(
				f'{similar_word} {similarity}\n' for similar_word, similarity in result
			)
		else:
			output_file.write(f"The word '{word}' is not present in the model.")

	print(f'The results have been saved to the file: {output_file_path}')


def load_models(model_name):
	"""Pomiar czasu ładowania modelu.
	Wczytanie modelu Word2Vec
	Measure time of generating results for example word
	"""
	root_path = '../../doc2vec/'
	path = root_path + model_name + '.model'
	start_loading_time = time.time()
	model = Doc2Vec.load(path)
	print(model)
	end_loading_time = time.time()
	loading_time = end_loading_time - start_loading_time

	word = 'example'
	result = None
	start_inference_time = time.time()
	result = model.wv.most_similar(word)
	end_inference_time = time.time()
	generation_time = end_inference_time - start_inference_time
	dir_name = 'detailed_info_doc2vec/example/'
	save(dir_name, model_name, loading_time, generation_time, word, result)

	categories = all_categories + default_categories
	dining_categories = dining

	print(categories)
	print(dining_categories)

	test_words_default = dict.fromkeys(default_subcategories, 1)
	test_words_dining = dict.fromkeys(dining_subcategories, 1)

	for main_category, dining_category in zip(categories, dining_categories):
		for words_default, word_dining in zip(
			default_subcategories[main_category], dining_subcategories[dining_category]
		):
			category = main_category.replace('_', ' ')
			dining_category = dining_category.replace('_', ' ')

			if words_default not in model.wv or word_dining not in model.wv:
				print(words_default, word_dining)
				continue

			if category not in model.wv or dining_category not in model.wv:
				print(category, dining_category)
				continue

			distance_default = model.wv.distance(words_default, category)
			distance_dining = model.wv.distance(word_dining, dining_category)

			test_words_default[words_default] = min(
				test_words_default[words_default], distance_default
			)

			test_words_dining[word_dining] = min(
				test_words_dining[word_dining], distance_dining
			)
	print(test_words_default)
	print(test_words_dining)

	base_dir_default = 'detailed_info_doc2vec/main_categories/' + model_name + '.txt'
	base_dir_dining = 'detailed_info_doc2vec/dining_categories/' + model_name + '.txt'
	with open(base_dir_default, 'a', encoding='utf-8') as output_file:
		output_file.write(str(test_words_default))
	with open(base_dir_dining, 'a', encoding='utf-8') as output_file:
		output_file.write(str(test_words_dining))

	model_dict = {
		model_name: {
			'loading_time': end_loading_time - start_loading_time,
			'inference_time': end_inference_time - start_inference_time,
		}
	}
	return model_dict


def main():
	model_dbow = 'doc2vec_dbow'
	model_dm = 'doc2vec_dm'
	model_dict = {}
	for model in [model_dbow, model_dm]:
		model_dict.update(load_models(model))
	with open('results.txt', 'a') as output_file:
		output_file.write(str(model_dict))


if __name__ == '__main__':
	main()


def debug():
	model_dbow = Doc2Vec.load('doc2vec_dbow.model')
	model_dm = Doc2Vec.load('doc2vec_dm.model')
	for model in [model_dbow, model_dm]:
		print(model)
		pprint(model.dv.most_similar(positive=['Machine learning'], topn=20))
