import pandas as pd

src = "amostra_bgp.txt"

pd.set_option("max_rows", 5)

bgp = pd.read_table(src, header=None, delim_whitespace=True)

bgp