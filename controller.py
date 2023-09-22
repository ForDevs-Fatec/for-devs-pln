
from fastapi import FastAPI
from pipeline import pipeline

app = FastAPI()

@app.get("/")
def hello_world_root():
    return {"Hello": "World"}

@app.put("/pipeline")
def executarPipeline():
    try:
        pipeline.executarPipeline()
        return {"message": "banco atualizado"}
    except:
        return {"erro": "erro ao atualizar banco"}