from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, fcluster
from pandas import DataFrame
import pandas as pd

#data = documento tokenizado 
def class_tema(df):
    tfidf_vectorized = TfidfVectorizer(min_df=0., max_df=1., norm='l2', use_idf=True)
    df_utilizado = df.head(10000)
    max_dist = 100.

    documents = df_utilizado['review_text_normalized']
    corpus_df = DataFrame({"Document": documents})

    tfidf_vectorized = TfidfVectorizer(min_df=0., max_df=1., norm='l2', use_idf=True)
    features = tfidf_vectorized.fit_transform(documents)
    feature_vectors = features.toarray()
    similarity_matrix = cosine_similarity(feature_vectors)
    Z = linkage(similarity_matrix, 'ward')
    cluster_labels = fcluster(Z, max_dist, criterion='distance')
    cluster_labels = DataFrame(cluster_labels, columns=['Cluster Label'])
    df['classificacao_tema'] = cluster_labels['Cluster Label']

    return df