import psycopg2
from dotenv import load_dotenv
import os
import urllib.parse as up
import pandas as pd
from sqlalchemy import create_engine


def criarTabelaReviews(conn, cur):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS reviews (
    submission_date TIMESTAMP,
    reviewer_id VARCHAR(255),
    product_id INT,
    product_name VARCHAR(255),
    product_brand VARCHAR(255),
    site_category_lv1 VARCHAR(255),
    site_category_lv2 VARCHAR(255),
    overall_rating INT,
    recommend_to_a_friend VARCHAR(10),
    review_title TEXT,
    review_text TEXT,
    reviewer_birth_year INT,
    reviewer_gender VARCHAR(1),
    reviewer_state VARCHAR(255)
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    return True

def removerNulos(df):
    df['product_name'] = df['product_name'].fillna('Não informado')
    df['product_brand'] = df['product_brand'].fillna('Não informado')
    df['site_category_lv1'] = df['site_category_lv1'].fillna('Não informado')
    df['site_category_lv2'] = df['site_category_lv2'].fillna('Não informado')
    df['review_title'] = df['review_title'].fillna('Não informado')
    df['recommend_to_a_friend'] = df['recommend_to_a_friend'].fillna('N/A')
    df['review_text'] = df['review_text'].fillna('Não informado')
    df['reviewer_birth_year'] = df['reviewer_birth_year'].fillna(0)
    df['reviewer_gender'] = df['reviewer_gender'].fillna('0')
    df['reviewer_state'] = df['reviewer_state'].fillna('Não informado')

    print('Limpeza realizada')
    return df

def executarPipeline(conn, cur, url, client):
    csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'
    df = pd.read_csv(csv_url, sep=',')
    df = df.drop_duplicates()
    print(df.isnull().sum())
    df = removerNulos(df)
    print(df.isnull().sum())
    try:
        client['dados'].insert_many(df.values.tolist())
        print(f"Total de registros na tabela 'reviews': {client['dados'].count()}")
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")