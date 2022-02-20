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

def replace_contraction_manually(corpus):
    ''' Remove '’' that cannot be detected by rule-based methods.'''
    processed_corpus=[]
    len_corpus = len(corpus)
    for i in range(len_corpus):
        doc = corpus[i]
        if 'Assassin’' in doc:
            doc = doc.replace('Assassin’', 'Assassin')
        if 'zouz’' in doc:
            doc = doc.replace('zouz’', 'zouz')
        if 'barbac’' in doc:
            doc = doc.replace('barbac’', 'barbecue')
        if 'Di Cap’' in doc:
            doc = doc.replace('Di Cap’', 'Di Caprio')
        if 'Sky’' in doc:
            doc = doc.replace('Sky’', 'Skyrock')
        if 'Diam’s' in doc:
            doc = doc.replace('Diam’s', 'Diams')
        if 'MC’s' in doc:
            doc = doc.replace('MC’s', 'emcees')
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


def find_all(character, string):
    str_as_list = list(string)
    sub_in_x = [*map(lambda x: character in x, string)]
    return np.where(sub_in_x)[0] # [0] avoid returning an ndarray of dimension (integer,)


def get_contracted_word(string, idx):

    ''' Extract contracted word from a string based on the position of the apostrophe.
        Ex: 'je veux qu’tu partes.'
            Return: 'qu’'
    '''
    string = string[:idx+1]
    len_str = len(string)
    word = string[idx]
    for i in range(1, len_str):
        # Exctract previous index
        prev_idx = len_str-1 - i
        # Extract precious letter
        prev_letter = string[prev_idx]
        if prev_letter not in [' ', ',', '’']:
            # Append word
            word = prev_letter + word
        else:
            break
    return word


def replace_contraction(string, contraction_dic):

        ''' Replace contractions by their actual words.
            eg: 'Moi tu m'parles pas d'age.' -> 'Moi tu me parles pas d'age.'
        '''
        
        left_trimmed=''
        apostrophe_idx = string.find('’')
        vowels =list('aàeéèêiïîoœuûùyhAÀEÉÈÊIÎÏOUÙÛYH') # Notice that H isn't a vowel but still needs to be included in the list
        while apostrophe_idx != -1:
            next_letter_idx = apostrophe_idx+1
            next_letter_is_consonent = string[next_letter_idx] not in vowels
            if next_letter_is_consonent:
                key = get_contracted_word(string, apostrophe_idx)
                value = contraction_dic[key]
                contraction_is_first_word = string[:len(key)] == key
                if contraction_is_first_word:
                    left_side = None
                    right_side = string[next_letter_idx:]
                    string = value + ' ' + right_side 
                else:
                    left_side = string[:apostrophe_idx - len(key)]   
                    right_side = string[next_letter_idx:]
                    string = left_side + ' ' + value + ' ' + right_side
                apostrophe_idx = string.find('’')

            else:
                left_trimmed += string[:apostrophe_idx+1]
                string = string[next_letter_idx:] # the right side
                apostrophe_idx = string.find('’')

        update = left_trimmed + string
        return update

for i,doc in enumerate(corpus):
    corpus[i] = replace_contraction(doc, contraction_dic)


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
