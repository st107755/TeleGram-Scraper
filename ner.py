from flair.data import Sentence
from flair.models import SequenceTagger
import pandas as pd
import ipdb

# load tagger
tagger = SequenceTagger.load("flair/ner-german-large")
# read data
df = pd.read_csv('chat.csv',delimiter=';')
# will empty with string
df = df.fillna('')
classified_sampes = 0
for index, row in df.iterrows():
    # classify sentence
    sentence = Sentence(row['text'])
    tagger.predict(sentence)
    # search for location in classification
    for entitys in sentence.get_spans('ner'):
        if entitys.tag == 'LOC':
            classified_sampes += 1
            print(entitys)
            break
    
print("Totals number of recongnised locations")
print(classified_sampes)
    
    # Test 2,3, 4,5
