# Implementação da Trie, adaptada do site
# https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
# com adaptações para funcionar com endereços IPs e inclusão de ajustes propostos no artigo referência.

from typing import Tuple, Any
import bgp


# Estrutura básica de um nó da trie
class TrieNode(object):
    def __init__(self, char: str, label=None):
        self.char = char  # caractere binário do endereço IP
        self.children = []  # lista de filhos do nó
        self.word_finished = False  # indica se o nó é folha
        self.label = label  # label do melhor Next Hop associado ao endereço procurado


# Adição de um elemento na trie
# Step 1: separate the provided prefixes by protocol (IPv4 vs IPv6),
# and build a Binary Trie per protocol.
#
# For example, if the input prefixes are
#   A: 0.0.0.0/0
#   B: 128.0.0.0/2  (10000000.0.0.0/2 in binary)
#   C: 192.0.0.0/2  (11000000.0.0.0/2)
# the Binary Trie for IPv4 will look like this at the end of step 1:
#          +---+
#          | A |
#          +---+
#               \ 1
#              +---+
#              |   |
#              +---+
#            0/     \1
#          +---+   +---+
#          | B |   | C |
#          +---+   +---+
#
# Note that the prefixes in this example are nested: any IPv4 address
# that matches B or C will also match A. Unfortunately, the classic LC Trie
# algorithm does not support nested prefixes. The next step will solve that
# problem.
def add(root, word: str, label: int):
    node = root
    if word == '':  # tratamento específico para a raiz da árvore.
        root.label = label
        # root.word_finished = True
        return
    # Devemos passar por cada elemento do IP binário, caminhando pela árvore para inserí-los nas posições corretas.
    for char in word:
        found_in_child = False
        for child in node.children:
            if child.char == char:
                node = child
                found_in_child = True
                node.word_finished = False
                break
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            node = new_node
    node.word_finished = True
    node.label = label


# Faz leaf push de cada prefixo da árvore para as suas folhas
#
# Continuing the previous example, the Binary Trie will look like this
# at the end of step 2:
# TODO: corrigir desenho
#          +---+
#          |   |
#          +---+
#        0/     \ 1
#      +---+   +---+
#      | A |   |   |
#      +---+   +---+
#            0/     \1
#          +---+   +---+
#          |A,B|   |A,C|
#          +---+   +---+
#
# This trie yields the same match results as the original trie from
# step 1. But it has a useful new property: now that all the prefixes
# are at the leaves, they are disjoint: no prefix is nested under another.
def leaf_push(root):
    if root.word_finished:  # se já é nó folha, não há necessidade de fazer leaf push
        return
    else:
        for child in root.children:
            if child.char:
                if not child.label:
                    child.label = root.label
                leaf_push(child)
        # Se um nó só tem um filho, ele deve criar um novo herdando o label.
        if len(root.children) == 1:
            if root.children[0].char == '1':    # se já existe um filho do lado direito, surge um novo do lado esquerdo.
                new_node = TrieNode('0', root.label)
            else:   # se já existe um filho do lado esquerdo, surge um novo do lado direito.
                new_node = TrieNode('1', root.label)
            new_node.word_finished = True
            root.children.append(new_node)
            return
        # root.label = None


# Dado um endereço IP, procura o prefixo com o maior matching e retorna o label de seu Next Hop
def find_prefix(root, prefix: str) -> Any:
    node = root
    if not root.children:
        return root.label
    for char in prefix:
        for child in node.children:
            if child.char == char:
                node = child
                break
    return node.label


if __name__ == "__main__":
    src = "files/amostra_bgp.txt"
    # src = "files/lg.vix.ptt.br-20180201000001-IPv4-BGP.txt" # início na linha 15
    bgp_table = bgp.read_bgp(src, 1)
    ip_label_list = bgp.ip_next_hop(bgp_table)

    root = TrieNode('*')
    for x in ip_label_list:
        add(root, x[0], x[1])

    leaf_push(root)

    print("Tabela BGP\n", bgp_table)

    print("\nConversão da tabela BGP")
    for n, i in enumerate(ip_label_list):
        print(ip_label_list[n])


    # Consultas
    while True:
        print("\nConsultar IP:\n")
        print(find_prefix(root, bgp.ip_to_bin(input())))

    # Testes padrão
    print(find_prefix(root, bgp.ip_to_bin("0.0.0.0")))
    print(find_prefix(root, bgp.ip_to_bin("1.0.4.0")))
    print(find_prefix(root, bgp.ip_to_bin("1.0.8.0")))
    print(find_prefix(root, bgp.ip_to_bin("1.0.16.0")))
    print(find_prefix(root, bgp.ip_to_bin("0.1.1.1")))
