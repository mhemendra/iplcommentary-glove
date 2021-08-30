
from spellchecker import SpellChecker
from collections import Counter
from tqdm import tqdm
import spacy
import numpy as np

stopwords = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]

modify_dict = {'Rashid Khan' : 'Rashid-Khan',
'du Plessis' : 'du-Plessis',
'de Kock' : 'de-Kock',
'Rohit Sharma' : 'Rohit',
'Axar Patel' : 'Axar',
'Avesh Khan' : 'Avesh-khan',
'Shivam Mavi' : 'Shivam-Mavi',
'Sam Curran' : 'Sam-Curran',
'Tom Curran' : 'Tom-Curran',
'JPR Scantlebury-Searles' : 'Searles',
'M Nabi' : 'Nabi',
'Barinder Sran' : 'Barinder-Sran',
'Monu Kumar' : 'Monu-Kumar',
'Shahbaz Ahmed' : 'Shabaz-Ahmed',
'Kartik Tyagi' : 'Karthik-Tyagi',
'S Dhawan' : 'Dhawan',
'Arshdeep Singh' : 'Arshdeep-Singh',
'Abdul Samad' : 'Samad',
'Harpreet Brar' : 'Harpreet-Brar',
'Ravi Bishnoi' : 'Ravi-Bishnoi',
'Chennai Super Kings': 'csk',
'Mumbai Indians':'mi',
'Kolkata Knight Riders':'kkr',
'Delhi Capitals':'dc',
'Kings XI Punjab':'kxip',
'Rajastan Royals':'rr',
'Sunrisers Hyderabad':'srh',
'Royal Challengers Banglore':'rcb',
'Rinku Singh': 'Rinku-Singh',
'1 run':'single',
'no run':'dot-ball',
'2 runs':'two-runs',
'3 runs':'three-runs',
'4 runs': 'four',
'FOUR runs': 'four',
'5 runs':'five-run',
'6 runs': 'six',
'SIX runs': 'six',
'no ball':'no-ball',
'1 wide':'1-wide',
'leg bye':'leg-bye',
'direct hit': 'direct-hit',
' off stump ':' off-stump ',
' leg stump ':' leg-stump ',
' off side ':' off-side ',
' leg side ':' leg-side ',
'run out':'run-out',
' silly mid on':' silly-mid-on',
' silly mid off':' silly-mid-off',
' silly point':' silly-point',
' leg slip':' leg-slip',
' deep midwicket':' deep-midwicket',
' deep backward point':' deep-backward-point',
' deep cover':' deep-cover',
' deep square leg':' deep-square-leg',
' deep point':' deep-point',
' deep fine leg':' deep-fine-leg',
' deep extra cover':' deep-extra-cover',
' short square leg':' short-square-leg',
' short fine leg':' short-fine-leg',
' short midwicket':' short-midwicket',
' short third man':' short-third-man',
' backward point':' backward-point',
' square leg':' square-leg',
' extra cover':' extra-cover',
' fine leg':' fine-leg',
' long off':' long-off',
' long on':' long-on',
' mid on':' mid-on',
' mid off':' mid-off',
' third man':' third-man',
' cover point':' cover-point',
' short leg':' short-leg',
' long leg':' long-leg',
' leg gully':' leg-gully',
' leg slip': ' leg-slip',
' hard length ':' hard-length ',
' short ball ':' short-ball ',
' in the slot ':' in-the-slot ',
' low full toss ':' low-full-toss ',
' full toss ':' full-toss ',
' good length ':' good-length ',
' run out ':' run-out ',
' down leg ':' down-leg ',
' slower ball ':' slower-ball ',
' slog swept ':' slog-swept ',
' outside off ':' outside-off ',
' knuckle ball ':' knuckle-ball ',
' knuckleball ':' knuckle-ball ',
' yorker length ':' yorker ',
}

def get_spell_errors(text_input):
  inputArray = []
  for row in text_input:
    rowArray = []
    for word in row.split(" "):
      rowArray.append(word)
    inputArray.append(rowArray)

  spell = SpellChecker()
  errors = list()
  for array in inputArray:
    out = spell.unknown(array)
    errors.extend(out)
  counts = Counter(errors)
  spell_errors = list()
  for key in counts:
    if(counts[key]<3):
      spell_errors.append(key)
  return spell_errors

