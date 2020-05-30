import pickle
from gensim.models import Word2Vec
from pprint import pprint as pp
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
import sys
import string
# # from sklearn.manifold import TSNE
# # import matplotlib.pyplot as plt
# # import pandas as pd

f = open("nyt.txt", "r")

sentences = sent_tokenize(f.readline())
f.close()

sents = []
nltk_sents = []
tokenizer = RegexpTokenizer(r'\w+')
for s in sentences:
    words = s.split(" ")
    # sents.append([word.strip(string.punctuation).lower() for word in words])
    nltk_sents.append(tokenizer.tokenize(s))

word_arrays = [word_tokenize(s) for s in sentences]

model = Word2Vec(word_arrays[], min_count=1)
words = list(model.wv.vocab)
print(words)

# pp(dir(model.wv))