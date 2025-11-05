import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import src.backend
import src.constants
import src.data_model
import src.database
import src.api_calls
import src.ml_operations
import src.nlp_operations
import src.open_ai
import src.path
import src.rating
import src.recommendation
import src.route_optimalization
import src.travel_time
import src.twitter_tweepy


project = 'travel-app'
copyright = '2024, Czarnecka Bałabuszek'
author = 'Czarnecka Bałabuszek'
release = '1.0.0'
language='en'




extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'  
html_static_path = ['_static']