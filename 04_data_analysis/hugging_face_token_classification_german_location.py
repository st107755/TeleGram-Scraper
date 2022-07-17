##not finished
#%% install flair -> ERROR: Underscore Problem
#from matplotlib.pyplot import text
from flair.data import Sentence
from flair.models import SequenceTagger

import transformers ## brauche die version 2.4.1, um Flair installieren zu lassen?

#%% load tagger
tagger = SequenceTagger.load("flair/ner-german-large")

# make example sentence
sentence = Sentence("George Washington ging nach Washington")

# predict NER tags
tagger.predict(sentence)

# print sentence
print(sentence)

# print predicted NER spans
print('The following NER tags are found:')
# iterate over entities and print
for entity in sentence.get_spans('ner'):
    print(entity)


# %% import data
import pandas as pd
data = pd.read_csv('chat.csv',delimiter=';')

#%% choose only relevant data
textseries = data['text']

# %%function over all sentences
def classif (textseries):
    for index,value in textseries.items():
        sentences = tagger.predict(text) 
    return sentences
        

sentence_predict = classif(sentences)