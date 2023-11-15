from language_tool_python import LanguageTool
from spellchecker import SpellChecker

def remover_duplicidade(texto):
    texto_sem_duplicidade = texto[0]
    quantidade_duplicados_consoantes = 0
    vogais = ['a', 'e', 'i', 'o', 'u']

    for i in range(1, len(texto)):
        if texto[i] != texto[i - 1]:
            texto_sem_duplicidade += texto[i]
            quantidade_duplicados_consoantes = 0
        else:
            if texto[i] not in vogais:
                quantidade_duplicados_consoantes += 1
                if quantidade_duplicados_consoantes < 2:
                    texto_sem_duplicidade += texto[i]
            else:
                texto_sem_duplicidade += texto[i]

    return texto_sem_duplicidade

def corrigir_palavra(word):
    portuguese = SpellChecker(language='pt')
    return portuguese.correction(word)

def corrigir_textos(df):
    df['review_text_normalized'] = df['review_text_normalized'].apply(lambda x: [remover_duplicidade(word) for word in x])
    df['review_text_normalized'] = df['review_text_normalized'].apply(lambda x: [corrigir_palavra(word) for word in x])
    return df
