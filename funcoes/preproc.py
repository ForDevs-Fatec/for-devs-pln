import re
from unidecode import unidecode
from language_tool_python import LanguageTool
import time

def remover_caracteres_especiais(texto):

    # Define a expressão regular para encontrar caracteres especiais
    padrao = re.compile(r'[^a-zA-ZãõÃÕáéíóúâêîôûàèìòùäëïöüçÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÄËÏÖÜÇ$\s]', re.UNICODE)
    
    # Substitui os caracteres especiais por uma string vazia
    texto_sem_especiais = re.sub(padrao, '', texto)

    texto_sem_especiais = texto_sem_especiais.replace('=', '')
    
    return texto_sem_especiais.lower()

def executarPreProcessamento(df_processado, df):
    inicio = time.time()
    df_processado["review_text_normalized"] = df["review_text"].apply(remover_caracteres_especiais)
    tempo = time.time() - inicio
    return df_processado, tempo