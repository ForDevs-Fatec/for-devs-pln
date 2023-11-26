from language_tool_python import LanguageTool
from spellchecker import SpellChecker

portuguese = SpellChecker(language='pt')

def remover_duplicidade_e_corrigir(texto):

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
                    # Verifica se a palavra corrigida existe antes de adicionar
                    palavra_corrigida = corrigir_palavra(texto[i])
                    if palavra_corrigida:
                        texto_sem_duplicidade += palavra_corrigida
            else:
                texto_sem_duplicidade += texto[i]

    return texto_sem_duplicidade

def corrigir_palavra(word):
    return portuguese.correction(word)

def corrigir_textos(df):
    df['review_text_normalized'] = df['review_text_normalized'].apply(remover_duplicidade_e_corrigir)
    print (df['review_text_normalized'])
    print ('correção')
    return df
