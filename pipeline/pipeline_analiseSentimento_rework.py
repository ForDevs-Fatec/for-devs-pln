from gensim.models import word2vec
from nltk.tokenize import word_tokenize
from sklearn.neural_network import MLPClassifier
import numpy as np
from numpy import average

def classificar_reviews_treinamento(reviews, classificacao, classified_reviews, model, feature_size):
    for review in reviews:
        documento = word_tokenize(review)
        word_embedding = []
        for word in documento:
            if word in model.wv:
                word_embedding.append(model.wv[word])
        
        word_embedding = np.array(word_embedding)
        doc_embedding = np.zeros(feature_size)
        for i in range(min(feature_size, len(word_embedding))):
            doc_embedding[i] = average(word_embedding[i])
        
        classified_review = {
            'corpus': review,
            'review_type': classificacao,
            'feature_vector': doc_embedding
        }

        classified_reviews.append(classified_review)
    
    return classified_reviews
        
def classificar_review_predicao(review, model, feature_size, classificador):
    print('passou aqui')
    word_embedding = []
    for word in review:
        if word in model.wv:
            word_embedding.append(model.wv[word])
    
    word_embedding = np.array(word_embedding)

    doc_embedding = np.zeros(feature_size)
    for i in range(min(feature_size, len(word_embedding))):
        doc_embedding[i] = average(word_embedding[i])
    
    unclassified_review = {
        'corpus': review,
        'review_type': '',
        'feature_vector': doc_embedding  
    }

    sentimento = classificador.predict([unclassified_review['feature_vector']])

    print(sentimento)

    return sentimento[0]

def executar_analise_sentimento(df):

    feature_size = 5  # size of vector representation
    window_context = 2
    min_word_count = 1
    sample = 1e-3

    w2vec_model = word2vec.Word2Vec(df['review_text_normalized'].apply(word_tokenize), vector_size= feature_size,
                                    window=window_context, min_count= min_word_count,
                                    sample=sample, epochs = 50)
    
    df_negativos = df[df['overall_rating'] < 3].head(1000)
    df_neutros = df[df['overall_rating'] == 3].head(1000)
    df_positivos = df[df['overall_rating'] > 3].head(1000)

    classified_reviews = []
    classified_reviews = classificar_reviews_treinamento(df_negativos['review_text_normalized'], 'negative', classified_reviews, w2vec_model, feature_size)
    classified_reviews = classificar_reviews_treinamento(df_neutros['review_text_normalized'], 'neutral', classified_reviews, w2vec_model, feature_size)
    classified_reviews = classificar_reviews_treinamento(df_positivos['review_text_normalized'], 'positive', classified_reviews, w2vec_model, feature_size)

    X = [] # feature vectors
    y = [] # feature classes
    for review in classified_reviews:
        X.append(review['feature_vector'])
        y.append(review['review_type'])

    classifier = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 3), random_state=1, max_iter=1000)

    classifier.fit(X, y)

    print(df.head(5))
    df['sentiment_text'] = df.apply(lambda row: classificar_review_predicao(word_tokenize(row['review_text_normalized']), w2vec_model, feature_size, classifier), axis=1)

    return df
