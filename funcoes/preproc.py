import re
from unidecode import unidecode
from language_tool_python import LanguageTool

def remover_caracteres_especiais(texto):

    # Define a expressão regular para encontrar caracteres especiais
    padrao = re.compile(r'[^a-zA-ZãõÃÕáéíóúâêîôûàèìòùäëïöüçÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÄËÏÖÜÇ$\s]', re.UNICODE)
    
    # Substitui os caracteres especiais por uma string vazia
    texto_sem_especiais = re.sub(padrao, '', texto)

    texto_sem_especiais = texto_sem_especiais.replace('=', '')
    
    return texto_sem_especiais.lower()

def executarPreProcessamento(df_processado, df):
    df_processado["review_text_normalized"] = df["review_text"].apply(remover_caracteres_especiais)
    print (df_processado["review_text_normalized"])
    return df_processado