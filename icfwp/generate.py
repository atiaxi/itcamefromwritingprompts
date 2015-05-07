# For fun

from icfwp import app
from markov.model import TransitionTable

markov_filename = app.config['MARKOV_STORAGE']
tt = TransitionTable.from_filename(markov_filename)

for unused in xrange(10):
    print list(tt)
