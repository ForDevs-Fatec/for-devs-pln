import nltk
from nltk.corpus import stopwords
import time

nltk.download('stopwords')
stop_words = set(stopwords.words('portuguese'))
stop_words.remove('não')

# Função para remover stopwords e formatar as palavras
def remover_stopwords(texto):
    palavras = nltk.word_tokenize(texto.lower())
    palavras_sem_stopwords = [f"'{palavra.strip()}'" for palavra in palavras if palavra.isalnum() and palavra not in stop_words]
    return f"[{', '.join(palavras_sem_stopwords)}]"

def executar_pipeline(df):
    inicio = time.time()
    df['review_text_normalized'] =  df['review_text_normalized'].apply(remover_stopwords)
    tempo = time.time() - inicio
    return df, tempo
