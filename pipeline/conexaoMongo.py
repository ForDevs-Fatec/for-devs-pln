from pymongo import MongoClient
from dotenv import load_dotenv
import os

def conectarMongo():
    load_dotenv()

    client = MongoClient(os.getenv("DB_URL_MONGO"))
    return client['ForDevs']