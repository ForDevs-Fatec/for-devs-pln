import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
# lista de stopwords
stop_words = set(stopwords.words('portuguese'))
stop_words.remove('não')

# Função para remover stopwords e formatar as palavras
def remover_stopwords_formatar(texto):
    palavras = nltk.word_tokenize(texto.lower())
    palavras_sem_stopwords = [f"'{palavra.strip()}'" for palavra in palavras if palavra.isalnum() and palavra not in stop_words]
    return f"[{', '.join(palavras_sem_stopwords)}]"

def executar_pipeline(df):
    df['review_text_normalized'] = df['review_text'].apply(remover_stopwords_formatar)
    return df