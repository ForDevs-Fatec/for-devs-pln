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
    query = "SELECT reviewer_id, sentiment_text FROM reviews_processados"
    cur.execute(query)
    result = cur.fetchall()
    resultado = []
    for row in result:
        newRow = {
            'reviewer_id': row[0],
            'sentiment_text': row[1]
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
    
    rating_mapping = {5: 'positivo', 4: 'positivo', 3: 'neutro', 2: 'negativo', 1: 'negativo'}
    df['overall_rating'] = df['overall_rating'].map(rating_mapping)

    print (df)
    
    # Calculando a matriz de confusão
    confusion = confusion_matrix(df['sentiment_text'], df['overall_rating'])

    matriz_confusao = np.array(confusion)

    valores_diferentes_de_zero = matriz_confusao[matriz_confusao != 0]

    # Calculando a acurácia
    accuracy = (valores_diferentes_de_zero[0]+valores_diferentes_de_zero[4]+valores_diferentes_de_zero[8])/10000

    # Calculando a precisão para a classe positiva
    precision_positivo = (valores_diferentes_de_zero[0])/(valores_diferentes_de_zero[0]+valores_diferentes_de_zero[3]+valores_diferentes_de_zero[6])

    precision_negativo = (valores_diferentes_de_zero[8])/(valores_diferentes_de_zero[8]+valores_diferentes_de_zero[5]+valores_diferentes_de_zero[2])

    
    return valores_diferentes_de_zero, accuracy, precision_positivo, precision_negativo

df = pd.DataFrame(dataframe())

valores_diferentes_de_zero, accuracy, precision_positivo, precision_negativo = calcular_matriz_confusao(df)

print("\n \n")
print("Matriz de Confusão:")

print(valores_diferentes_de_zero[0], valores_diferentes_de_zero[1], valores_diferentes_de_zero[2])
print(valores_diferentes_de_zero[3], valores_diferentes_de_zero[4], valores_diferentes_de_zero[5])
print(valores_diferentes_de_zero[6], valores_diferentes_de_zero[7], valores_diferentes_de_zero[8])


print("\n \n")
print("Acurácia:", accuracy*100, " %" )

print("\n \n")
print("Precisão (Positivo):", precision_positivo*100, " %")
print("\n \n")

print("Precisão (Negativo):", precision_negativo*100, " %")
print("\n \n")


