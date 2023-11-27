from sklearn.neural_network import MLPClassifier
from nltk.tokenize import word_tokenize
import pandas as pd
import re
import numpy as np
from numpy import dot
from numpy.linalg import norm
from numpy import average
from gensim.models import word2vec


def analisar(review_text, texto):
    
    normalized_sentences = texto
    feature_size = 5  # size of vector representation
    window_context = 2
    min_word_count = 1
    sample = 1e-3
    
    w2vec_model = word2vec.Word2Vec(normalized_sentences, vector_size= feature_size,
                                window=window_context, min_count= min_word_count,
                                sample=sample, epochs = 50)

    classified_reviews= [
        {'corpus': "['prazo', 'entrega', 'legal', 'recebi', 'certo', 'prazo']", 'review_type': 'entrega', 'feature_vector': [ 0.9859457,  -0.39454368,  0.43683675,  1.34583318, -1.59644437]},
        {'corpus': "['superou', 'expectativas', 'pratico', 'silencioso']", 'review_type': 'expectativa', 'feature_vector': [ 1.01352441, -0.45478693,  0.2653594,   1.37331629, -1.57133651]},
        {'corpus': "['amei', 'aparelho', 'recomendo', 'certeza', 'vcs', 'vão', 'adorar', 'lindo', 'demais']", 'review_type': 'recomendação', 'feature_vector': [ 0.98118585, -0.4250668,   0.49363875,  1.37780368, -1.62831032]},
        {'corpus': "['excelente', 'qualidade', 'confortável', 'prático', 'possui', 'tamanho', 'ideal', 'peso', 'leve', 'bonito', 'robusto', 'designer', 'moderno']", 'review_type': 'qualidade', 'feature_vector': [ 1.02177513, -0.32772842,  0.37046278,  1.41807616, -1.56547773]},
        {'corpus': "['produto', 'condiz', 'todas', 'características', 'citadas', 'descrição', 'excelente', 'aparelho']", 'review_type': 'produto', 'feature_vector': [ 0.97044176, -0.2705096,   0.50055963,  1.35449171, -1.55063212]},

        {'corpus': "['posso', 'avaliar', 'não', 'recebi', 'produto', 'entrega', 'atrasada']", 'review_type': 'entrega', 'feature_vector': [ 0.94398201, -0.52527958,  0.46511927,  1.32126689, -1.62774825]},
        {'corpus': "['produto', 'ruim', 'não', 'atendeu', 'expectativas', 'desmontar', 'utilizar', 'somente', 'eixo', 'pois', 'ficava', 'folgado', 'balançando']", 'review_type': 'expectativa', 'feature_vector': [ 1.00605607, -0.36434552,  0.40119869,  1.35844374, -1.58613181]},
        {'corpus': "['péssima', 'embalagem', 'veio', 'apenas', 'própria', 'caixa', 'produto', 'chegou', 'peça', 'quebrada', 'não', 'recomendo']", 'review_type': 'recomendação', 'feature_vector': [ 0.94554156, -0.46264803,  0.40292323,  1.30739188, -1.57310927]},
        {'corpus': "['produto', 'péssima', 'qualidade', 'veio', 'defeito']", 'review_type': 'qualidade', 'feature_vector': [ 0.98532993, -0.43148941,  0.3307595,   1.43512011, -1.55502713]},
        {'corpus': "['péssimo', 'produto', 'bem', 'diferente', 'foto', 'parece', 'plástico', 'elástico', 'borda', 'nada', 'parecido', 'foto', 'descrição']", 'review_type': 'produto', 'feature_vector': [ 0.95714509, -0.3531363,   0.48666632,  1.29767215, -1.57398582]},

        {'corpus': "['bem', 'atendido', 'entrega', 'prazo', 'combinado', 'recomendo', 'compra', 'internet']", 'review_type': 'entrega', 'feature_vector': [ 1.00182545, -0.27319217,  0.47128075,  1.34335029, -1.57229066]},
        {'corpus': "['atendeu', 'expectativas', 'ótimo', 'custo', 'benefício']", 'review_type': 'expectativa', 'feature_vector': [ 0.99502105, -0.42982051,  0.29593214,  1.44100273, -1.54663777]},
        {'corpus': "['recomendo', 'bom', 'produto', 'supriu', 'necessidades']", 'review_type': 'recomedação', 'feature_vector': [ 0.97929126, -0.44101262,  0.38888559,  1.37470424, -1.5854795 ]},
        {'corpus': "['gostei', 'acho', 'deveria', 'pouco', 'maiormais', 'produto', 'ótima', 'qualidade']", 'review_type': 'qualidade', 'feature_vector': [ 0.98538792, -0.45688102,  0.36807284,  1.45151973, -1.58140421]},
        {'corpus': "['produto', 'conforme', 'foto', 'descrição', 'site', 'não', 'reclamar', 'enquanto']", 'review_type': 'produto', 'feature_vector': [ 0.96225649, -0.3278639,   0.56723708,  1.25892878, -1.60990977]},
    ]


    documento = texto
    word_embedding = [] 
    for word in documento:
        if word in w2vec_model.wv:
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

    df['sentiment_text'] = df.apply(lambda row: analisar(row['review_text'], row['review_text_normalized']), axis=1)
    return df