def get_lemma(input):
  nlp = spacy.load('en_core_web_md', disable=['parser','ner','tagger'])
  lemma_dict = {}
  docs = nlp.pipe(input, n_threads = 4)
  for doc in tqdm(docs):
      word_seq = []
      for token in doc:
          if (token.text not in lemma_dict) and (token.pos_ is not "PUNCT"):
              lemma_dict[token.text] = token.lemma_
  del docs
  return lemma_dict

import pandas as pd

def joinData():
    ipl2020 = pd.read_csv(r'IPL2020 - Commentary Data.csv')
    ipl2019 = pd.read_csv(r'IPL2019 - Commentary Data.csv')
    ipl2018 = pd.read_csv(r'IPL2018 - Commentary Data.csv')

    txtInput = pd.concat([ipl2018, ipl2019, ipl2020])

    txtInput['short_text'] = txtInput['short_text'].str.replace(",", "")
    txtInput['long_text'] = txtInput['long_text'].fillna("")

    for special_char in ['kph','kmph', 'km/h', '\.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        txtInput['long_text'] = txtInput['long_text'].str.replace(special_char, "")

    #Adding traling whitespace to help with replace operation
    txtInput['commentary'] = " " + txtInput['short_text'] + " " + txtInput['long_text'] + " "
    txtInput = txtInput.drop(["over", "short_text", "long_text"], axis=1)

    for special_char in [';', '\'', ',', '?', '!', '"', ')', '(', '\'s ', '\'ll', '\[','\]']:
        txtInput['commentary'] = txtInput['commentary'].str.replace(special_char, "")

    for word in modify_dict.keys():
        txtInput['commentary'] = txtInput['commentary'].str.replace(word, modify_dict[word])

    txtInput['commentary'] = txtInput['commentary'].str.lower().replace("  ", " ")

    for word in stopwords:
      token = " " + word + " "
      txtInput['commentary'] = txtInput['commentary'].str.replace(token, " ")

    spell_errors = get_spell_errors(txtInput['commentary'])

    for word in spell_errors:
        token = " " + word + " "
        txtInput['commentary'] = txtInput['commentary'].str.replace(token, " ")

    txtInput['commentary'] = txtInput['commentary'].str.strip()

    for _ in range(10):
      txtInput['commentary'] = txtInput['commentary'].str.replace("  ", " ")

    input_array = []
    lemma_dict = get_lemma(txtInput['commentary'])
    for sentence in txtInput['commentary']:
        sentenceArray =[]
        for word in sentence.split(" "):
            try:
              sentenceArray.append(lemma_dict[word])
            except:
              sentenceArray.append(word)
        input_array.append(sentenceArray)
    #txtInput.to_csv(r'combined.csv', index=False)
    return input_array

def generate_glove(input, num_epochs=100):
    # importing the glove library
    from glove import Corpus, Glove
    # creating a corpus object
    corpus = Corpus()
    # training the corpus to generate the co occurence matrix which is used in GloVe
    corpus.fit(input, window=10)
    # creating a Glove object which will use the matrix created in the above lines to create embeddings
    # We can set the learning rate as it uses Gradient Descent and number of components
    glove = Glove(no_components=50, learning_rate=0.03)

    glove.fit(corpus.matrix, epochs=num_epochs, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)
    glove.save('glove.model')
    return glove

if __name__ == '__main__':
    inputArray = joinData()
    glove = generate_glove(inputArray, 100)

    glove_dict = glove.dictionary
    glove_vecs = glove.word_vectors
    word_vecs = []
    for item in glove_dict:
        # print(glove_vecs[glove_dict[item]])
        word_vec = []
        word_vec.append(item)
        word_vec.extend(glove_vecs[glove_dict[item]])
        word_vecs.append(word_vec)

    np_array = np.array(word_vecs)  # .reshape(-1, 51)
    np.savetxt('output/glove.txt', np_array, fmt='%s')