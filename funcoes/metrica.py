import time
from sqlalchemy import create_engine

def conectar_banco(conn, cur):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tempos (
        funcao TEXT, 
        tempo FLOAT);
    """
    insert = """INSERT INTO tempos VALUES""", (funcao.__name__, total)
    cur.execute(create_table_query, insert)
    conn.commit()
    return True

def metrica(funcao, *args, **kwargs):
    inicio = time.time()
    funcao(*args, **kwargs)  # chama função genérica
    total = time.time() - inicio

    conectar_banco()

    return total