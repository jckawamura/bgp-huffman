import pandas as pd
import ipaddress


# read_bgp:     retorna uma tabela (DataFrame) com as colunas Network e Next Hop a partir da leitura de um arquivo de
#               BGP. São mantidas apenas as melhores rotas.
# Entradas:
#       file:       caminho do arquivo que contém a tabela BGP.
#       first_row:  indica a posição da primeira linha da tabela.
# Saídas:
#       bgp:        tabela BGP em formato DataFrame.
def read_bgp(file, first_row):
    # Leitura do arquivo com definição de intervalos fixos para cada coluna
    bgp = pd.read_fwf(file,
                      colspecs=[(1, 2), (3, 20), (20, 40)],
                      names=['Status', 'Network', 'Next Hop'],
                      skiprows=first_row)  # ignora o cabeçalho original. Um novo cabeçalho é definido linha acima

    # Preenchimento das células vazias
    bgp['Network'].fillna(method='ffill', inplace=True)  # replica o IP anterior quando não houver (NaN)
    bgp['Next Hop'].fillna(method='backfill', inplace=True)  # replica o próximo Next Hop quando não houver (NaN)

    # Devemos manter apenas as melhores rotas
    bgp.dropna(subset=['Status'], inplace=True)  # mantém apenas as rotas com "Status" '>', ou seja, as melhores rotas
    bgp.drop(axis=1, labels=['Status'], inplace=True)  # a coluna "Status" deixa de ser útil
    return bgp


# ip_next_hop(): retorna uma lista com as duplas IP em binário e label
# Entrada:
#       bgp: DataFrame da tabela BGP
# Saída:
#       lista de labels do Next Hop para cada endereço ip. [ip em binário, label do Next Hop]
def ip_next_hop(bgp: pd.DataFrame):
    ip_label = []
    for index, row in bgp.iterrows():
        ip_network = ipaddress.ip_network(row['Network'])
        # print(ip_network)

        ip_length = str(ip_network).rpartition('/')[2]

        ip_bin = str(bin(int(ipaddress.ip_address(ip_network[0])))[2:].zfill(32))[:int(ip_length)]

        label = ipaddress.ip_address(row['Next Hop'])
        label = str(label).rpartition('.')[2]

        ip_label.append([ip_bin, label])
    return ip_label


# ip_to_bin(): conversão de IP para binário
# Entrada:
#       ip: endereço IP
# Saída:
#       ip_bin: versão binária do endereço IP
def ip_to_bin(ip):
    ip = ipaddress.ip_address(ip)
    ip_bin = bin(int(ip))
    ip_bin = str(ip_bin[2:].zfill(32))
    return ip_bin

# src = "files/amostra_bgp.txt"
# bgp_table = read_bgp(src, 1)
# ip_label_list = ip_next_hop(bgp_table)
# print(ip_label_list)
# print(ip_to_bin("1.0.4.0"))
