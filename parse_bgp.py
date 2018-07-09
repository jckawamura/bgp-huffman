import pandas as pd

# pd.set_option("max_rows", 19)


def read_bgp(file):
    bgp = pd.read_fwf(file, colspecs=[(1, 2), (3, 20), (20, 40)], names=['Status', 'Network', 'Next Hop'], skiprows=1)
    return bgp

#teste
src = "files/amostra_bgp.txt"
print(read_bgp(src))
