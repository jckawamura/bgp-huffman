# https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1

from typing import Tuple, Any
import bgp
import pandas as pd


class TrieNode(object):
    def __init__(self, char: str, label=None):
        self.char = char
        self.children = []
        self.word_finished = False
        self.label = label


def add(root, word: str, label: int):
    node = root
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


def leafpush(root):
    if root.word_finished:
        return True
    else:
        for child in root.children:
            if child.char:
                if not child.label:
                    child.label = root.label
                leafpush(child)
        if len(root.children) == 1:
            if root.children[0].char == '1':
                new_node = TrieNode('0', root.label)
            else:
                new_node = TrieNode('1', root.label)
            new_node.word_finished = True
            root.children.append(new_node)
            return True
        root.label = None


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
    bgp_table = bgp.read_bgp(src, 1)
    ip_label_list = bgp.ip_next_hop(bgp_table)

    root = TrieNode('*', 4)

    for x in ip_label_list:
        add(root, x[0], x[1])

    # add(root, "100", 4)
    # add(root, "0", 40)
    # add(root, "000", 43)
    # add(root, "0111", 42)
    #
    #
    leafpush(root)

    print("Tabela BGP\n", bgp_table)
    print("\nConversão da tabela BGP\n", ip_label_list)

    print("\nTestes:\n")
    print(find_prefix(root, "00000000000000000000000000000000"))
    print(find_prefix(root, "00000001000000000000010000000000"))
    print(find_prefix(root, "00000001000000000000010000000001"))
    print(find_prefix(root, "00000001000000000000010000000010"))
