from sklearn.neural_network import MLPClassifier
from nltk.tokenize import word_tokenize
import pandas as pd
import re
import numpy as np
from numpy import dot
from numpy.linalg import norm
from numpy import average
from gensim.models import word2vec

csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'
df = pd.read_csv(csv_url)

palavras_unicas = set()


for linha in df['review_text']:
    if isinstance(linha, str): 
        palavras = linha.split()
        for palavra in palavras:
            palavra = palavra.strip('.,!?"\'').lower()
            if palavra:
                palavras_unicas.add(palavra)

palavras_unicas = list(palavras_unicas)

setencas = palavras_unicas

sentences = [word_tokenize(sentence) for sentence in setencas]

normalized_sentences = []
i = 0
for sentence in sentences:
    normalized_sentences.append([])
    for word in sentence:
        word = re.sub(r'[^A-Za-zÀ-Ýà-ý]','', word).lower()
        if word!='':
            normalized_sentences[i].append(word)
    i = i+1

stop_words = ['a', 'as', 'e', 'o', 'os', 'da', 'de', 'do', 'um', 'uma', '.', ',']
for word in stop_words:
    for sentence in normalized_sentences:
        if word in sentence:
            sentence.remove(word)

feature_size = 5  # size of vector representation
window_context = 2
min_word_count = 1
sample = 1e-3


w2vec_model = word2vec.Word2Vec(normalized_sentences, vector_size= feature_size,
                                window=window_context, min_count= min_word_count,
                                sample=sample, epochs = 50)


def analisar(review_text, texto, w2vec_model):
    classified_reviews= [
        {'corpus': "adorei o produto", 'review_type': 'positive', 'feature_vector': [1.10541701,  4.97184324,  5.38224506, -4.43752956, -0.96960557]},
        {'corpus': "amei o produto ", 'review_type': 'positive', 'feature_vector': [1.30435753,  5.02494621,  5.47072935, -5.06457138, -0.77965456]},
        {'corpus': "produto excelente", 'review_type': 'positive', 'feature_vector': [1.00461185,  5.93039513,  5.70828247, -5.02065182, -1.27102089]},
        {'corpus': "com certeza comprarei novamente ", 'review_type': 'positive', 'feature_vector': [0.37201083,  1.30930567,  1.41745484, -1.07905996, -0.19520766]},
        {'corpus': "detestei o produto ", 'review_type': 'negative', 'feature_vector': [0.7036382,   2.95675635,  3.15801859, -2.35740685, -0.85239857]},
        {'corpus': "produto horrível ", 'review_type': 'negative', 'feature_vector': [0.89847773,  3.66045666,  3.71151376, -3.10267878, -0.8972038]},
        {'corpus': "nunca mais compro novamente ", 'review_type': 'negative', 'feature_vector': [0.95918018,  2.1400764,   2.1044178,  -1.78310275, -0.91713619]},
        {'corpus': "pior produto que comprei ", 'review_type': 'negative', 'feature_vector': [1.09777379,  3.18250084,  3.7215023,  -3.0672574,  -1.21458387]},
        {'corpus': "produto satisfatório", 'review_type': 'neutral', 'feature_vector': [0.85209656,  2.94415069, 3.20332241, -2.32801414, -0.8120085]},
        {'corpus': "produto atende as necessidades", 'review_type': 'neutral', 'feature_vector': [0.59712869,  3.30555534,  3.41746235, -2.81626821, -0.9406082]},
        {'corpus': "produto ok", 'review_type': 'neutral', 'feature_vector': [0.37090012,  4.30867672,  4.47415543, -2.97053313, -0.4166882 ]},
        {'corpus': "produto razoável", 'review_type': 'neutral', 'feature_vector': [0.9018358,   3.01320148,  3.29691458, -2.40569186, -0.7701351]}
    ]


    documento = word_tokenize(texto)
    word_embedding = [] 
    for word in normalized_doc:
        word_embedding.append(w2vec_model.wv[word])
    word_embedding = np.array(word_embedding)

    doc_embedding = np.zeros(feature_size)
    for i in range(min(feature_size, len(word_embedding))):
        doc_embedding[i] = average(word_embedding[i])


    unclassified_review = {
        'corpus': documento,
        'review_type': '',
        'feature_vector': doc_embedding  
        }

    X = [] # feature vectorsS
    y = [] # feature classes
    for review in classified_reviews:
        X.append(review['feature_vector'])
        y.append(review['review_type'])

    classifier = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 3), random_state=1, max_iter=1000)



    classifier.fit(X, y)

    sentimento = classifier.predict([unclassified_review['feature_vector']])

    print(review_text)
    print(sentimento)
    print('==================================================================')
    return sentimento[0]

def executar_analise_sentimento(df):

    df['sentiment_result'] = df.apply(lambda row: analisar(row['review_text'], row['review_text_normalized'], w2vec_model), axis=1)
    return df