import pandas as pd

pd.set_option("max_rows", 5)


def read_bgp(file):
    fields = ['Network', 'Next']
    bgp = pd.read_csv(file, sep='\s+', skipinitialspace=True, usecols=fields)
    bgp
    pass


src = "files/amostra_bgp.txt"
read_bgp(src)
