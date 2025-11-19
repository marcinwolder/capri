from pprint import pprint

from gensim.models.doc2vec import Doc2Vec

model_dbow = Doc2Vec.load('doc2vec_dbow.model')
model_dm = Doc2Vec.load('doc2vec_dm.model')


for model in [model_dbow, model_dm]:
	print(model)
	pprint(model.dv.most_similar(positive=['Machine learning'], topn=20))

# for model in [model_dm, model_dbow]:
#     print(model)
#     pprint(model.dv.most_similar(positive=["Lady Gaga"], topn=10))
