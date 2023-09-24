def appendItem(newRow, lista, campo):
    if newRow[campo] in lista:
            lista[newRow[campo]].append(newRow)
    else:
        lista[newRow[campo]] = [newRow]

def analisar(valor, tipo, analise, cur):
    campo = ''
    campoCategoria2 = ''
    campoAnalise = ''
    valorQuery = valor
    operadorIgualdade = 'LIKE'

    if tipo == 'marca':
        campo = 'product_brand'
    elif tipo == 'produto':
        campo = 'product_name'
    elif tipo == 'categoria':
        campo = 'site_category_lv1'
        campoCategoria2 = 'site_category_lv2'


    if analise == 'genero':
        campoAnalise = 'reviewer_gender'
    elif analise == 'estado':
        campoAnalise = 'reviewer_state'
    elif analise == 'dia':
        campoAnalise = 'submission_date'
        valorQuery = '%' + valor + '%'
    elif analise == 'idade':
        campoAnalise = 'reviewer_birth_year'
        operadorIgualdade = '='
    
    query = "SELECT " + campoAnalise + ", " + campo + ", overall_rating FROM reviews WHERE " + campoAnalise + " " + operadorIgualdade + " '" + valorQuery + "' AND " + campo + " != 'Não informado'"
    if tipo == 'categoria':
        query = "SELECT " + campoAnalise + ", " + campo + ", " + campoCategoria2 + ", overall_rating FROM reviews WHERE " + campoAnalise + " " + operadorIgualdade + " '" + valorQuery + "' AND (" + campo + " != 'Não informado' OR " + campoCategoria2 + " != 'Não informado')"

    cur.execute(query)
    result = cur.fetchall()

    resultados = {}

    if tipo != 'categoria':
        for row in result:
            newRow = {
                campoAnalise: row[0],
                campo: row[1],
                'overall_rating': row[2]
            }
            
            appendItem(newRow=newRow, lista=resultados, campo=campo)
    else:
        for row in result:
            newRow = {
                campoAnalise: row[0],
                campo: row[1],
                campoCategoria2: row[2],
                'overall_rating': row[3]
            }
            if newRow[campo] != 'Não informado':
                appendItem(newRow=newRow, lista=resultados, campo=campo)
            if newRow[campoCategoria2] != 'Não informado':
                appendItem(newRow=newRow, lista=resultados, campo=campoCategoria2)
    
    classificacao = []
    for resultado in resultados:
        overallTotal = 0
        totalRows = 0
        for row in resultados[resultado]:
            totalRows += 1
            overallTotal += row['overall_rating']
        
        media = overallTotal / totalRows
        res = {
            analise: valor,
            tipo: resultado,
            'avaliação_média': round(media, 2)
        }
        classificacao.append(res)

    return classificacao

def analisarPorDataGeral(conn, cur):
    query = "SELECT * FROM reviews WHERE product_name != 'Não informado'"
    cur.execute(query)
    result = cur.fetchall()

    resultados_por_produto = {}
    for row in result:
        newRow = {
            'submission_date': row[0],
            'product_name': row[3],
            'overall_rating': row[8]
        }

        if newRow['product_name'] in resultados_por_produto:
            resultados_por_produto[newRow['product_name']].append(newRow)
        else:
            resultados_por_produto[newRow['product_name']] = [newRow]
    
    classificacao = []
    for resultado in resultados_por_produto:
        overallTotal = 0
        totalRows = 0
        product_name = ''
        for row in resultados_por_produto[resultado]:
            totalRows += 1
            overallTotal += row['overall_rating']
            product_name = row['product_name']
        
        media = overallTotal / totalRows
        res = {
            'produto': product_name,
            'avaliação_média': media
        }
        classificacao.append(res)

    return classificacao