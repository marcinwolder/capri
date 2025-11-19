from gensim.models import KeyedVectors

from src.nlp_operations.gensim_similarity import get_similarity3

base_path = '../../new_models/'


def test_similarity():
	"""Load Google's pre-trained Word2Vec model."""
	path = '../../new_models/GoogleNews-vectors-negative300.bin'
	gensim_model = KeyedVectors.load_word2vec_format(path, binary=True)
	words = [('art', 1), ('antique', 1), ('coffee', 1), ('museum', 1), ('theater', 1)]

	ret = get_similarity3(words, gensim_model)
	assert ret == [
		('art_gallery', 1),
		('museum', 1),
		('italian_restaurant', 1),
		('museum', 1),
		('movie_theater', 1),
	]
