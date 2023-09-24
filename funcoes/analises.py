def appendItem(newRow, lista, campo):
    if newRow[campo] in lista:
            lista[newRow[campo]].append(newRow)
    else:
        lista[newRow[campo]] = [newRow]

def analisarPorDiaMarca(dia, conn, cur):
    query = "SELECT submission_date, product_brand, overall_rating FROM reviews WHERE submission_date LIKE '%" + dia + "%' AND product_brand != 'Não informado'"
    cur.execute(query)
    result = cur.fetchall()

    resultados_por_marca = {}
    for row in result:
        newRow = {
            'submission_date': row[0],
            'product_brand': row[1],
            'overall_rating': row[2]
        }
        
        appendItem(newRow=newRow, lista=resultados_por_marca, campo='product_brand')

    classificacao = []
    for resultado in resultados_por_marca:
        overallTotal = 0
        totalRows = 0
        for row in resultados_por_marca[resultado]:
            totalRows += 1
            overallTotal += row['overall_rating']
        
        media = overallTotal / totalRows
        res = {
            'dia_analisado': dia,
            'marca': resultado,
            'avaliação_média': round(media, 2)
        }
        classificacao.append(res)

    return classificacao

def analisarPorDiaProduto(dia, conn, cur):
    query = "SELECT submission_date, product_name, overall_rating FROM reviews WHERE submission_date LIKE '%" + dia + "%' AND product_name != 'Não informado'"
    cur.execute(query)
    result = cur.fetchall()

    resultados_por_produto = {}
    for row in result:
        newRow = {
            'submission_date': row[0],
            'product_name': row[1],
            'overall_rating': row[2]
        }
        
        appendItem(newRow=newRow, lista=resultados_por_produto, campo='product_name')
    
    classificacao = []
    for resultado in resultados_por_produto:
        overallTotal = 0
        totalRows = 0
        for row in resultados_por_produto[resultado]:
            totalRows += 1
            overallTotal += row['overall_rating']
        
        media = overallTotal / totalRows
        res = {
            'dia_analisado': dia,
            'produto': resultado,
            'avaliação_média': round(media, 2)
        }
        classificacao.append(res)

    return classificacao

def analisarPorDiaCategoria(dia, conn, cur):
    query = "SELECT submission_date, site_category_lv1, site_category_lv2, overall_rating FROM reviews WHERE submission_date LIKE '%" + dia + "%' AND (site_category_lv1 != 'Não informado' OR site_category_lv2 != 'Não informado')"
    cur.execute(query)
    result = cur.fetchall()

    resultados_por_categoria = {}
    for row in result:
        newRow = {
            'submission_date': row[0],
            'site_category_lv1': row[1],
            'site_category_lv2': row[2],
            'overall_rating': row[3]
        }
        
        if newRow['site_category_lv1'] != 'Não informado':
            appendItem(newRow=newRow, lista=resultados_por_categoria, campo='site_category_lv1')
        if newRow['site_category_lv2'] != 'Não informado':
            appendItem(newRow=newRow, lista=resultados_por_categoria, campo='site_category_lv2')
    
    classificacao = []
    for resultado in resultados_por_categoria:
        overallTotal = 0
        totalRows = 0
        for row in resultados_por_categoria[resultado]:
            totalRows += 1
            overallTotal += row['overall_rating']
        
        media = overallTotal / totalRows
        res = {
            'dia_analisado': dia,
            'categoria': resultado,
            'avaliação_média': round(media, 2)
        }
        classificacao.append(res)

    return classificacao

def analisarPorEstadoMarcaProduto(estado, tipo, cur):
    campo = ''
    if(tipo == 'marca'):
        campo = 'product_brand'
    else:
        campo = 'product_name'
    query = "SELECT reviewer_state, " + campo + ", overall_rating FROM reviews WHERE reviewer_state LIKE '" + estado + "' AND " + campo + " != 'Não informado'"
    cur.execute(query)
    result = cur.fetchall()

    resultados = {}
    for row in result:
        newRow = {
            'submission_date': row[0],
            campo: row[1],
            'overall_rating': row[2]
        }
        
        appendItem(newRow=newRow, lista=resultados, campo=campo)
    
    classificacao = []
    for resultado in resultados:
        overallTotal = 0
        totalRows = 0
        for row in resultados[resultado]:
            totalRows += 1
            overallTotal += row['overall_rating']
        
        media = overallTotal / totalRows
        res = {
            'estado': estado,
            tipo: resultado,
            'avaliação_média': round(media, 2)
        }
        classificacao.append(res)

    return classificacao

def analisarPorEstadoCategoria(estado, cur):
    query = "SELECT reviewer_state, site_category_lv1, site_category_lv2, overall_rating FROM reviews WHERE reviewer_state LIKE '" + estado + "' AND (site_category_lv1 != 'Não informado' OR site_category_lv2 != 'Não informado')"
    cur.execute(query)
    result = cur.fetchall()

    resultados = {}
    for row in result:
        newRow = {
            'submission_date': row[0],
            'site_category_lv1': row[1],
            'site_category_lv2': row[2],
            'overall_rating': row[3]
        }
        
        if newRow['site_category_lv1'] != 'Não informado':
            appendItem(newRow=newRow, lista=resultados, campo='site_category_lv1')
        if newRow['site_category_lv2'] != 'Não informado':
            appendItem(newRow=newRow, lista=resultados, campo='site_category_lv2')
    
    classificacao = []
    for resultado in resultados:
        overallTotal = 0
        totalRows = 0
        for row in resultados[resultado]:
            totalRows += 1
            overallTotal += row['overall_rating']
        
        media = overallTotal / totalRows
        res = {
            'estado': estado,
            'categoria': resultado,
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