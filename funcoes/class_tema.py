from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, fcluster
from pandas import DataFrame


#data = documento tokenizado 
def class_tema(df):
    tfidf_vectorized = TfidfVectorizer(min_df=0., max_df=1., norm='l2', use_idf=True)
    max_dist = 90.

    documents = df['review_text_normalized']
    features = tfidf_vectorized.fit_transform(documents)
    feature_vectors = features.toarray()
    similarity_matrix = cosine_similarity(feature_vectors)
    Z = linkage(similarity_matrix, 'ward')
    cluster_labels = fcluster(Z, max_dist, criterion='distance')
    cluster_labels = DataFrame(cluster_labels, columns=['Cluster Label'])
    
    df = df.reset_index(drop=True)
    df['classificacao_tema'] = cluster_labels['Cluster Label']
    return df

