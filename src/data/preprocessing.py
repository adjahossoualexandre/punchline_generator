import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize

# Helper functions
def read_corpus(path):
    with open(path, encoding='utf-8') as f:
        corpus=[]
        for line in f:
            corpus.append(line)
    return corpus
 
remove_xa0 = lambda corpus: [*map(lambda string: string[1:][:-2], corpus)]

def tokenize_quotation_marks(corpus):
    ''' replace quotation marks by  to distinguish them from apostrophees.
        eg: '‘Allô’' -> 'START_QUOTATION Allô END_QUOTATION'
    '''

    processed_corpus=[]
    len_corpus = len(corpus)
    for i in range(len_corpus):
        doc = corpus[i]
        if ('‘' in doc) and ('’' in doc):
            doc = doc.replace('‘', 'START_QUOTATION ')
            doc = doc.replace('’', ' END_QUOTATION')
            processed_corpus.append(doc)
        else:
            processed_corpus.append(doc)
        
    return processed_corpus

def manual_contraction_replacement(corpus):
    processed_corpus=[]
    len_corpus = len(corpus)
    for i in range(len_corpus):
        doc = corpus[i]
        if 'p’tit' in doc:
            doc = doc.replace('p’tit', 'petit')
        if 'p’tet' in doc:
            doc = doc.replace('p’tet', 'peut-être')
        if 'ch’vaux' in doc:
            doc = doc.replace('ch’vaux', 'chevaux')
        if 'stup’' in doc:
            doc = doc.replace('stup’', 'stupéfiant')
        if 'manif’' in doc:
            doc = doc.replace('manif’', 'manifestation')
        if 'Fuckin’' in doc:
            doc = doc.replace('Fuckin’', 'Fucking')
        if 'Fuckin' in doc:
            doc = doc.replace('Fuckin', 'Fucking')
        if 'd’amphét’' in doc:
            doc = doc.replace('d’amphét’', 'd’amphétamine')
        if 'compét’' in doc:
            doc = doc.replace('compét’', 'compétition')
        if 'tass’' in doc:
            doc = doc.replace('tass’', 'pétasse')
        if 'pauv’' in doc:
            doc = doc.replace('pauv’', 'pauvre')
        if 'mic’' in doc:
            doc = doc.replace('mic’', 'micro')
        if 'mic' in doc:
            doc = doc.replace('mic', 'micro')
        processed_corpus.append(doc)

    return processed_corpus

# CODE

corpus = read_corpus(r'C:\Users\alexa\punchline_generator\data\raw\raw_data.txt')

# remove \xa0 at the begining and the end of each document
corpus = remove_xa0(corpus)
corpus[0] = corpus[0][1:]

# Replace quotation marks with 'START_QUOTATION' and 'END_QUOTATION'
corpus = tokenize_quotation_marks(corpus)

# Manually replace  SOME contractions by the actual word
corpus = manual_contraction_replacement(corpus) 

''' Need to handle contraction. Example: "J'me" == "Je me".
        Need to be careful to exceptions such as "ch'vaux"
'''

# list of documents containing apostrophe
l=[doc for doc in corpus if '’' in doc]
# tokenizing
ll=[*map(lambda string: string.split(' '), l)]
# list of words with apostrophe
apo = [word for doc in ll for word in doc if '’' in word]

# collecting contractions
## contractions are when an apostrophe is followed by a consonant (except for H)
contractions=[]
vowels =list('aàeéèêiïîoœuûùyhAÀEÉÈÊIÎÏOUÙÛYH') # Notice that H isn't a vowel but still needs to be included in the list
for elmt in set(apo):
    apostrophe = elmt.find('’')
    if elmt[-1]=='’':
        contractions.append(elmt)
    elif elmt[apostrophe+1] not in vowels:
        contractions.append(elmt)

# Listing all the contractions and their actual word in a dictionary
contraction_dic = dict()
for elmt in contractions:
    apostrophe_position = elmt.find('’')
    contra = elmt[:apostrophe_position+1]
    actual_word = elmt[:apostrophe_position] + 'e'
    contraction_dic[contra] = actual_word



''' 

    tokenization : traiter les mot ac apostrophe ('j’', 't’' etc) comme des mots à part

    Entrainer mon propre word embedding pour tout le voc du corpus

    embedding_corpus=[]
    emedding_voc=[]
    vocabulary=[les mots du vocabulaire]
    stopwords=[les stopwords]
    l=[word for word in vocabulary if word not in stopword]
    for word in l:
        if word in embedding_voc:
            pass
        else:
            embedding_doc = scrap_on_internet(query(f'site:genius.com "{word}"')) # result is a string
            embedding_doc = embedding_doc.split(' ')
            embedding_corpus.append(embedding_doc)
            embedding_voc.extend([word for \
                                           word in embedding_doc if word not in stopword])

'''
