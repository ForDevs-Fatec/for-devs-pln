from datetime import date # quando se quer apenas 1 dos submódulos
from pipeline.pipeline_Tokenizacao import tokenize_unique
from pipeline.pipeline_Stopwords import remover_stopwords
from pipeline.pipeline_analiseSentimento import analisar
from funcoes.correcao_ortografica import remover_duplicidade
from funcoes.preproc import remover_caracteres_especiais
from funcoes.class_tema import class_tema_new

def pesquisarReviews(param: str, conn, cur):

    try:
        # Faz pré-processamento 
        param_preproc = remover_caracteres_especiais(param)
        print(param_preproc)

        # Remove as StopWords do parâmetro de pesquisa - tarefa 1.10
        param_sem_stopwords = remover_stopwords(param_preproc)
        print(param_sem_stopwords)

        # Correção ortográficas dos parâmetros de pesquisa - tarefa 1.11
        param_corrigido = remover_duplicidade(param_sem_stopwords)
        print(param_corrigido)

        # Tokeniza o parâmetro de pesquisa - tarefa 1.9
        param_tokens = tokenize_unique(param_sem_stopwords)
        print(param_tokens)

        classificacao = class_tema_new(param_tokens)
        print(classificacao)

        # Aplica a análise de sentimentos aos parâmetros de pesquisa - tarefa 1.12
        sentimento_param = analisar(param_tokens)
        print(sentimento_param)

        query = f"SELECT * FROM reviews r JOIN reviews_processados rp ON r.submission_date = rp.submission_date AND r.reviewer_id = rp.reviewer_id WHERE r.review_text LIKE '%{param}%' AND rp.sentiment_result = '{sentimento_param}' AND rp.classificacao_tema = {classificacao}"

        cur.execute(query)
        result = cur.fetchall()
        resultado = []
        for row in result:
            newRow = {
                'submission_date': row[0],
                'reviewer_id': row[1],
                'product_id': row[2],
                'product_name': row[3],
                'product_brand': row[4],
                'site_category_lv1': row[5],
                'site_category_lv2': row[6],
                'review_title': row[7],
                'overall_rating': row[8],
                'recommend_to_a_friend': row[9],
                'review_text': row[10],
                'reviewer_birth_year': row[11],
                'reviewer_gender': row[12],
                'reviewer_state': row[13],
                'sentimento_param': sentimento_param,  
            }
            resultado.append(newRow)

        return resultado
    except Exception as e:
        print(e)

def getAll(conn, cur):
    query = "SELECT submission_date, reviewer_id, site_category_lv1, overall_rating, reviewer_birth_year, reviewer_gender, reviewer_gender, reviewer_state FROM reviews LIMIT 10000"
    cur.execute(query)
    result = cur.fetchall()
    resultado = []
    for row in result:
        newRow = {
            'submission_date': row[0],
            'reviewer_id': row[1],
            'site_category_lv1': row[2],
            'overall_rating':  row[3],
            'reviewer_birth_year':  row[4],
            'reviewer_gender':  row[5],
            'reviewer_state': row[6]
        }
        resultado.append(newRow)
    return resultado

def getAllProcessados(conn, cur):
    query = "SELECT * FROM reviews_processados LIMIT 10000"
    cur.execute(query)
    result = cur.fetchall()
    resultado = []
    for row in result:
        newRow = {
            'submission_date': row[0],
            'reviewer_id': row[1],
            'review_text_normalized': row[3],
            'classificacao_tema': row[4],
            'sentiment_text': row[5]
        }
        resultado.append(newRow)
    print(resultado)
    return resultado

def getMedia(conn, cur):
    query = """SELECT
    rp.classificacao_tema,
    COUNT(*) AS quantidade,
    ROUND(AVG(r.overall_rating), 2) AS media_rating
    FROM
        reviews_processados rp
    JOIN
        reviews r ON rp.submission_date = r.submission_date
    GROUP BY
        rp.classificacao_tema;"""
    
    cur.execute(query)
    result = cur.fetchall()
    resultado = []
    for row in result:
        newRow = {
            'classificacao_tema': row[0],
            'quantidade': row[1],
            'overall_rating': row[2]
        }
        resultado.append(newRow)
    return resultado

def getCategoriasPorTema(conn, cur):
    query = """
            WITH RankedReviews AS (
            SELECT
                rp.classificacao_tema,
                r.site_category_lv1,
                COUNT(*) AS frequencia
            FROM
                reviews_processados rp
            JOIN
                reviews r ON rp.submission_date = r.submission_date
            WHERE
                rp.classificacao_tema IN (2, 3, 4)
            GROUP BY
                rp.classificacao_tema, r.site_category_lv1
        )
        SELECT
            classificacao_tema,
            site_category_lv1,
            frequencia
        FROM (
            SELECT
                classificacao_tema,
                site_category_lv1,
                frequencia,
                ROW_NUMBER() OVER (PARTITION BY classificacao_tema ORDER BY frequencia DESC) AS ranking
            FROM
                RankedReviews
        ) RankedAndNumbered;
    """
    cur.execute(query)
    result = cur.fetchall()
    resultado = []
    for row in result:
        newRow = {
            'classificacao_tema': row[0],
            'categoria': row[1],
            'frequencia': row[2]
        }
        resultado.append(newRow)
        
    return resultado

