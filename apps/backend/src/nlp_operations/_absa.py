"""This module contains the Aspect Based Sentiment Analysis (ABSA) model."""

from pyabsa import AspectTermExtraction as ATEPC

# you can view all available checkpoints by calling available_checkpoints()
# checkpoint_map = available_checkpoints()


def get_sentiment_data(sentences: list[str]):
	"""Function that returns a list of dictionaries with aspects and their sentiment."""
	aspect_extractor = ATEPC.AspectExtractor(
		# 'English',
		'multilingual',
		auto_device=True,  # False means load model on CPU
		cal_perplexity=True,
	)

	# instance inference
	atepc_result = aspect_extractor.predict(
		sentences,
		save_result=True,
		print_result=True,  # print the result
		ignore_error=True,
		# ignore the error when the
		# model cannot predict the input
	)
	return atepc_result
