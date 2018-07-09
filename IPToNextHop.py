import ipaddress


class IPToNextHop(object):
    """
    Par prefixo IP - Next Hop
    """

    def __init__(self, network: ipaddress, next_hop: ipaddress):
        self.network = network
        self.next_hop = next_hop
