import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

def tokenize_unique(text):
    tokens = word_tokenize(text)
    unique_tokens = list(set(tokens))  # Converte para conjunto para remover duplicatas
    print (unique_tokens)
    return ' '.join(unique_tokens)  # Retorna uma string única
    unique_tokens = list(set(tokens))
    return unique_tokens # retorna uma lista de tokens únicos - 1.14 [PLN]

def tokenizar(df):
    df['review_text_normalized'] = df['review_text_normalized'].apply(tokenize_unique)
    return df
