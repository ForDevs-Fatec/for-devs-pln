
from fastapi import FastAPI
import psycopg2
from pipeline import pipeline
from funcoes import pesquisa, analises
from dotenv import load_dotenv
import os
import urllib.parse as up
import json


app = FastAPI()

load_dotenv()

up.uses_netloc.append("postgres")
url = up.urlparse(os.getenv('DB_URL'))

conn = psycopg2.connect(
            database=url.path[1:],
            password = url.password,
            user=url.username,
            host=url.hostname,
            port=url.port
        )

cur = conn.cursor()

@app.get("/")
def hello_world_root():
    return {"Hello": "World"}

@app.get("/pesquisa/{parametro_de_pesquisa}")
def pesquisar(parametro_de_pesquisa: str):
    try:
        resposta = pesquisa.pesquisarReviews(param=parametro_de_pesquisa, conn=conn, cur=cur)
        return resposta
    except:
        {"erro": "erro ao executar busca"} 

@app.get("/analise/classificacao-produtos")
def analisarClassificacaoProdutos():
    try:
        return(analises.analisarPorDataGeral(conn=conn, cur=cur))
    except:
        {"erro": "erro ao executar análise"}

@app.get("/analise/por-dia/{dia}/{tipo}")
def analisarPorDia(dia, tipo):
    try:
        if tipo == 'marca':
            return(analises.analisarPorDiaMarca(dia=dia, conn=conn, cur=cur))
        if tipo == 'produto':
            return(analises.analisarPorDiaProduto(dia=dia, conn=conn, cur=cur))
        if tipo == 'categoria':
            return(analises.analisarPorDiaCategoria(dia=dia, conn=conn, cur=cur))
    except:
        {"erro": "erro ao executar análise"} 


@app.put("/pipeline")
def executarPipeline():
    try:
        pipeline.executarPipeline(conn=conn, cur=cur, url=url)
        return {"message": "banco atualizado"}
    except:
        return {"erro": "erro ao atualizar banco"}