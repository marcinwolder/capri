"""t-SNE (t-distributed Stochastic Neighbor Embedding) is a technique for dimensionality reduction that is particularly
well suited for the visualization of high-dimensional datasets. It is a nonlinear dimensionality reduction technique
well-suited for embedding high-dimensional data for visualization in a low-dimensional space of two or three dimensions.

t-SNE minimizes the divergence between two distributions: a distribution that measures pairwise similarities of the
input objects and a distribution that measures pairwise similarities of the corresponding low-dimensional points in the
embedding. The t-SNE algorithm comprises two main stages. First, t-SNE constructs a probability distribution over pairs
of high-dimensional objects in such a way that similar objects have a high probability of being picked, whilst
dissimilar points have an extremely small probability of being picked. Second, t-SNE defines a similar probability
distribution over the points in the low-dimensional map, and it minimizes the Kullback–Leibler divergence between the
two distributions with respect to the locations of the points in the map. Note that whilst the original algorithm uses
the Euclidean distance between objects as the base of its similarity metric, this should be changed as appropriate.

The t-SNE algorithm has two main advantages over other techniques for visualizing high-dimensional data. First, t-SNE
optimizes the positions of the points in the map in such a way that similar objects are modeled by nearby points and
dissimilar objects are modeled by distant points with high probability. Second, t-SNE is capable of capturing much of
the local structure of the high-dimensional data very well, while also revealing global structure such as the presence
of clusters at several scales.


Point is to show distance between words and our categories in 2D space,
to show how similar they are.

"""

import matplotlib.pyplot as plt
import numpy as np
from gensim.models import KeyedVectors
from sklearn.manifold import TSNE

categories = [
	'amusement_park',
	'historical_landmark',
	'aquarium',
	'art_gallery',
	'bowling_alley',
	'campground',
	'church',
	'city_hall',
	'library',
	'lodging',
	'movie_theater',
	'museum',
	'night_club',
	'park',
	'restaurant',
	'spa',
	'stadium',
	'tourist_attraction',
	'university',
	'zoo',
]


words1 = ['restaurant', 'cafe', 'bar', 'coffee']
words2 = ['restaurant', 'cafe', 'bar', 'coffee', 'beer', 'wine', 'whiskey', 'vodka']
words3 = [
	'restaurant',
	'cafe',
	'bar',
	'coffee',
	'lunch',
	'dinner',
	'breakfast',
	'brunch',
]
words4 = [
	'restaurant',
	'cafe',
	'bar',
	'coffee',
	'beer',
	'wine',
	'whiskey',
	'vodka',
	'tea',
	'lunch',
	'dinner',
	'breakfast',
	'brunch',
]
words = [words1, words2, words3, words4]


def tsne_plot(model, words):
	"""Function to plot t-SNE for words in model.

	Check which words are available in the model and get their vectors.
	Set perplexity to a value smaller than the number of samples.
	Good starting point is e.g. sqrt(n_samples); adjust depending on your data.
	Use t-SNE to reduce the dimensionality to 2.
	Save word_vectors_2d to file.
	:param model: word2vec model
	:param words: list of words to plot
	:return:
	"""
	available_words = [word for word in words if word in model]
	word_vectors = np.array([model[word] for word in available_words])
	n_samples = len(word_vectors)
	print(f'Number of samples: {n_samples}')

	tsne = TSNE(n_components=2, perplexity=2, random_state=0)
	word_vectors_2d = tsne.fit_transform(word_vectors)

	np.save('../models_nlp/word_vectors_2d.npy', word_vectors_2d)


def plot(word_vectors_2d, available_words: list, idx: int):
	"""Function to plot word vectors in 2D.

	Read vectors from file and plot them in 2D space.
	Save plot to file.
	:param word_vectors_2d: word vectors in 2D space
	:param idx: index of the plot
	:param available_words: list of words
	"""
	plt.figure(figsize=(10, 8))
	for i, word in enumerate(available_words):
		plt.scatter(word_vectors_2d[i, 0], word_vectors_2d[i, 1])
		plt.annotate(
			word,
			xy=(word_vectors_2d[i, 0], word_vectors_2d[i, 1]),
			xytext=(5, 2),
			textcoords='offset points',
			ha='right',
			va='bottom',
		)
	plt.show()
	plt.savefig('./similarity_plots/plot_' + str(idx) + '.png')


def plot_2(word_vectors_2d, available_words: list, idx: int):
	plt.figure(figsize=(10, 8))
	plt.title('Wizualizacja wektorów słów', fontsize=18)
	for i, word in enumerate(available_words):
		plt.scatter(word_vectors_2d[i][0], word_vectors_2d[i][1], edgecolors='k', s=50)
		plt.text(
			word_vectors_2d[i][0] + 10, word_vectors_2d[i][1] + 5, word, fontsize=12
		)

	plt.xlabel('Wymiar 1', fontsize=14)
	plt.ylabel('Wymiar 2', fontsize=14)
	plt.grid(True)
	all_x_values = [coord[0] for coord in word_vectors_2d]
	all_y_values = [coord[1] for coord in word_vectors_2d]

	plt.xlim(min(all_x_values) - 50, max(all_x_values) + 50)
	plt.ylim(min(all_y_values) - 50, max(all_y_values) + 50)
	plt.show()


def main():
	model = KeyedVectors.load('../models/word2vec-google-news-300.model')
	for idx, w in enumerate(words):
		tsne_plot(model, w)
		word_vectors_2d = np.load('../models_nlp/word_vectors_2d.npy')
		plot_2(word_vectors_2d, w, idx)


if __name__ == '__main__':
	main()
