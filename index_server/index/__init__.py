"""Ask485 package init."""
import os
import flask

from index.flask_app import app

import index.api

# Load inverted index, stopwords, and pagerank into memory
index.api.load_index()
