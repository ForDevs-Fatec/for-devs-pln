from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, fcluster
from gensim.models import word2vec
from pandas import DataFrame
import pandas as pd
from numpy import dot 
from numpy.linalg import norm
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re
import numpy as np
from numpy import average

#data = documento tokenizado 
def class_tema(df):
    tfidf_vectorized = TfidfVectorizer(min_df=0., max_df=1., norm='l2', use_idf=True)
    df
    max_dist = 150.

    documents = df['review_text_normalized']
    features = tfidf_vectorized.fit_transform(documents)
    feature_vectors = features.toarray()
    similarity_matrix = cosine_similarity(feature_vectors)
    Z = linkage(similarity_matrix, 'ward')
    cluster_labels = fcluster(Z, max_dist, criterion='distance')
    cluster_labels = DataFrame(cluster_labels, columns=['Cluster Label'])
    df['classificacao_tema'] = cluster_labels['Cluster Label']
    print(cluster_labels.head(5))
    return df

def class_tema_new(df):

    documents = df['review_text_normalized'].apply(word_tokenize)

    feature_size = 5  # size of vector representation
    window_context = 2
    min_word_count = 1
    sample = 1e-3
    w2vec_model = word2vec.Word2Vec(documents, vector_size= feature_size,
                                    window=window_context, min_count= min_word_count,
                                    sample=sample, epochs = 50)


    for doc in documents:
        print(doc)
        word_embedding = [] 
        for word in doc:
            word_embedding.append(w2vec_model.wv[word])
        word_embedding = np.array(word_embedding)
        print("\n \n")
        print("Document word embeddings: ")
        print(word_embedding)

        doc_embedding = np.zeros(feature_size)
        print(doc_embedding)
        if(len(doc) > 0):
            for i in range(len(doc_embedding)):     
                doc_embedding[i] = average(word_embedding[:,i])
        print("\n \n")
        print("Document feature vector based upon word embeddings: ")
        print(doc_embedding)
        print('=========================================================')
