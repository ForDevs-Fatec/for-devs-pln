import pandas as pd
import nltk
nltk.download('stopwords')

# lista personalizada de stopwords
stop_words_custom = set([
    'a', 'o', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'do', 'da', 'dos', 'das', 'em', 'para', 'por', 'com', 'sem', 'e', 'mas',
    'ou', 'que', 'se', 'quando', 'onde', 'como', 'porquê', 'quem', 'isso', 'aquilo', 'este', 'esse', 'aquele', 'ela', 'ele', 'eles',
    'elas', 'nós', 'vós', 'vocês', 'eu', 'você', 'tu', 'muito', 'pouco', 'bom', 'ruim', 'bonito', 'feio', 'grande', 'pequeno', 'novo',
    'velho', 'caro', 'barato', 'fácil', 'difícil', 'rápido', 'lento', 'perto', 'longe', 'aqui', 'ali', 'lá', 'agora', 'depois', 'ontem',
    'hoje', 'amanhã', 'muito', 'pouco', 'bom', 'ruim', 'bonito', 'feio', 'grande', 'pequeno', 'novo', 'velho', 'caro', 'barato',
    'fácil', 'difícil', 'rápido', 'lento', 'perto', 'longe', 'aqui', 'ali', 'lá', 'agora', 'depois', 'ontem', 'hoje', 'amanhã',
    'de', 'acordo', 'com', 'primeiro', 'segundo', 'terceiro', 'lugar', 'no', 'entanto', 'outro', 'além', 'disso', 'concluindo',
    'fim', 'que', 'a', 'partir', 'até', 'desde', 'durante', 'antes', 'depois', 'que', 'assim', 'então', 'portanto', 'dessa',
    'forma', 'dessa', 'maneira', 'dessa', 'forma', 'dessa', 'maneira', 'eu', 'você', 'ele', 'ela', 'nós', 'vós', 'vocês',
    'eles', 'elas', 'meu', 'seu', 'seu', 'dela', 'nosso', 'vosso', 'vosso', 'deles', 'delas', 'este', 'esse', 'aquele',
    'esta', 'essa', 'aquela', 'aquilo', 'isso', 'isso', 'o', 'que', 'quem', 'como', 'quando', 'onde', 'por', 'que', 'qual',
    'quanto', 'se', 'mas', 'ou', 'e', 'porque', 'pois', 'por', 'isso', 'logo', 'portanto', 'assim', 'então'
])

# Link do CSV
csv_url = 'https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/master/B2W-Reviews01.csv'

# Lendo o CSV pro df do pandas
df = pd.read_csv(csv_url)

# Colunas do DataFrame com o texto
colunas_texto = ['review_title', 'review_text']

# Função para remover stopwords
def remover_stopwords(texto):
    palavras = str(texto).split()
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra.lower() not in stop_words_custom]
    return ' '.join(palavras_sem_stopwords)

# Aplicar a remoção das stops
for coluna in colunas_texto:
    df[coluna] = df[coluna].apply(remover_stopwords)

# Exibir o bagulho
print(df)
