import pandas as pd
from numpy import dot 
from numpy.linalg import norm
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re
import numpy as np
from numpy import average
from gensim.models import word2vec

def class_tema_new(palavra):

    sentencas_produto = ["chegou nem meses enviaram estorno vai 3 produto estava devolvi comprei fazer me já avaria não ",
        "na devendo ser poderia ficou melhor fraco opinião minha material ",
        "par estou dias durou jogando usando semana me vale todos controle xbox carga ",
        "produto ótimo sem reclamacoes "]
    
    sentencas_expectativa = ["superou recomendo imaginava expectativas minhas bom mas era ",
        "superou americanas agradeço prazo pelo produto expectativas ",
        "ótimo elogios está expectativas minhas preço boa correspondendo qualidade só ",
        "qualidade boa atendeu as expectativas"
    ]
    
    sentencas_prazo = [
        "chegou previsto prazo anúncio ao corresponde ",
        "corre indico dia prazo prático fora foi rápida super bem entrega ",
        "chegou prazo excelente ",
        "atendeu ao prazo entrega excelente"]
    

    documents_produto  = [ word_tokenize(sentence)  for sentence in sentencas_produto]
    documents_expectativa  = [ word_tokenize(sentence)  for sentence in sentencas_expectativa]
    documents_prazo  = [ word_tokenize(sentence)  for sentence in sentencas_prazo]

    feature_size = 5  # size of vector representation
    window_context = 2
    min_word_count = 1
    sample = 1e-3

    w2vec_model_produto = word2vec.Word2Vec(documents_produto, vector_size= feature_size,
                                    window=window_context, min_count= min_word_count,
                                    sample=sample, epochs = 50)
    w2vec_model_expectativa = word2vec.Word2Vec(documents_expectativa, vector_size= feature_size,
                                    window=window_context, min_count= min_word_count,
                                    sample=sample, epochs = 50)
    w2vec_model_prazo = word2vec.Word2Vec(documents_prazo, vector_size= feature_size,
                                    window=window_context, min_count= min_word_count,
                                    sample=sample, epochs = 50)

    word_embedding = [] 
    sentence_vector = 0
    for word in palavra.split():
        if word in w2vec_model_produto.wv:
            sentence_vector+=w2vec_model_produto.wv[word]
        if word in w2vec_model_expectativa.wv:
            sentence_vector+=w2vec_model_expectativa.wv[word]
        if word in w2vec_model_prazo.wv:
            sentence_vector+=w2vec_model_prazo.wv[word]
        print(word_embedding)

    produto_similarity = dot(sentence_vector, w2vec_model_produto.wv["produto"])
    expectativas_similarity = dot(sentence_vector, w2vec_model_expectativa.wv["expectativas"])
    prazo_similarity = dot(sentence_vector, w2vec_model_prazo.wv["prazo"])
    print("passou aqui")

    if len(word_embedding) > 0 and produto_similarity > expectativas_similarity and produto_similarity > prazo_similarity:
        print('==================================================================')
        print("produto")
        return 1
    elif len(word_embedding) > 0 and expectativas_similarity > produto_similarity and expectativas_similarity > prazo_similarity:
        print('==================================================================')
        print("expectativas")
        return 2
    else:
        print('==================================================================')
        print("entrega")
        return 3
