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
            if texto[i] not in vogais and quantidade_duplicados_consoantes < 2:
                texto_sem_duplicidade += texto[i]
                quantidade_duplicados_consoantes += 1
    return texto_sem_duplicidade

def corrigir(texto):
    portuguese = SpellChecker(language='pt')
    texto_corrigido = [portuguese.correction(word) for word in texto]
    return texto_corrigido

#def corrigir_textos(df):
#    df['review_text_normalized'] = df['review_text_normalized'].apply(remover_duplicidade)
#    df['review_text_normalized'] = df['review_text_normalized'].apply(corrigir)
#    return df

texto = ['sempree', 'compro', 'Americanass', 'recomemdo', 'loja', 'amigos', 'bom', 'demaisss']

dados_sem_duplicidade = [remover_duplicidade(palavra) for palavra in texto]
dados_corrigidos = corrigir(dados_sem_duplicidade)

print("Palavras sem duplicidade:", dados_sem_duplicidade)
print("Palavras corrigidas:", dados_corrigidos)