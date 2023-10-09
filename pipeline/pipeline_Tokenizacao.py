import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Link para o CSV
csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'
df = pd.read_csv(csv_url)

# Pegar as colunas de texto
colunas_texto = ['review_title', 'review_text']

# Aplicar a tokenização a cada linha das colunas de texto
for coluna_texto in colunas_texto:
    df[coluna_texto] = df[coluna_texto].apply(lambda texto: word_tokenize(texto, language='portuguese'))

# Acessar os tokens (alterar dependendo do que for necessário)
linha_tokens = df.loc[0, 'review_text']  

# Printar a linha dos tokens
print(linha_tokens)
