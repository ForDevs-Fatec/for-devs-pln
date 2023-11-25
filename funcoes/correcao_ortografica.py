from language_tool_python import LanguageTool
from spellchecker import SpellChecker
import pandas as pd

def remover_duplicidade(texto):
    texto_sem_duplicidade = texto
    if len(texto) > 1:
        texto_sem_duplicidade = texto[0]
        quantidade_duplicados_consoantes = 0
        vogais = ['a', 'e', 'i', 'o', 'u']
        for i in range(1, len(texto)):
            if texto[i] != texto[i - 1]:
                texto_sem_duplicidade += texto[i]
                quantidade_duplicados_consoantes = 0
            else:
                if texto[i] not in vogais and quantidade_duplicados_consoantes < 2:
                    texto_sem_duplicidade += texto[i]
                    quantidade_duplicados_consoantes += 1
    return texto_sem_duplicidade

def corrigir_palavra(word):
    spell = SpellChecker(language='pt')
    corrigido = spell.correction(word)
    return corrigido if corrigido and spell.known([corrigido]) else None

def dividir_silabas(palavra):
    for i in range(1, len(palavra)):
        prefixo = palavra[:i]
        sufixo = palavra[i:]
        corrigido_prefixo = corrigir_palavra(prefixo)
        corrigido_sufixo = corrigir_palavra(sufixo)
        if corrigido_prefixo and corrigido_sufixo:
            return ' '.join([corrigido_prefixo, corrigido_sufixo])
    return palavra

def corrigir_textos(df):
    # Remover duplicidades
    df['review_text_normalized'] = df['review_text_normalized'].apply(remover_duplicidade)
    print("Duplicidades removidas")
    print (df['review_text_normalized'])

    # Corrigir palavras e tratar quando a correção é None
    df['review_text_normalized'] = df['review_text_normalized'].apply(lambda x: [corrigir_palavra(word) or dividir_silabas(word) for word in x.split()])
    df['review_text_normalized'] = df['review_text_normalized'].apply(lambda x: ' '.join(x) if x else '')
    print("Palavras corrigidas em lista")

    return df
