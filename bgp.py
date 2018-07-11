import pandas as pd
import ipaddress


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


# ip_next_hop(): retorna uma lista com as duplas IP em binário e label
# bgp: DataFrame da tabela BGP
def ip_next_hop(bgp: pd.DataFrame):
    ip_label = []
    for index, row in bgp.iterrows():
        ip_network = ipaddress.ip_network(row['Network'])
        ip_bin = bin(int(ip_network[0]))
        ip_length = str(ip_network).rpartition('/')[2]
        label = ipaddress.ip_address(row['Next Hop'])
        label = str(label).rpartition('.')[2]
        ip_bin = str(ip_bin[2:].zfill(int(ip_length)))
        ip_label.append([ip_bin, label])
    return ip_label

# src = "files/amostra_bgp.txt"
# bgp_table = read_bgp(src, 1)
# ip_label_list = ip_next_hop(bgp_table)
# print(ip_label_list)