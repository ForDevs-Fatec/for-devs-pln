#import do pandinha
import pandas as pd

# tokenização
def tokenizar(texto):
    tokens = texto.split()  
    return tokens

# link do CSV
csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'
df = pd.read_csv(csv_url)

# pegar as colunas (trocar se for necessário)
colunas_texto = ['review_title', 'review_text']

# aplicar a tokenização a cada linha das colunas de texto (trocar se for necessário)
for coluna_texto in colunas_texto:
    df[coluna_texto] = df[coluna_texto].apply(tokenizar)

# acessar os tokens (alterar dependendo do que for necessário)
linha_tokens = df.loc['review_text', 'review_title']  

# printar a linha dos tokens
print(linha_tokens)
