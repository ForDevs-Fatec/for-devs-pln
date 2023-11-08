from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
import pandas as pd
from dotenv import load_dotenv
import urllib.parse as up
import psycopg2
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


load_dotenv()

up.uses_netloc.append("postgres")
url = up.urlparse(os.getenv('DB_URL'))
conn = psycopg2.connect(
    database=url.path[1:],
    password = url.password,
    user=url.username,
    host=url.hostname,
    port=url.port
    )

cur = conn.cursor()

def getAllProcessados(conn, cur):
    query = "SELECT * FROM reviews_processados"
    cur.execute(query)
    result = cur.fetchall()
    resultado = []
    for row in result:
        newRow = {
            'reviewer_id': row[1],
            'sentiment_text': row[5]
        }
        resultado.append(newRow)
    return resultado

def csv():
    df = pd.read_csv('https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/main/B2W-Reviews01.csv')

    # Filtrar os comentários com 'review_text' não vazia ou NaN
    filtered_df = df.dropna(subset=['review_text'])
    filtered_df = filtered_df[filtered_df['review_text'].str.strip() != '']

    recent_comments = filtered_df

    df_pre = recent_comments[['reviewer_id','review_text', 'overall_rating' ]]

    df_pre = pd.DataFrame(df_pre)

    return df_pre

def dataframe():

    processado = getAllProcessados(conn=conn, cur=cur)

    comentarios = csv()

    df_processado = pd.DataFrame(processado)

    df_comentarios = pd.DataFrame(comentarios)

    df = pd.merge(df_comentarios, df_processado, on='reviewer_id')

    df = pd.DataFrame(df.head(10000))

    print (df)

    return df

def calcular_matriz_confusao(df):
    
    rating_mapping = {5: 'positive', 4: 'positive', 3: 'neutral', 2: 'negative', 1: 'negative'}
    df['overall_rating'] = df['overall_rating'].map(rating_mapping)

    print (df)
    
    # Calculando a matriz de confusão
    matriz_confusao = confusion_matrix(df['overall_rating'].values, df['sentiment_text'].values)

    print(matriz_confusao)

    # Calculando a acurácia
    accuracy = (matriz_confusao[0,0]+matriz_confusao[1,1]+matriz_confusao[2,2])/10000

    # Calculando a precisão para a classe positiva
    precision_positivo = (matriz_confusao[0,0])/(matriz_confusao[0,0]+matriz_confusao[1,0]+matriz_confusao[2,0])

    precision_negativo = (matriz_confusao[0,2])/(matriz_confusao[0,2]+matriz_confusao[1,2]+matriz_confusao[2,2])

    
    return matriz_confusao, accuracy, precision_positivo, precision_negativo

df = pd.DataFrame(dataframe())

matriz_confusao, accuracy, precision_positivo, precision_negativo = calcular_matriz_confusao(df)

print("\n \n")
print("Matriz de Confusão:")

print("        Positivo |   Neutro |  Negativo ")
print("Positivo   ", matriz_confusao[0,0],"|       ", matriz_confusao[0,1],"|    ", matriz_confusao[0,2]) 
print("Neutro      ", matriz_confusao[1,0],"|       ", matriz_confusao[1,1],"|    ", matriz_confusao[1,2])
print("Negativo   ", matriz_confusao[2,0],"|       ", matriz_confusao[2,1],"|    ", matriz_confusao[2,2])

print("\n \n")
print("Acurácia:", accuracy*100, " %" )

print("\n \n")
print("Precisão (Positivo):", precision_positivo*100, " %")
print("\n \n")

print("Precisão (Negativo):", precision_negativo*100, " %")
print("\n \n")


