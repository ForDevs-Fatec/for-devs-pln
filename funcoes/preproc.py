import re
from unidecode import unidecode

def remover_caracteres_especiais(texto):

    # Define a expressão regular para encontrar caracteres especiais
    padrao = re.compile(r'[^a-zA-Z0-ãõÃÕáéíóúâêîôûàèìòùäëïöüçÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÄËÏÖÜÇ\s]', re.UNICODE)
    
    # Substitui os caracteres especiais por uma string vazia
    texto_sem_especiais = re.sub(padrao, '', texto)
    
    return texto_sem_especiais

def executarPreProcessamento(lista):
    documentos = []
    i = 1
    for item in lista:
        documento = {
            "id": i,
            "reviewer_id": item['reviewer_id'],
            "product_id": item["product_id"],
            "review_text": item['review_text'],
            "review_title": item['review_title'],
            "overall_rating": item['overall_rating']
        }
        print('passou aqui!')
        documento["review_text"] = remover_caracteres_especiais(documento["review_text"])
        print('passou aqui!!')
        documento["review_text"] = documento["review_text"].lower()
        print('passou aqui!!!')
        documentos.append(documento)
        i += 1
    return documentos