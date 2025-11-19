import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')


sentence = 'I like coffe, but I hate alcohol.'
displacy.serve(nlp(sentence), style='dep', port=5007)
