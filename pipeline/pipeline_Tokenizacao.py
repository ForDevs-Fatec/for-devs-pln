import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import time

def tokenize_unique(text):
    tokens = word_tokenize(text)
    unique_tokens = list(set(tokens))
    return ' '.join(unique_tokens) # retorna uma lista de tokens únicos - 1.14 [PLN]

def tokenizar(df):
    inicio = time.time()
    df['review_text_normalized'] = df['review_text_normalized'].apply(tokenize_unique)
    tempo = time.time() - inicio
    return df, tempo
