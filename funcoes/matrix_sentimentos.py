from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
import pandas as pd
from dotenv import load_dotenv
import urllib.parse as up
import psycopg2
import os
import numpy as np


load_dotenv()

up.uses_netloc.append("postgres")
url = up.urlparse(os.getenv('DB_URL_RESERVA'))
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
            'overall_rating': row[3],
            'sentiment_text': row[6]
        }
        resultado.append(newRow)
    return resultado

def dataframe():

    processado = getAllProcessados(conn=conn, cur=cur)

    df_processado = pd.DataFrame(processado)

    print (df_processado)

    return df_processado

def calcular_matriz_confusao(df):
    
    rating_mapping = {5: 'positive', 4: 'positive', 3: 'neutral', 2: 'negative', 1: 'negative'}
    df['overall_rating'] = df['overall_rating'].map(rating_mapping)

    print (df)
    
    # Calculando a matriz de confusão
    matriz_confusao = confusion_matrix(df['overall_rating'].values, df['sentiment_text'].values)

    print(matriz_confusao)

    # Calculando a acurácia
    accuracy = (matriz_confusao[0,0]+matriz_confusao[1,1]+matriz_confusao[2,2])/((matriz_confusao[0,0])+(matriz_confusao[0,1])+(matriz_confusao[0,2])+(matriz_confusao[1,0])+(matriz_confusao[1,1])+(matriz_confusao[1,2])+(matriz_confusao[2,0])+(matriz_confusao[2,1])+(matriz_confusao[2,2]))

    # Calculando a precisão para a classe positiva
    precision_positivo = (matriz_confusao[0,0])/(matriz_confusao[0,0]+matriz_confusao[1,0]+matriz_confusao[2,0])

    precision_neutro = (matriz_confusao[1,1])/(matriz_confusao[0,1]+matriz_confusao[1,1]+matriz_confusao[1,2])

    precision_negativo = (matriz_confusao[2,2])/(matriz_confusao[0,2]+matriz_confusao[1,2]+matriz_confusao[2,2])

    
    return matriz_confusao, accuracy, precision_positivo, precision_negativo, precision_neutro

df = pd.DataFrame(dataframe())

matriz_confusao, accuracy, precision_positivo, precision_negativo, precision_neutro = calcular_matriz_confusao(df)

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

print("Precisão (Neutro):", precision_neutro*100, " %")
print("\n \n")

print("Precisão (Negativo):", precision_negativo*100, " %")
print("\n \n")


