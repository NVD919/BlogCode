from gensim.models import Word2Vec
from utils import MySentences

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
sentences = MySentences('chat_logs_processed.txt') # a memory-friendly iterator
model = Word2Vec(sentences,size = 200,window=2,min_count=50)
model.save('twitch_corpus.wv')
