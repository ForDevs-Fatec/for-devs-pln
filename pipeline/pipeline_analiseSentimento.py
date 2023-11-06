import re
import numpy as np
from numpy import dot
from numpy.linalg import norm
from gensim.models import word2vec
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity

def analisar(review_text, texto):

    setencas_politivas= ["adorei o produto",
                         "amei o produto", "O produto atendeu as expectativas. Até o momento não tive nenhum problema.",
                         "Excelente produto, entrega super rápida. Recomendo a todos", 
                         "com certeza comprarei novamente ", "Produto com bom custo benefício.. boa qualidade, estampas bem fiéis as da foto. Não tive problemas após lavagem,"
                         "produto muito bom", "Produto de boa qualidade, superou minhas expectativas", 
                         "consumidor amou o produto", "recomendo a todos", "O produto funciona perfeitamente, muito bom e muito prático de instalação e uso, eu o recomendo a todos, e muito barato e muito bom"
                         "entrega no prazo", "comprarei de novo", "produto maravilhoso", 
                         "Comprei exatamente o que queria, excelente produto, altíssima qualidade, super recomendo", 
                         "excelente qualidade", "produto otimo", "O aparelho chegou em perfeito estado e antes do previsto"]
    
    setencas_negativas= ["detestei o produto ", "produto horrível ", "nunca mais compro novamente ", "produto não foi entregue", "entrega atrasou", "não chegou","Até agora não recebi o meu pedido","produto com problemas, quebrou e não compensava arrumar", "Produto não condiz com as informações da embalagem",
                         "Não funciona, o nome é modelador de cachos, mas cachos que é bom não faz, veio na cor errada. E além de tudo isso não respondem as mensagens e não fazem o cancelamento ou a troca.", 
                         "pior produto que comprei ", "não é bom",   "não recomendo", "produto péssimo", "Não recebi o produto até a presente data, Lamentável isso! Vou denunciar no procon!", "O fone de ouvido não é original, qualidade péssima e som abafado.",
                         "não gostei ninguém resolve nada Já liguei várias vezes e ninguém resolve nada e eu quero meu dinheiro de volta", "Produto de péssima qualidade, não tem nada a ver com a foto", "O preço é enganoso" ]
    
    setencas_neutras= ["produto satisfatório", "produto atende as necessidades", "produto ok", "produto razoável", "não informado", "Atende as necessidades e expectativa do usuário, com preço acessível e de acordo com minhas disponibilidade.",
                       "Está de acordo com esperado.chegou dentro do praso pode comprar", "Por enquanto, sem queixas. Se surgir algum problema, com certeza voltarei para registrar.",
                       "Fiquei satisfeito com relação ao produto, prazo de entrega e preço."]

    positive_sentences = [word_tokenize(sentence) for sentence in setencas_politivas]
    negative_sentences = [word_tokenize(sentence) for sentence in setencas_negativas]
    neutral_sentences = [word_tokenize(sentence) for sentence in setencas_neutras]

    feature_size = 5  # size of vector representation
    window_context = 2
    min_word_count = 1
    sample = 1e-3

    w2vec_model_positivo = word2vec.Word2Vec(positive_sentences, vector_size= feature_size,
                                    window=window_context, min_count= min_word_count,
                                    sample=sample, epochs = 50)
    w2vec_model_negativo = word2vec.Word2Vec(negative_sentences, vector_size= feature_size,
                                    window=window_context, min_count= min_word_count,
                                    sample=sample, epochs = 50)
    w2vec_model_neutro = word2vec.Word2Vec(neutral_sentences, vector_size= feature_size,
                                    window=window_context, min_count= min_word_count,
                                    sample=sample, epochs = 50)
    
    sentence_vector = np.zeros(feature_size)
    positivo_similarity = []
    negativo_similarity = []
    neutro_similarity = []

    for word in texto.split():
        if word in w2vec_model_positivo.wv:
            positivo_similarity += cosine_similarity([sentence_vector], [w2vec_model_positivo.wv[word]])[0][0]
        if word in w2vec_model_negativo.wv:
            negativo_similarity += cosine_similarity([sentence_vector], [w2vec_model_negativo.wv[word]])[0][0]
        if word in w2vec_model_neutro.wv:
            neutro_similarity += cosine_similarity([sentence_vector], [w2vec_model_neutro.wv[word]])[0][0]

    if positivo_similarity > negativo_similarity and positivo_similarity > neutro_similarity:
        print(review_text)
        print('==================================================================')
        return "positiva"
    elif negativo_similarity > positivo_similarity and negativo_similarity > neutro_similarity:
        print(review_text)
        print('==================================================================')
        return "negativa"
    else:
        print(review_text)
        print('==================================================================')
        return "neutra"

def executar_analise_sentimento(df):

    df['sentiment_result'] = df.apply(lambda row: analisar(row['review_text'], row['review_text_normalized']), axis=1)
    return df