

# test inputs
hex1 = 'D2FE28'
hex2 = '38006F45291200'
hex3 = 'EE00D40C823060'
hex4 = '8A004A801A8002F478'
hex5 = '620080001611562C8802118E34'
hex6 = 'C0015000016115A2E0802F182340'
hex7 = 'A0016C880162017C3686B18A3D4780'

# real input
with open('16_input.txt', encoding = 'utf-8-sig') as txt:
    txt = txt.readlines()
    txt = txt[0][:-1]
input_txt = txt

def get_binary_txt(hex_txt = input_txt):
    bin_txt = bin(int(hex_txt, 16))
    bin_txt = bin_txt[2:]
    first_bit = bin(int(hex_txt[0], 16))[2:]
    if len(first_bit) == 3:
        bin_txt = '0'+bin_txt
    elif len(first_bit) == 2:
        bin_txt = '00'+bin_txt
    elif len(first_bit) == 1:
        bin_txt = '000'+bin_txt
    return bin_txt

input_binary = get_binary_txt()

def is_zeros(chunks_of_binary_txt):  # a few lines are likely redundant
    if chunks_of_binary_txt == None:
        return True
    elif len(chunks_of_binary_txt) == 0:
        return True
    elif int(chunks_of_binary_txt, 2) == 0:
        return True
    elif (type(chunks_of_binary_txt) == list) and (int(chunks_of_binary_txt[0], 2) == 0):
        return True
    elif (type(chunks_of_binary_txt) == list) and (chunks_of_binary_txt[0] in [i*'0' for i in range(10)]):
        return True
    return False

def get_version_id_rest(bin_txt):
    version = bin_txt[:3]
    version = int(version, 2)
    id_number = bin_txt[3:6]
    id_number = int(id_number, 2)
    id_index_end = 5
    rest_of_packet = bin_txt[(id_index_end + 1):]
    return version, id_number, rest_of_packet

def get_payload(rest):
    payload = []
    chunks = [rest[x * 5:(x + 1) * 5] for x in range((len(rest) + 5 - 1) // 5 )]
    for ind, chunk in enumerate(chunks):
        if chunk[0] == '1':
            payload.append(chunk[1:])
        else:
            payload.append(chunk[1:])
            if ind == len(chunks)-1:
                unused_chunks = None
            else:
                unused_chunks = ''.join(chunks[(ind+1):])
            return payload, unused_chunks


def parse_operators(rest):
    zero_one = rest[0]
    if zero_one == '0':
        rest = rest[16:]
    else:
        rest = rest[12:]
    return rest


def f(binary_txt):
    versions = []
    payloads = []
    while is_zeros(binary_txt) == False:
        version, id_number, rest_of_packet = get_version_id_rest(binary_txt)
        versions.append(version)
        if id_number == 4:
            a, unused_chunks = get_payload(rest_of_packet)
            payloads.append(a)
            if is_zeros(unused_chunks) == False:
                binary_txt = unused_chunks
            else:
                payloads = [''.join(x) for x in payloads]
                payloads = [int(x, 2) for x in payloads]
                return payloads, sum(versions)
        else:
            rest = parse_operators(rest_of_packet)
            binary_txt = rest

    return payloads, sum(versions)


print(f(input_binary))


