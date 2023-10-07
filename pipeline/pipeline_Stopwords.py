import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

# Carregando as stopwords em português
stop_words = set(stopwords.words('portuguese'))

# Link para o CSV
csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'

# Lendo o CSV para um DataFrame do pandas
df = pd.read_csv(csv_url)

# Colunas do DataFrame que contêm texto para processamento
colunas_texto = ['review_title', 'review_text']

# Função para remover stopwords
def remover_stopwords(texto):
    palavras = str(texto).split()
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra.lower() not in stop_words]
    return ' '.join(palavras_sem_stopwords)

# Aplicar a remoção de stopwords às colunas de texto
for coluna in colunas_texto:
    df[coluna] = df[coluna].apply(remover_stopwords)

# Exibir o DataFrame com as stopwords removidas
print(df)
