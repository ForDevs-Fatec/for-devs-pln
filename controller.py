
from fastapi import FastAPI
import psycopg2
from pipeline import pipeline, conexaoMongo
from funcoes import pesquisa, analises
from dotenv import load_dotenv
import os
import urllib.parse as up
import json
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson.json_util import dumps

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

client = conexaoMongo.conectarMongo()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return(analises.analisar(valor=dia, tipo=tipo, analise='dia', cur=cur))
    except:
        {"erro": "erro ao executar análise"} 

@app.get("/analise/por-estado/{estado}/{tipo}")
def analisarPorEstado(estado, tipo):
    try:
        return(analises.analisar(valor=estado, tipo=tipo, analise='estado', cur=cur))
    except:
        {"erro": "erro ao executar análise"}

@app.get("/analise/por-genero/{genero}/{tipo}")
def analisarPorGenero(genero, tipo):
    try:
        return(analises.analisar(valor=genero, tipo=tipo, analise='genero', cur=cur))
    except:
        {"erro": "erro ao executar análise"}

@app.get("/analise/por-idade/{anoNascimento}/{tipo}")
def analisarPorIdade(anoNascimento, tipo):
    try:
        return(analises.analisar(valor=anoNascimento, tipo=tipo, analise='idade', cur=cur))
    except:
        {"erro": "erro ao executar análise"}

@app.put("/pipeline")
def executarPipeline():
    try:
        pipeline.executarPipeline(conn=conn, cur=cur, url=url, client=client)
        return {"message": "banco atualizado"}
    except:
        return {"erro": "erro ao atualizar banco"}
    
@app.get("/get-all")
def getAll():
    try:
        # Recupere todos os documentos e converta para uma lista de dicionários
        dados_cursor = client['dados'].find()
        
        # Use dumps do bson.json_util para serializar os dados
        dados_json = dumps(dados_cursor)
        
        # Converta o JSON serializado de volta para um dicionário Python
        dados = json.loads(dados_json)
        
        return {"data": dados}
    except:
        return {"erro": "erro ao buscar dados"}

@app.get("/get-all-processados")
def getAllProcessados():
    try:
        # Recupere todos os documentos e converta para uma lista de dicionários
        dados_cursor = client['dados_processados'].find()
        
        # Use dumps do bson.json_util para serializar os dados
        dados_json = dumps(dados_cursor)
        
        # Converta o JSON serializado de volta para um dicionário Python
        dados = json.loads(dados_json)
        
        return {"data": dados}
    except:
        return {"erro": "erro ao buscar dados"}