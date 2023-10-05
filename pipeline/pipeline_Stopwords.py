# importando as libs
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

# definindo as stop words
stop_words = set(["produto", "ótimo", "estrelas"])

# git do CSV
csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'

# CSV -> DataFrame do pandas
df = pd.read_csv(csv_url)

# colunas do DataFrame que contêm texto pro processamento
colunas_texto = ['review_title', 'review_text']

# remover as desgraça de stopwords
def remover_stopwords(texto):
    palavras = str(texto).split()
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra.lower() not in stop_words]
    return ' '.join(palavras_sem_stopwords)

# aplicar a remoção de stop words às colunas de texto
for coluna in colunas_texto:
    df[coluna] = df[coluna].apply(remover_stopwords)

# printa o df com as stopwords removidas
print(df)

