from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, fcluster
from pandas import DataFrame
import pandas as pd

#data = documento tokenizado 
def class_tema(data):
    
    documents = data
    corpus_df = DataFrame({"Document": documents})
    tfidf_vectorized = TfidfVectorizer(min_df=0., max_df=1., norm='l2', use_idf=True)
    features = tfidf_vectorized.fit_transform(documents)
    feature_vectors = features.toarray()
    similarity_matrix = cosine_similarity(feature_vectors)
    Z = linkage(similarity_matrix, 'ward')
    max_dist = 2.
    cluster_labels = fcluster(Z, max_dist, criterion='distance')
    cluster_labels = DataFrame(cluster_labels, columns=['Cluster Label'])
    df = pd.concat([corpus_df, cluster_labels], axis=1)

    return df