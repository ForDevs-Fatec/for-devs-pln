import psycopg2
from dotenv import load_dotenv
import os
import urllib.parse as up
import pandas as pd
from sqlalchemy import create_engine


def conectarBanco():
    
    return conn

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

env_path = 'for-devs-pln/.env'
load_dotenv()

up.uses_netloc.append("postgres")
url = up.urlparse(os.getenv('DB_URL'))

csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'
df = pd.read_csv(csv_url, sep=',')
df = df.drop_duplicates()
print(df.isnull().sum())
#df = removerNulos(df)
try:
    conn = psycopg2.connect(
        database=url.path[1:],
        password = url.password,
        user=url.username,
        host=url.hostname,
        port=url.port
    )

    engine = create_engine('postgresql://' + url.netloc)

    print("Conectou")

    cur = conn.cursor()

    criarTabelaReviews(conn=conn, cur=cur)
    df.to_sql('reviews', engine, if_exists='replace', index=False)

    cur.execute("SELECT COUNT(*) FROM reviews")
    count = cur.fetchone()[0]
    print(f"Total de registros na tabela 'reviews': {count}")

    conn.close()

except psycopg2.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

