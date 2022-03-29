import pandas as pd
import numpy as np
import re
import spacy
from functools import reduce
from operator import add
import string
import re
import multiprocessing as mp

### Below is all the code necessary to clean the data into useable form for modeling.

# Loading Data
from sklearn.feature_extraction.text import TfidfVectorizer

allrecipes_raw = pd.read_json('recipes_raw_nosource_ar.json')
epicurious_raw = pd.read_json('recipes_raw_nosource_epi.json')
foodnetwork_raw = pd.read_json('recipes_raw_nosource_fn.json')

allrecipes = allrecipes_raw.copy().T.reset_index().drop(columns = ['index'])
epicurious = epicurious_raw.copy().T.reset_index().drop(columns = ['index'])
foodnetwork = foodnetwork_raw.copy().T.reset_index().drop(columns = ['index'])
recipes = pd.concat([allrecipes, epicurious, foodnetwork]).reset_index(drop=True) # Concat does not reset indices

# Cleaning
null_recs = recipes.copy().drop(columns = 'picture_link').T.isna().any()
rows_to_drop = recipes[null_recs].index
recipes = recipes.drop(index = rows_to_drop).reset_index(drop = True)

nc_ingred_index = [index for i, index in zip(recipes['ingredients'], recipes.index) if all(j.isdigit() or j in string.punctuation for j in i)]
nc_title_index = [index for i, index in zip(recipes['title'], recipes.index) if all(j.isdigit() or j in string.punctuation for j in i)]
nc_instr_index = [index for i, index in zip(recipes['instructions'], recipes.index) if all(j.isdigit() or j in string.punctuation for j in i)]

index_list = [nc_ingred_index, nc_title_index, nc_instr_index]

inds_to_drop = set(reduce(add, index_list))
print(len(inds_to_drop))
recipes = recipes.drop(index=inds_to_drop).reset_index(drop=True)
print(recipes.shape)

empty_instr_ind = [index for i, index in zip(recipes['instructions'], recipes.index) if len(i) < 20]
recipes = recipes.drop(index = empty_instr_ind).reset_index(drop=True)

ingredients = []
for ing_list in recipes['ingredients']:
    clean_ings = [ing.replace('ADVERTISEMENT','').strip() for ing in ing_list]
    if '' in clean_ings:
        clean_ings.remove('')
    ingredients.append(clean_ings)
recipes['ingredients'] = ingredients

recipes['ingredient_text'] = ['; '.join(ingredients) for ingredients in recipes['ingredients']]
recipes['ingredient_text'].head()

recipes['ingredient_count'] = [len(ingredients) for ingredients in recipes['ingredients']]

all_text = recipes['title'] + ' ' + recipes['ingredient_text'] + ' ' + recipes['instructions']

def clean_text(documents):
    cleaned_text = []
    for doc in documents:
        doc = doc.translate(str.maketrans('', '', string.punctuation)) # Remove Punctuation
        doc = re.sub(r'\d+', '', doc) # Remove Digits
        doc = doc.replace('\n',' ') # Remove New Lines
        doc = doc.strip() # Remove Leading White Space
        doc = re.sub(' +', ' ', doc) # Remove multiple white spaces
        cleaned_text.append(doc)
    return cleaned_text

cleaned_text = clean_text(all_text)

# Testing Strategies and Code
nlp = spacy.load('en_core_web_sm')
' '.join([token.lemma_ for token in nlp(cleaned_text[2]) if not token.is_stop])

def text_tokenizer_mp(doc):
    tok_doc = ' '.join([token.lemma_ for token in nlp(doc) if not token.is_stop])
    return tok_doc

# Parallelzing tokenizing process
pool = mp.Pool(mp.cpu_count())
tokenized_text = pool.map(text_tokenizer_mp, [doc for doc in cleaned_text])
print(tokenized_text)

# Creating TF-IDF Matrices and recalling text dependencies

# import text_tokenized.csv

# TF-IDF vectorizer instance
# vectorizer = TfidfVectorizer(lowercase = True,
#                             ngram_range = (1,1))
#
# text_tfidf = vectorizer.fit_transform(tokenized_text)