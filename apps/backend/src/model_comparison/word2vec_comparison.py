import matplotlib.pyplot as plt
import numpy as np


def plots(model_dict, type):
	model_names = list(model_dict.keys())
	loading_times = [model_dict[model]['loading_time'] for model in model_names]
	inference_times = [model_dict[model]['inference_time'] for model in model_names]
	accuracies = [model_dict[model]['avg_accuracy'] for model in model_names]

	x = np.arange(len(model_names))

	fig, axs = plt.subplots(3, 1, figsize=(10, 15))

	axs[0].bar(model_names, loading_times, color='skyblue')
	axs[0].set_title(type)
	axs[0].set_subtitle('Czas ładowania modeli')
	axs[0].set_ylabel('Czas (s)')
	axs[0].set_xlabel('Nazwa modelu')

	axs[1].bar(model_names, inference_times, color='lightgreen')
	axs[1].set_title('Czas wnioskowania modeli')
	axs[1].set_ylabel('Czas (s)')
	axs[1].set_xlabel('Nazwa modelu')

	axs[2].bar(model_names, accuracies, color='salmon')
	axs[2].set_title('Dokładność modeli')
	axs[2].set_ylabel('Dokładność')
	axs[2].set_xlabel('Nazwa modelu')

	plt.tight_layout()
	plt.show()


def _plot(title, model_names, parameter, color, ylabel, filename):
	plt.figure(figsize=(10, 6))
	plt.bar(model_names, parameter, color=color)
	plt.title(title)
	plt.ylabel(ylabel)
	plt.xlabel('Nazwa modelu')

	plt.savefig('plots/' + filename + '.png')
	plt.show()


def plot(model_dict):
	model_names = list(model_dict.keys())

	names_dict = {
		'glove-twitter-25': 'tw-25',
		'glove-twitter-50': 'tw-50',
		'glove-twitter-100': 'tw-100',
		'glove-twitter-200': 'tw-200',
		'glove-wiki-gigaword-50': 'wiki-50',
		'glove-wiki-gigaword-100': 'wiki-100',
		'glove-wiki-gigaword-200': 'wiki-200',
		'glove-wiki-gigaword-300': 'wiki-300',
		'GoogleNews-vectors-negative300': 'gNews',
		'fasttext-wiki-news-subwords-300': 'fasttext',
	}

	loading_times = [model_dict[model]['loading_time'] for model in model_names]
	inference_times = [model_dict[model]['inference_time'] for model in model_names]
	accuracies = [model_dict[model]['avg_accuracy'] for model in model_names]
	missing_words = [model_dict[model]['missing_word_ratio'] for model in model_names]
	model_names = [names_dict[model] for model in model_names]
	_plot(
		'Czas ładowania modeli',
		model_names,
		loading_times,
		'skyblue',
		'Czas (s)',
		'loading_times',
	)
	_plot(
		'Czas wnioskowania modeli',
		model_names,
		inference_times,
		'lightgreen',
		'Czas (s)',
		'inference_times',
	)
	_plot(
		'Dokładność modeli',
		model_names,
		accuracies,
		'salmon',
		'Dokładność',
		'accuracies',
	)
	_plot(
		'Brakujące słowa',
		model_names,
		missing_words,
		'lightcoral',
		'Brakujące słowa',
		'missing_words',
	)


def main():
	model_dict = 'word2vec/results.txt'
	with open(model_dict) as file:
		models = eval(file.read())
		print(models)
	plot(models)


if __name__ == '__main__':
	main()
