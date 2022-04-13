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
    
    for entitys in sentence.get_spans('ner'):
        if entitys.tag == 'LOC':
            classified_sampes += 1
            print(entitys)
            break
    
print("Totals number of recongnised locations")
print(classified_sampes)
    
