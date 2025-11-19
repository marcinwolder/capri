import logging

import smart_open
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

logging.basicConfig(
	format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO
)

if __name__ == '__main__':
	# Preparing the corpus
	# wiki = WikiCorpus(
	#     "enwiki-latest-pages-articles.xml.bz2",  # path to the file you downloaded above
	#     tokenizer_func=tokenize,  # simple regexp; plug in your own tokenizer here
	#     metadata=True,  # also return the article titles and ids when parsing
	#     dictionary={},  # don't start processing the data yet
	# )
	#
	# with smart_open.open("wiki.txt.gz", "w", encoding='utf8') as fout:
	#     for article_no, (content, (page_id, title)) in enumerate(wiki.get_texts()):
	#         title = ' '.join(title.split())
	#         if article_no % 500000 == 0:
	#             logging.info("processing article #%i: %r (%i tokens)", article_no, title, len(content))
	#         fout.write(f"{title}\t{' '.join(content)}\n")  # title_of_article [TAB] words of the article
	#
	#
	# ########
	class TaggedWikiCorpus:
		def __init__(self, wiki_text_path):
			self.wiki_text_path = wiki_text_path

		def __iter__(self):
			for line in smart_open.open(self.wiki_text_path, encoding='utf8'):
				title, words = line.split('\t')
				yield TaggedDocument(words=words.split(), tags=[title])

	documents = TaggedWikiCorpus(
		'wiki.txt.gz'
	)  # A streamed iterable; nothing in RAM yet.
	first_doc = next(iter(documents))
	print(
		first_doc.tags,
		': ',
		' '.join(first_doc.words[:50] + ['………'] + first_doc.words[-50:]),
	)

	###########Training the model################
	workers = (
		20  # multiprocessing.cpu_count() - 1  # leave one core for the OS & other stuff
	)

	# PV-DBOW: paragraph vector in distributed bag of words mode
	model_dbow = Doc2Vec(
		dm=0,
		dbow_words=1,  # dbow_words=1 to train word vectors at the same time too, not only DBOW
		vector_size=200,
		window=8,
		epochs=10,
		workers=workers,
		max_final_vocab=1000000,
	)
	print('model_dbow: ')
	# PV-DM: paragraph vector in distributed memory mode
	model_dm = Doc2Vec(
		dm=1,
		dm_mean=1,  # use average of context word vectors to train DM
		vector_size=200,
		window=8,
		epochs=10,
		workers=workers,
		max_final_vocab=1000000,
	)
	print('model_dm: ')
	model_dbow.build_vocab(documents, progress_per=500000)
	print(model_dbow)

	# Save some time by copying the vocabulary structures from the DBOW model to the DM model.
	# Both models are built on top of exactly the same data, so there's no need to repeat the vocab-building step.
	model_dm.reset_from(model_dbow)
	print(model_dm)

	# Train DBOW doc2vec incl. word vectors.
	# Report progress every ½ hour.
	print('Training DBOW doc2vec incl. word vectors')
	model_dbow.train(
		documents,
		total_examples=model_dbow.corpus_count,
		epochs=model_dbow.epochs,
		report_delay=30 * 60,
	)
	# Train DM doc2vec.
	# Report progress every ½ hour.
	print('Training DM doc2vec')
	model_dm.train(
		documents,
		total_examples=model_dm.corpus_count,
		epochs=model_dm.epochs,
		report_delay=30 * 60,
	)

	model_dbow.save('doc2vec_dbow.model')
	model_dm.save('doc2vec_dm.model')
