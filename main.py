import bgp
import trie_ip


def main():
    src = "files/amostra_bgp.txt"
    # src = "files/bgp.txt"
    bgp_table = bgp.read_bgp(src, 15)   # início na linha 15
    ip_label_list = bgp.ip_next_hop(bgp_table)

    root = trie_ip.TrieNode('*')
    for x in ip_label_list:
        trie_ip.add(root, x[0], x[1])

    trie_ip.leaf_push(root)

    print("Tabela BGP\n", bgp_table)

    print("\nConversão da tabela BGP")
    for n, i in enumerate(ip_label_list):
        print(ip_label_list[n])

    # Consultas
    while True:
        print("Consultar IP:")
        print(trie_ip.find_prefix(root, bgp.ip_to_bin(input())))

    # Testes padrão
    # print(trie_ip.find_prefix(root, bgp.ip_to_bin("0.0.0.0")))
    # print(trie_ip.find_prefix(root, bgp.ip_to_bin("1.0.4.0")))
    # print(trie_ip.find_prefix(root, bgp.ip_to_bin("1.0.8.0")))
    # print(trie_ip.find_prefix(root, bgp.ip_to_bin("1.0.16.0")))
    # print(trie_ip.find_prefix(root, bgp.ip_to_bin("0.1.1.1")))


if __name__ == "__main__":
    main()