def getClassificacaoTemaEContagem(conn, cur):
    query = "SELECT classificacao_tema, COUNT(*) FROM reviews_processados GROUP BY classificacao_tema LIMIT 10000"
    cur.execute(query)
    result = cur.fetchall()

    resultado = []

    for row in result:
        newRow = {
            'classificação_tema': row[0],
            'quantidade': row[1],
        }
        resultado.append(newRow)
    
    
    return resultado

def getClassificacaoTemaTempo(conn, cur):
    query = "SELECT DATE(submission_date) as data, classificacao_tema, COUNT(*) as contagem FROM reviews_processados GROUP BY data, classificacao_tema LIMIT 10000"
    cur.execute(query)
    result = cur.fetchall()   

    resultado = [] 

    for row in result:
        newRow = {
            'data': row[0],
            'classificacao_tema': row[1],
            'quantidade': row[2]
        }
        resultado.append(newRow)
    
    return resultado

def getClassificacaoTemaSentimento(conn, cur):
    query = "SELECT classificacao_tema, sentiment_text, COUNT(*) as contagem FROM reviews_processados GROUP BY classificacao_tema, sentiment_text LIMIT 10000"
    cur.execute(query)
    result = cur.fetchall()   

    resultado = [] 

    for row in result:
        newRow = {
            'classificacao_tema': row[0],
            'sentiment_text': row[1],
            'quantidade': row[2]
        }
        resultado.append(newRow)
    
    return resultado

def getClassificacaoTemaSentimentoEstado(conn, cur):
    query = 'SELECT r.reviewer_state, rp.classificacao_tema, rp.sentiment_text, COUNT (*) as contagem  FROM reviews r JOIN reviews_processados rp ON r.reviewer_id = rp.reviewer_id GROUP BY rp.classificacao_tema, rp.sentiment_text, r.reviewer_state LIMIT 10000;'
    cur.execute(query)
    result = cur.fetchall()   

    resultado = [] 

    for row in result:
        newRow = {
            'estado': row[0],
            'classificacao_tema': row[1],
            'sentimento_text': row[2],
            'quantidade': row[3],
        }
        resultado.append(newRow)

    return resultado

def getDistribuicaoSentimentosFaixaEtariaTema(conn, cur):
    query = 'SELECT r.reviewer_birth_year, rp.classificacao_tema, rp.sentiment_text, COUNT (*) as contagem FROM reviews r JOIN reviews_processados rp ON r.reviewer_id = rp.reviewer_id GROUP BY r.reviewer_birth_year, rp.classificacao_tema, rp.sentiment_text LIMIT 10000;'
    cur.execute(query)
    result = cur.fetchall()

    resultado = []
    
    for row in result:
        newRow = {
            'reviewer_birth_year': int(row[0]),
            'classificacao_tema': row[1],
            'sentimento_text': row[2],
            'quantidade': row[3],
        }
        resultado.append(newRow)

    return resultado

def getMedicoes(conn, cur):
    query = 'SELECT funcao, tempo FROM tempos;'
    cur.execute(query)
    result = cur.fetchall()

    resultado = []

    for row in result:
        newRow = {
            'função': row[0],
            'tempo': round(row[1], 2),
        }
        resultado.append(newRow)

    return resultado

def getMelhoresProdutos(conn, cur):
    query = '''SELECT r.product_name, COUNT(rp.sentiment_text) as positive_count
            FROM reviews r
            JOIN reviews_processados rp ON r.submission_date = rp.submission_date AND r.reviewer_id = rp.reviewer_id
            WHERE rp.sentiment_text = 'positive'
            GROUP BY r.product_name
            ORDER BY positive_count DESC
            LIMIT 5;'''
    cur.execute(query)
    result = cur.fetchall()

    resultado = []

    for row in result:
        newRow = {
            'product_name': row[0],
            'quantidade_reviews_positivas': row[1]
        }
        resultado.append(newRow)

    return resultado

def getPioresProdutos(conn, cur):
    query = '''SELECT r.product_name, COUNT(rp.sentiment_text) as negative_count
            FROM reviews r
            JOIN reviews_processados rp ON r.submission_date = rp.submission_date AND r.reviewer_id = rp.reviewer_id
            WHERE rp.sentiment_text = 'negative'
            GROUP BY r.product_name
            ORDER BY negative_count DESC
            LIMIT 5;'''
    cur.execute(query)
    result = cur.fetchall()

    resultado = []

    for row in result:
        newRow = {
            'product_name': row[0],
            'quantidade_reviews_negativas': row[1]
        }
        resultado.append(newRow)

    return resultado

def getMelhoresTemas(conn, cur):
    query = '''SELECT classificacao_tema, COUNT(sentiment_text) as positive_count
            FROM reviews_processados
            WHERE sentiment_text = 'positive'
            GROUP BY classificacao_tema
            ORDER BY positive_count DESC
            LIMIT 5;'''
    
    cur.execute(query)
    result = cur.fetchall()

    resultado = []

    for row in result:
        newRow = {
            'classificacao_tema': row[0],
            'quantidade_reviews_positivas': row[1]
        }
        resultado.append(newRow)
    
    return resultado

def getPioresTemas(conn, cur):
    query = '''SELECT classificacao_tema, COUNT(sentiment_text) as negative_count
            FROM reviews_processados
            WHERE sentiment_text = 'negative'
            GROUP BY classificacao_tema
            ORDER BY negative_count DESC
            LIMIT 5;'''
    
    cur.execute(query)
    result = cur.fetchall()

    resultado = []

    for row in result:
        newRow = {
            'classificacao_tema': row[0],
            'quantidade_reviews_negativas': row[1]
        }
        resultado.append(newRow)
    
    return resultado