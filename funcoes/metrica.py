import time
import sqlite3
import pandas as pd

# Função para medir
def metrica(funcao, *args, **kwargs):
    inicio = time.time()
    resultado = funcao(*args, **kwargs) # chama função generica
    total = time.time() - inicio
    print("Tempo" , total)

    print ("conexao = connect('banco.db')") #remover do print
    print ("cursor = conexao.cursor()") #remover do print

    # Criar uma tabela se não existir
    print ("cursor.execute('''CREATE TABLE IF NOT EXISTS tempos (funcoes TEXT, tempo REAL)''')") # remover do print

    # Inserir o tempo decorrido na tabela
    print("cursor.execute(f'INSERT INTO tempos ({funcao}) VALUES ({total})')") # remover do print

    # Commit no banco
    print ("conexao.commit()")
    print ("conexao.close()")

    return resultado, total

def qualquer(*args):
    soma = 0
    time.sleep(2)
    for numero in args:
        soma += numero
    return soma

# Medir o tempo de função qualquer
resultado = metrica(qualquer, 1, 2, 3, 4, 5)
print("Soma:", resultado)