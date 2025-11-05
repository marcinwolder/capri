import gensim.downloader


print(list(gensim.downloader.info()['models'].keys()))
models = ['fasttext-wiki-news-subwords-300',
          'conceptnet-numberbatch-17-06-300',
          'word2vec-ruscorpora-300',
          'word2vec-google-news-300',
          'glove-wiki-gigaword-50',
          'glove-wiki-gigaword-100',
          'glove-wiki-gigaword-200',
          'glove-wiki-gigaword-300',
          'glove-twitter-25',
          'glove-twitter-50',
          'glove-twitter-100',
          'glove-twitter-200',
          '__testing_word2vec-matrix-synopsis']


def download_model():
    for model in models:
        print(gensim.downloader.load(model))
        print("Model {} downloaded".format(model))


download_model()
