from flair.data import Sentence
from flair.models import SequenceTagger
import pandas as pd
import ipdb

# load tagger
tagger = SequenceTagger.load("flair/ner-german-large")
df = pd.read_csv('chat.csv',delimiter=';')
df = df.dropna()
classified_sampes = 0

for index, row in df.iterrows():
    sentence = Sentence(row['text'])
    tagger.predict(sentence)
    loc_entitiys = []
    for entity in sentence.get_spans('ner'):
        #if entity.tag == 'LOC':
            #ipdb.set_trace()
            print(entity)
            loc_entitiys.append(entity)
    #if len(loc_entitiys) >= 2 :
        #ipdb.set_trace()


