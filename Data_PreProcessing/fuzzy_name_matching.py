import pandas as pd
import numpy as np
import re
import os
from pathlib import Path
from unidecode import unidecode
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

#Load the database containing science and technology staff names
personas = pd.read_csv('../CyT_Datasets/personas.csv', sep = ';', low_memory = False,
                      encoding='UTF-8')
#Remove rows with null values for sex
personas_limpia = personas[personas['sexo_id'].notna()]
#Combine first and last name
nombres_personas = personas_limpia['nombre'] + ' ' + personas_limpia['apellido']
#Normalize names
nombres_personas = nombres_personas.str.lower()
nombres_personas = nombres_personas.apply(lambda x: unidecode(x))
nombres_personas_clean = nombres_personas.apply(lambda x: re.sub(r'[^a-zA-Z]', r'', string = x))

#Load the dataset holding all posters information
all_posters_data = pd.read_csv('../SAN_csv/all_posters.csv')
#Remove author names duplicates
autores_sin_dup = all_posters_data['autor'].drop_duplicates()
#Normalize author names
name_spam = autores_sin_dup.str.lower()
name_spam = name_spam.str.strip()
name_spam = name_spam.apply(lambda x: re.sub(r'[\d°]', r'', string = str(x)))
name_spam = name_spam.apply(lambda x: unidecode(str(x)))
name_spam_clean = name_spam.apply(lambda x: re.sub(r'[^a-zA-Z]', r'', string = str(x)))

#Record Linkage

def ngrams(string, n = 3):
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

def getNearestN(query):
    queryTFIDF_ = vectorizer.transform(query)
    distances, indices = nbrs.kneighbors(queryTFIDF_)
    return distances, indices

#tf-idf implementation and KNN algorithm implementation over the tf-idf matrix
vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase= False)
tf_idf_matrix = vectorizer.fit_transform(nombres_personas_clean)
nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tf_idf_matrix)

#Generate a data frame holding the target name, the best match and the KNN distance score
name_spam = list(name_spam) #we need to convert back to a list
matches = []
for i,j in enumerate(inds):
    temp = [round(dis[i][0],2), nombres_personas.values[j][0], name_spam[i], autores_sin_dup.values[i], personas_limpia['persona_id'].values[j][0], j[0]]
    matches.append(temp)
final_res = pd.DataFrame(matches, columns = ['score', 'match','messy', 'original', 'id', 'index'])


#Levenshtein distance 

def multiple_scorer(col1, col2):
    partial_token_set = fuzz.partial_token_set_ratio(col1,col2)
    partial_ratio = fuzz.partial_ratio(col1, col2)
    token_sort = fuzz.token_sort_ratio(col1, col2)
    wratio = fuzz.WRatio(col1, col2)
    return [partial_token_set, partial_ratio, token_sort, wratio]

#Employ different applications of the Levenshtein distance to the best match from the KNN algorithm
resultado = []
for indice, row in final_res.iterrows():
    tmp_resultado = multiple_scorer(row['match'],row['messy'])
    promedio = np.round(np.mean(tmp_resultado[1:]), 3)
    tmp_resultado.append(promedio)
    resultado.append(tmp_resultado)
scores = pd.DataFrame(resultado, columns=['Partial Token Set', 'Partial Ratio', 'Token Sort', 'WRatio', 'Score Average'])

#Merge the previously created data frame with the new metrics
names_matched = pd.merge(final_res, scores, left_index=True, right_index=True)
#Save the results
names_matched.to_csv('../SAN_csv/matche_nombres.csv')