from gensim.models import KeyedVectors

from src.model_comparison.single_keyword import categories_keywords_single

base_path = "../../new_models/"
twitter_25 = "glove-twitter-25.model"
twitter_50 = "glove-twitter-50.model"
twitter_100 = "glove-twitter-100.model"
twitter_200 = "glove-twitter-200.model"
gigaword_50 = "glove-wiki-gigaword-50.model"
gigaword_100 = "glove-wiki-gigaword-100.model"
gigaword_200 = "glove-wiki-gigaword-200.model"
gigaword_300 = "glove-wiki-gigaword-300.model"
path3 = "GoogleNews_vectors_negative/GoogleNews-vectors-negative300.bin"
gensim_model = KeyedVectors.load_word2vec_format(base_path + path3, binary=True)


categories_keywords_single['default_categories']['museum'] = ['art', 'history', 'artifacts']
categories_keywords_single['categories_nlp']['art_gallery'] = ['paintings', 'exhibitions', 'art', 'sculptures']
categories_keywords_single['dining']['performing_arts_theater'] = ['plays', 'musicals', 'performances', 'opera']







