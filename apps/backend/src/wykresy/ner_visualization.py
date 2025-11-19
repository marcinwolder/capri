"""Wizualizacja zależności między słowami w zdaniu. Korzysta z biblioteki SpaCy.
named entity recognition
"""

import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')

sentence = (
	'Elon Musk, the CEO of Tesla, announced a new electric vehicle model '
	'at a press conference in Los Angeles, California, on July 5th, 2023.'
)
displacy.serve(nlp(sentence), style='ent', port=5006)
