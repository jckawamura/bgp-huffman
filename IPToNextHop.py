import ipaddress


class IPToNextHop(object):
    """
    Par prefixo IP - Next Hop
    """

    def __init__(self, network: ipaddress, next_hop: ipaddress):
        self.network = network
        self.next_hop = next_hop

# TODO: adicionar este comando no algoritmo da trie
print(ipaddress.ip_address('1.0.0.0') in ipaddress.ip_network('0.0.0.0/0'))