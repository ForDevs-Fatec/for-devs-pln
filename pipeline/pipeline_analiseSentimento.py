import pandas as pd
from textblob import TextBlob

# Link para o CSV
csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'
df = pd.read_csv(csv_url)

# Pegar as colunas de texto
colunas_texto = ['review_title', 'review_text']

# Aplicar a análise de sentimentos a cada linha das colunas de texto
for coluna_texto in colunas_texto:
    df[coluna_texto + '_sentiment'] = df[coluna_texto].apply(lambda texto: TextBlob(texto).sentiment.polarity)

# Determinar o sentimento com base na polaridade
def determinar_sentimento(polaridade):
    if polaridade > 0:
        return 'Sentimento positivo'
    elif polaridade < 0:
        return 'Sentimento negativo'
    else:
        return 'Sentimento neutro'

# Aplicar a determinação de sentimento
for coluna_texto in colunas_texto:
    df[coluna_texto + '_sentimento'] = df[coluna_texto + '_sentiment'].apply(determinar_sentimento)

# Exemplo: Pegar o sentimento da primeira linha da coluna 'review_text'
sentimento_exemplo = df.loc[0, 'review_text_sentimento']
print(sentimento_exemplo)
