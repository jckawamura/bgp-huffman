# Implementação da Trie, adaptada do site
# https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
# com adaptações para funcionar com endereços IPs e inclusão de ajustes propostos no artigo referência.

from typing import Tuple, Any


# Estrutura básica de um nó da trie
class TrieNode(object):
    def __init__(self, char: str, label=None):
        self.char = char  # caractere binário do endereço IP
        self.children = []  # lista de filhos do nó
        self.word_finished = False  # indica se o nó é folha
        self.label = label  # label do melhor Next Hop associado ao endereço procurado


# Adição de um elemento na trie
#   A: 0.0.0.0/0
#   B: 128.0.0.0/2  (10000000.0.0.0/2)
#   C: 192.0.0.0/2  (11000000.0.0.0/2)
#
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
def add(root, ip_prefix: str, label: int):
    node = root
    if ip_prefix == '':  # tratamento específico para a raiz da árvore.
        root.label = label
        return
    # Devemos passar por cada elemento do IP binário, caminhando pela árvore para inserí-los nas posições corretas.
    for char in ip_prefix:
        found_in_child = False
        # Percorre a árvore enquando o prefixo ainda corresponde
        for child in node.children:
            if child.char == char:
                node = child
                found_in_child = True
                node.word_finished = False
                break
        # Quando não encontra mais o valor inserido, é criado um novo nó
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            node = new_node
    node.word_finished = True
    node.label = label


# Faz leaf push de cada prefixo da árvore para as suas folhas
#
#          +---+
#          |   |
#          +---+
#        0/     \ 1
#      +---+   +---+
#      | A |   |   |
#      +---+   +---+
#            0/     \1
#          +---+   +---+
#          | B |   | C |
#          +---+   +---+
#
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
            if root.children[0].char == '1':  # se já existe um filho do lado direito, surge um novo do lado esquerdo.
                new_node = TrieNode('0', root.label)
            else:  # se já existe um filho do lado esquerdo, surge um novo do lado direito.
                new_node = TrieNode('1', root.label)
            new_node.word_finished = True
            root.children.append(new_node)
            return
        root.label = None


# Dado um endereço IP, procura o prefixo com o maior matching e retorna o label de seu Next Hop
def find_prefix(root, prefix: str) -> Any:
    node = root
    if not root.children:
        return root.label
    # Percorre a árvore até encontrar um nó folha.
    for char in prefix:
        for child in node.children:
            if child.char == char:
                node = child
                if child.word_finished:  # Se encontrar a folha, retorna o label associado.
                    return child.label
                break
