import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Link para o CSV
# csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'
# df = pd.read_csv(csv_url)

# Pegar as colunas de texto
# colunas_texto = ['review_title', 'review_text']

# Aplicar a tokenização a cada linha das colunas de texto
# for coluna_texto in colunas_texto:
#     df[coluna_texto] = df[coluna_texto].apply(lambda texto: word_tokenize(str(texto), language='portuguese'))

# Acessar os tokens (alterar dependendo do que for necessário)
# linha_tokens = df.loc[0, 'review_text']  

# Printar a linha dos tokens
# print(linha_tokens)

def tokenizar(dados):
    dados_processados = []
    for dado in dados:
        dado['review_title_tokenizado'] = ' '.join(word_tokenize(str(dado['review_title']), language='portuguese'))
        dado['review_text_tokenizado'] = ' '.join(word_tokenize(str(dado['review_text']), language='portuguese'))
        dados_processados.append(dado)
    return dados_processados