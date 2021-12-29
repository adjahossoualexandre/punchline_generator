import numpy as np
import pandas as pd

# Helper functions
def read_corpus(path):
    with open(path, encoding='utf-8') as f:
        corpus=[]
        for line in f:
            corpus.append(line)
    return corpus
 
remove_xa0 = lambda corpus: [*map(lambda string: string[1:][:-2], corpus)]


corpus = read_corpus(r'C:\Users\alexa\punchline_generator\data\raw\raw_data.txt')

# remove \xa0 at the begining and the end of each document
corpus = remove_xa0(corpus)
corpus[0] = corpus[0][1:]


''' Need to handle contraction. Example: "J'me" == "Je".
        Need to be careful to exceptions such as "ch'vaux"
'''

# list of documents containing apostrophe
l=[elmt for elmt in corpus if '’' in elmt]
# tokenizing
ll=[*map(lambda string: string.split(' '), l)]
# list of words with apostrophe
apo = [elmt for doc in ll for elmt in doc if '’' in elmt]

# collecting contractions
## contractions are when an apostrophe is followed by a consonant (except for H)
contractions=[]
vowels = list('aàeéèêioœuyhAEIOUYH')
for elmt in set(apo):
    apostrophe = elmt.find('’')
    if elmt[-1]=='’':
        contractions.append(elmt)
    elif elmt[apostrophe+1] not in vowels:
        contractions.append(elmt)

for i in contractions:
    print(i)