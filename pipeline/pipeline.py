import pandas as pd
from funcoes import preproc
from pipeline import pipeline_Stopwords, pipeline_Tokenizacao, pipeline_analiseSentimento
from funcoes import class_tema

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

def gerarDocuments(lista):
    documents = []
    i = 0
    for item in lista:

        document = {
            "index_review": i,
            "submission_date": item[0],
            "reviewer_id": item[1],
            "product_id": item[2],
            "product_name": item[3],
            "product_brand": item[4],
            "site_category_lv1": item[5],
            "site_category_lv2": item[6],
            "overall_rating": item[8],
            "recommend_to_a_friend": item[9],
            "review_title": item[7],
            "review_text": item[10],
            "reviewer_birth_year": item[11],
            "reviewer_gender": item[12],
            "reviewer_state": item[13]
        }
        documents.append(document)
        i+= 1
    return documents


def executarPipeline(conn, cur, url, client):
    csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'
    df = pd.read_csv(csv_url, low_memory=True, sep=',')
    df = df.drop_duplicates()
    df = removerNulos(df)
    try:
        print('a')
        dados = gerarDocuments(df.values.tolist())
        print('b')
        client['dados'].delete_many({})
        client['dados'].insert_many(dados)
        print('c')

        dados_processados = preproc.executarPreProcessamento(dados)
        dados_processados = pipeline_Stopwords.executar_pipeline(dados_processados)
        dados_processados = pipeline_Tokenizacao.tokenizar(dados_processados)
        #classificacao
        class_tema.class_tema(dados_processados)
        dados_processados = pipeline_analiseSentimento.executar_analise_sentimento(dados_processados)
        print('passou aqui')
        client['dados_processados'].delete_many({})
        client['dados_processados'].insert_many(dados_processados)
        print(f"Total de registros na tabela 'reviews': {client['dados'].count()}")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")