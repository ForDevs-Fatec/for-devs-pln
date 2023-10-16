import re
from unidecode import unidecode
from language_tool_python import LanguageTool

def remover_caracteres_especiais(texto):

    # Define a expressão regular para encontrar caracteres especiais
    padrao = re.compile(r'[^a-zA-Z0-ãõÃÕáéíóúâêîôûàèìòùäëïöüçÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÄËÏÖÜÇ$\s]', re.UNICODE)
    
    # Substitui os caracteres especiais por uma string vazia
    texto_sem_especiais = re.sub(padrao, ' ', texto)
    
    return texto_sem_especiais

def executarPreProcessamento(df_processado, df):
    df_processado["review_text_normalized"] = df["review_text"].apply(remover_caracteres_especiais)
    return df_processado