from language_tool_python import LanguageTool

def remover_duplicidade(texto):
    texto_sem_duplicidade = texto # Inicializa a nova string com o primeiro caractere
    if len(texto) > 1:
        texto_sem_duplicidade = texto[0]
        encontrou_duplicidade = False
        quantidade_duplicados_consoantes = 0
        vogais = ['a', 'e', 'i', 'o', 'u']
        # Percorre os caracteres da string
        for i in range(1, len(texto)):
            # Adiciona à nova string se o caractere atual for diferente do anterior
            if texto[i] != texto[i - 1]:
                texto_sem_duplicidade += texto[i]
                quantidade_duplicados_consoantes = 0
            else:
                if texto[i] not in vogais and quantidade_duplicados_consoantes < 2:
                    texto_sem_duplicidade += texto[i]
                    quantidade_duplicados_consoantes += 1
                else:
                    encontrou_duplicidade = True
                    

        if encontrou_duplicidade == True:
            print(texto)
            print(texto_sem_duplicidade)
            print('========================================')
    return texto_sem_duplicidade

def corrigir(texto):
    texto_corrigido = texto
    tool = LanguageTool('pt-BR')  # Especifica o idioma (Português do Brasil)

    # Verifica os erros no texto
    erros = tool.check(texto)

    # Imprime os erros encontrados
    for erro in erros:
        print(f'Erro: {erro}')

    # Retorna o texto corrigido
    if len(erros) > 0:
        texto_corrigido = tool.correct(texto)
        print(texto)
        print(texto_corrigido)

    return texto_corrigido

def corrigir_textos(df):
    df['review_text_normalized'] = df['review_text_normalized'].apply(remover_duplicidade)
    #df['review_text_normalized'] = df['review_text_normalized'].apply(corrigir)
    return df