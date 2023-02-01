

hex1 = 'D2FE28'
hex2 = '38006F45291200'  # z nejakeho duvodu nefunguje
hex3 = 'EE00D40C823060'

def get_binary_txt(hex_txt):
    bin_txt = bin(int(hex_txt, 16))
    return bin_txt[2:]
bin_txt = get_binary_txt(hex3)

def get_version_id(bin_txt = bin_txt):
    version = bin_txt[:3]
    version = int(version, 2)
    id_number = bin_txt[3:6]
    id_number = int(id_number, 2)
    id_index_end = 5
    rest = bin_txt[(id_index_end + 1):]
    return version, id_number, id_index_end, rest
result = get_version_id(hex3)
version = result [0]
id_number = result [1]
id_index_end = result [2]
rest = result [3]
print(rest)

""" for version 4
def parse_literal_value(literal_bits):  # pouzit slicing s udajem o kroku
    chunks = [literal_bits[x * 5:(x + 1) * 5] for x in range((len(literal_bits) + 5 - 1) // 5 )]
    values = []
    for chunk in chunks:
        if chunk[0] != '0':
            values.append(chunk[1:])
        else:
            values.append(chunk[1:])
            values = ''.join(values)
            values = int(values, 2)
            return values
print(parse_literal_value(rest))
"""

def parse_operators(rest = rest):
    if rest[0] == '1':
        subpackets = rest[1:12]
        subpackets = int(subpackets, 2)
        print(subpackets)
        literal_packets = rest[12:]  # a v tom dany pocet paketu
        print(literal_packets)

    else:
        subpackets = rest[1:16]
        subpackets = int(subpackets, 2)
        print(subpackets)
        literal_packets = rest[16:(subpackets+1)]
        print(literal_packets)

print(parse_operators())


