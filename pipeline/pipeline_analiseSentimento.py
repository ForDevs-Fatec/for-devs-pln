from sklearn.neural_network import MLPClassifier
from nltk.tokenize import word_tokenize
import pandas as pd
import re
import numpy as np
from numpy import dot
from numpy.linalg import norm
from numpy import average
from gensim.models import word2vec
from funcoes.correcao_ortografica import remover_duplicidade
from funcoes.preproc import remover_caracteres_especiais
from pipeline.pipeline_Tokenizacao import tokenize_unique
from pipeline.pipeline_Stopwords import remover_stopwords

csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'
df = pd.read_csv(csv_url)

palavras_unicas = set()


for linha in df['review_text']:
    if isinstance(linha, str):
        palavras = linha.split()
        for palavra in palavras:
            palavra = palavra.strip(',.!?"\'').lower()


            if palavra:
              if ',' in palavra:
                words = palavra.split(',')
                for word in words:
                  palavras_unicas.add(word)
              else:
                palavras_unicas.add(palavra)

palavras_unicas = list(palavras_unicas)

setencas = palavras_unicas
sentences = [word_tokenize(sentence) for sentence in setencas]

normalized = []
i = 0
for sentence in sentences:
    normalized.append([])
    for word in sentence:
        word = re.sub(r'[^A-Za-zÀ-Ýà-ý]','', word).lower()
        if word!='':
            normalized[i].append(word)
    i = i+1

normalized_sentences = []

for sublista in normalized:
    for item in sublista:
        normalized_sentences.append([item])

stop_words = ['a', 'as', 'e', 'o', 'os', 'da', 'de', 'do', 'um', 'uma', '.', ',', '!']
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
        {'corpus': "Ótimo produto e entrega Super rapida, chegou em menos de dois dias.", 'review_type': 'positive', 'feature_vector': [1.10541701,  4.97184324,  5.38224506, -4.43752956, -0.96960557]},
        {'corpus': "Chegou bem antes do prazo!! Tudo otimo recomendo demais!!", 'review_type': 'positive', 'feature_vector': [-0.00394224, -0.00186425,  0.03984901, -0.01576146,  0.01215821]},
        {'corpus': "Ótimo produto Excelente qualidade. Já usei e recomendo este produto.", 'review_type': 'positive', 'feature_vector': [-0.08136832,  0.04390262,  0.08365295, -0.00907106, -0.05642267]},
        {'corpus': "Produto de boa qualidade e recebi em perfeito estado, entrega super rápida.", 'review_type': 'positive', 'feature_vector': [-0.05841277,  0.02493754,  0.01713472, -0.01604848, -0.01423774]},
        {'corpus': "Chegou no prazo correto. Aparelho ótimo, tudo conforme descrito no anúncio.", 'review_type': 'positive', 'feature_vector': [0.02736017, -0.00628977,  0.00672057,  0.05595206,  0.00499788]},
        {'corpus': "Gostei muito, atendeu perfeitamente. Chegou direitinho!!", 'review_type': 'positive', 'feature_vector': [-0.03946819,  0.01854357,  0.01189471, -0.07593762,  0.0322136 ]},
        {'corpus': "Mesa ótima!! É linda! Eu mesma montei! Chegou antes do prazo! Super recomendo!", 'review_type': 'positive', 'feature_vector': [-0.00807642,  0.02122578,  0.02509633,  0.02652107, -0.00663178]},
        {'corpus': "Indico o produto e o vendedor também. Ótimos preços e entrega rápida.", 'review_type': 'positive', 'feature_vector': [-0.02366128,  0.0747508,   0.0075716,  -0.05016868, -0.00525335]},
        {'corpus': "Produto prático e útil. Fácil manuseio. Já disse tudo de relevante em relação ao produto.", 'review_type': 'positive', 'feature_vector': [-0.05997973, -0.01290564,  0.02751197, -0.04504505,  0.01168993]},
        {'corpus': "Produto veio no dia certo. Amei. Pode comprar é confiável", 'review_type': 'positive', 'feature_vector': [0.02719796, -0.00626532,  0.06487962, -0.03043219, -0.02083143]},
        {'corpus': "Tudo certo com o produto. Chegou no prazo, tudo conforme prometido.", 'review_type': 'positive', 'feature_vector': [0.01169822, 0.03002487, 0.02195769, 0.03441947, 0.01136815]},
        {'corpus': "Muito bom e recomendo pois atendeu as minhas expectativas de acordo com o prometido", 'review_type': 'positive', 'feature_vector': [0.01976705,  0.02236095,  0.01977084,  0.00888005, -0.03331756]},
        {'corpus': "Gostei do produto, bom acabamento, estampa bonita e bem feita.", 'review_type': 'positive', 'feature_vector': [0.00787183, -0.04485768,  0.01957471, -0.02008803,  0.01866031]},


        {'corpus': "O produto simplesmente não funciona e não estou conseguindo devolver o produto.", 'review_type': 'negative', 'feature_vector': [-0.00926059,  0.09580828,  0.04905467, -0.09229385, -0.08771273]},
        {'corpus': "Não gostei do produto. Qualidade duvidosa. Não recomendo.", 'review_type': 'negative', 'feature_vector': [-0.03302601,  0.03787755,  0.04970625,  0.01533167, -0.10186921]},
        {'corpus': "Ainda não recebi o produto e nem uma posição ou retorno de quando receberei.", 'review_type': 'negative', 'feature_vector': [0.00655954, -0.01938496, -0.01662059, -0.06758626, -0.07846995]},
        {'corpus': "Comprei e me arrependi. Produto de baixa qualidade, veio com uma peça trincada. Não recomendo.", 'review_type': 'negative', 'feature_vector': [-0.01272981,  0.02871567,  0.05262753, -0.0304186,  -0.06302559]},
        {'corpus': "Até hoje não recebi o produto e nem o dinheiro, não recomendo essa americanas para ninguém", 'review_type': 'negative', 'feature_vector': [-0.00190271,  0.0094188,   0.03217983, -0.06665723, -0.07436707]},
        {'corpus': "produto não é bom", 'review_type': 'negative', 'feature_vector': [0.02802305,  0.10602981,  0.12126648, -0.08163466, -0.03711553]},

        {'corpus': "muito simples pelo preço, isso que da compra espontaneamente", 'review_type': 'negative', 'feature_vector': [0.03430578,  0.032687,    0.0403705,  -0.01818323, -0.0323541]},
        {'corpus': "Bom . Conforme combinado. chegou antes do prazo. Tudo certo.", 'review_type': 'positive', 'feature_vector': [0.00902728, -0.00630609, -0.00864388, -0.02090178, -0.01329581]},
        {'corpus': "estou satisfeito com o produto bom e barato o meu não o entrou aguá", 'review_type': 'positive', 'feature_vector': [-0.00066112, -0.00274017,  0.03489415, -0.01236685,  0.01852863]},
        {'corpus': "A qualidade do produto é equivalente ao preço, ou seja, é bom para o valor cobrado.", 'review_type': 'positive', 'feature_vector': [-0.00242339,  0.09500432,  0.0429258,   0.02415989,  0.01505293]},
        {'corpus': "Nao gostei do material do produto. O tamanho é ótimo chegou muito rápido do não gostei do material", 'review_type': 'negative', 'feature_vector': [-0.02762635, -0.05266787,  0.03693885, -0.01872506,  0.03050968]}

    ]

    documento = word_tokenize(texto)
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

    df['sentiment_text'] = df.apply(lambda row: analisar(row['review_text'], row['review_text_normalized'], w2vec_model), axis=1)
    return df