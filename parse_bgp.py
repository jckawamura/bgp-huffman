import pandas as pd


# read_bgp():   retorna uma tabela (DataFrame) com as colunas Network e Next Hop a partir da leitura de um arquivo de
#               BGP. São mantidas apenas as melhores rotas.
# file:         caminho do arquivo que contém a tabela BGP.
# first_row:    indica a posição da primeira linha da tabela.
def read_bgp(file, first_row):
    bgp = pd.read_fwf(file,
                      colspecs=[(1, 2), (3, 20), (20, 40)],
                      names=['Status', 'Network', 'Next Hop'],
                      skiprows=first_row)

    # Devemos manter apenas as melhores rotas
    bgp['Network'].fillna(method='ffill', inplace=True)  # replica o IP anterior quando não houver (NaN)
    bgp.dropna(subset=['Status'], inplace=True)  # mantém apenas as rotas com "Status" '>', ou seja, as melhores rotas
    # TODO: Testar se existe algum status diferente de '>'
    bgp.drop(axis=1, labels=['Status'], inplace=True)  # a coluna "Status" deixa de ser útil
    return bgp


# Teste com o arquivo de amostra
src = "files/amostra_bgp.txt"
print(read_bgp(src, 1))
