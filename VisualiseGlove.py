# Commented out IPython magic to ensure Python compatibility.
# Get the interactive Tools for Matplotlib
# %matplotlib inline
import matplotlib.pyplot as plt
#plt.style.use('ggplot')

from sklearn.decomposition import PCA

def display_pca_scatterplot(model, words=None, sample=0):
    if words == None:
        if sample > 0:
            words = np.random.choice(list(model.vocab.keys()), sample)
        else:
            words = [word for word in model.vocab]

    word_vectors = np.array([model[w] for w in words])
    twodim = PCA().fit_transform(word_vectors)[:, :2]

    plt.figure(figsize=(10, 10))
    plt.scatter(twodim[:, 0], twodim[:, 1], edgecolors='k', c='r')
    for word, (x, y) in zip(words, twodim):
        plt.text(x + 0.05, y + 0.05, word)

from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

glove_file = datapath('output/glove.txt')
word2vec_glove_file = get_tmpfile("file.word2vec.txt")
glove2word2vec(glove_file, word2vec_glove_file)

model = KeyedVectors.load_word2vec_format(word2vec_glove_file)

model.most_similar('leg-side')
result = model.most_similar(positive=['dot-ball'], negative=['six','four'])
print("{}: {:.4f}".format(*result[0]))
display_pca_scatterplot(model,words=['bravo','ashwin','pandya','tahir','kuldeep','bumrah','archer','rabada'])