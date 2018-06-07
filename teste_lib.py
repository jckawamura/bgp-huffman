import bz2

src_file = "sample.xml"
dst_file = "sample.xml.bz2"

compress_level = 9
with open(src_file, 'rb') as src:
    tarbz2contents = bz2.compress(src.read(), compress_level)
    print(tarbz2contents)
    with open(dst_file, 'w') as dst:
        dst.write(tarbz2contents)
