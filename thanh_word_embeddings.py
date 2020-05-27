import pickle
from gensim.models import Word2Vec
from pprint import pprint as pp
from nltk.tokenize import sent_tokenize, word_tokenize
import sys
import string
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

TARGET_WORD_COUNT = 20000
TARGET_WORDS = ['Trump', 'Fauci', 'lockdown', 'mask', 'social-distancing', 'quarantine', 'shelter-in-place', 'stay-at-home', 'travel', 'China', 'vaccine', 'W.H.O.', 'C.D.C.', 'Pence', 'congress', 'Democrat', 'Republican']

if (len(sys.argv) != 2):
  print("Please supply a text file to build the word2vec model from.")
  exit(-1)

source_text_file = sys.argv[1]
f = open(source_text_file, "r")
raw_text = f.read()
sentences = sent_tokenize(raw_text, language='english')
f.close()

# Cut the number of sentences such that the word count is as close to the
# TARGET_WORD_COUNT as possible and at least as large
word_count = 0
for count, sentence in enumerate(sentences):
  if (word_count >= TARGET_WORD_COUNT): break
  word_count += len(word_tokenize(sentence))

word_arrays = [word_tokenize(s) for s in sentences[:count]]

model = Word2Vec(word_arrays, min_count=1)
words = list(model.wv.vocab)
# print("Model Vocabulary: " + str(words))
print("Total Word Count: " + str(word_count))
print("Unique Word Count: " + str(len(words)))

X = model[words]
pca = PCA(n_components=2)
result = pca.fit_transform(X)

target_word_indexes = []
for word in TARGET_WORDS:
  idx = words.index(word) if word in words else None
  if (idx):
    target_word_indexes.append(words.index(word))
    most_similar_words = model.most_similar(positive=word, topn=10)
    print(word)
    pp(most_similar_words)

sys.exit(0)

plt.scatter(result[target_word_indexes, 0], result[target_word_indexes, 1])

for idx in target_word_indexes:
  word = words[idx]
  plt.annotate(word, xy=(result[idx, 0], result[idx, 1]))

source_name = source_text_file.split(".")[0]
model_plot_file_name = source_name + "_plot.png"
print(model_plot_file_name)
plt.savefig(model_plot_file_name)