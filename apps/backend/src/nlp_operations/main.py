import spacy

from src.nlp_operations._absa import get_sentiment_data
from src.nlp_operations.gensim_similarity import get_similarity3, get_subcategories
from src.nlp_operations.translation import detect_language, translate
from src.nlp_operations.utils import divide_text_to_sentences, process_sentiment_data


class AspectBasedSentimentAnalyzer:
	"""Class for Aspect Based Sentiment Analysis."""

	def __init__(self):
		self.nlp = spacy.load('en_core_web_sm')

	def get_preferences_from_text_data(self, text):
		"""1. wyciagniecie aspektow z tekstu
		2. obliczenie podobienstwa do kategorii
		3. zwrocenie listy kategorii
		"""
		lang = detect_language(text)  # detect language
		text = translate(text, lang[0]['label'])  # translate to english
		sentences = divide_text_to_sentences(text, self.nlp)
		sentiment_data = get_sentiment_data(sentences)
		list_of_aspects = process_sentiment_data(sentiment_data)
		return get_similarity3(list_of_aspects, self.gensim_model)

	def get_preferences_from_reviews(self, reviews: list[str]):
		"""1. wyciagniecie aspektow z recenzji
		2. obliczenie podobienstwa do podkategorii
		3. zwrocenie listy podkategorii
		:param reviews:
		:return:
		"""
		subcategories = {}  # set()
		for review in reviews:
			sentences = divide_text_to_sentences(review, self.nlp)
			sentiment_data = get_sentiment_data(sentences)
			list_of_aspects = process_sentiment_data(sentiment_data)
			subcategories.update(get_subcategories(list_of_aspects, self.gensim_model))

		return subcategories
