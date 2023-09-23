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