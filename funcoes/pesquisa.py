def pesquisarReviews(param: str, conn, cur):
    query = "SELECT * FROM reviews WHERE review_text LIKE '%" + param + "%' OR review_title LIKE '%" + param + "%'"
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
            'review_title':  row[7],
            'overall_rating':  row[8],
            'recommend_to_a_friend':  row[9],
            'review_text':  row[10],
            'reviewer_birth_year':  row[11],
            'reviewer_gender':  row[12],
            'reviewer_state': row[13]
        }
        resultado.append(newRow)
    return resultado

def getAll(conn, cur):
    query = "SELECT * FROM reviews LIMIT 10000"
    cur.execute(query)
    result = cur.fetchall()
    resultado = []
    for row in result:
        newRow = {
            'submission_date': row[0],
            'reviewer_id': row[1],
            #'product_id': row[2],
            #'product_name': row[3],
            #'product_brand': row[4],
            'site_category_lv1': row[5],
            #'site_category_lv2': row[6],
            #'review_title':  row[7],
            'overall_rating':  row[8],
            #'recommend_to_a_friend':  row[9],
            #'review_text':  row[10],
            'reviewer_birth_year':  row[11],
            'reviewer_gender':  row[12],
            'reviewer_state': row[13]
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
    query = 'SELECT r.reviewer_state, rp.classificacao_tema, rp.sentiment_text FROM reviews r JOIN reviews_processados rp ON r.reviewer_id = rp.reviewer_id LIMIT 10000;'
    cur.execute(query)
    result = cur.fetchall()   

    resultado = [] 

    for row in result:
        newRow = {
            'estado': row[0],
            'classificacao_tema': row[1],
            'sentimento_text': row[2]
        }
        resultado.append(newRow)
    
    return resultado