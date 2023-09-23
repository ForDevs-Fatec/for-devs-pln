def analisarPorDia(dia, tipo, conn, cur):
    query = "SELECT * FROM reviews WHERE submission_date LIKE '%" + dia + "%' AND product_brand != 'Não informado'"
    cur.execute(query)
    result = cur.fetchall()

    resultados_por_marca = {}
    for row in result:
        newRow = {
            'submission_date': row[0],
            'product_brand': row[4],
            'overall_rating': row[8]
        }
        
        if newRow['product_brand'] in resultados_por_marca:
            resultados_por_marca[newRow['product_brand']].append(newRow)
        else:
            resultados_por_marca[newRow['product_brand']] = [newRow]

    classificacao = []
    for resultado in resultados_por_marca:
        overallTotal = 0
        totalRows = 0
        submission_date = ''
        product_brand = ''
        for row in resultados_por_marca[resultado]:
            totalRows += 1
            overallTotal += row['overall_rating']
            submission_date = dia
            product_brand = row['product_brand']
        
        media = overallTotal / totalRows
        res = {
            'dia_analisado': submission_date,
            'marca': product_brand,
            'avaliação_média': media
        }
        classificacao.append(res)


    return classificacao
