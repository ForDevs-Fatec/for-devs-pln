from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, fcluster
from pandas import DataFrame
import pandas as pd

#data = documento tokenizado 
def class_tema(data):
    tfidf_vectorized = TfidfVectorizer(min_df=0., max_df=1., norm='l2', use_idf=True)
    max_dist = 100.

    for i in range(0, len(data), 10000):
        documents = [item['review_text_tokenizado'] for item in data[i: i + 10000]]

        features = tfidf_vectorized.fit_transform(documents)
        feature_vectors = features.toarray()

        # Similarity matrix computation
        similarity_matrix = cosine_similarity(feature_vectors)
        Z = linkage(similarity_matrix, 'ward')
        cluster_labels = fcluster(Z, max_dist, criterion='distance')
        cluster_labels = DataFrame(cluster_labels, columns=['Cluster Label'])

        j = 0
        for label in cluster_labels:
            data[i + j]['classificacao_tema'] = label
            j += 1
    
    return data