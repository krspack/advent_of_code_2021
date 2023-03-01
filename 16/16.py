
# input A
with open('16_input.txt', encoding = 'utf-8-sig') as txt:
    txt = txt.readlines()
    txt = txt[0][:-1]

# test inputs     VYMAZAT NULY NA KONCI - ZKUSIT...
hex1 = 'D2FE28'
hex2 = '38006F45291200'
hex3 = 'EE00D40C823060'
hex4 = '8A004A801A8002F478'
hex5 = '620080001611562C8802118E34'  # nefunguje, 12
hex6 = 'C0015000016115A2E0802F182340'  # nefunguje, 23
hex7 = 'A0016C880162017C3686B18A3D4780'

input_txt = hex5
print('len hex', len(input_txt))
print('len hex krat 4', len(input_txt)*4)

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
    print('len bin txt', len(bin_txt))
    return bin_txt

input_binary = get_binary_txt()

def is_zeros(chunks_of_binary_txt):
    print(chunks_of_binary_txt)
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
    print(bin_txt), '---'
    version = bin_txt[:3]
    version = int(version, 2)
    id_number = bin_txt[3:6]
    id_number = int(id_number, 2)
    id_index_end = 5
    rest_of_packet = bin_txt[(id_index_end + 1):]
    print(version, id_number, rest_of_packet)
    return version, id_number, rest_of_packet

def get_payload(rest):
    payload = []
    chunks = [rest[x * 5:(x + 1) * 5] for x in range((len(rest) + 5 - 1) // 5 )]
    print(chunks)
    for ind, chunk in enumerate(chunks):    # tady je potreba uchovat zbytek chunku - muze v nich byt dalsi operacni subpaket
        if chunk[0] == '1':   # tady neni return, protoze dokud neni prvni nula, neni to posledni paket
            payload.append(chunk[1:])
        else:
            payload.append(chunk[1:])
            if ind == len(chunks)-1:
                unused_chunks = None
            else:
                unused_chunks = ''.join(chunks[(ind+1):])
            return payload, unused_chunks


def parse_operators(rest):
    zero_one, rest = int(rest[0]), rest[1:]
    print('len rest', len(rest))
    return zero_one, rest

# tyto dve funkce lze rovnou smazat a nahradit je pouhym zkracenim retezce rest..? zkusit
def get_number_of_subpackets(rest_1):
    print('If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.')
    subpackets_count = rest_1[:11]
    subpackets_count = int(subpackets_count, 2)
    print('subpackets count', subpackets_count)
    subpackets = rest_1[11:]
    print(subpackets, subpackets_count)
    return subpackets, subpackets_count

def get_lenght_of_subpackets(rest_0):
    print('If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.')
    subpackets_length = rest_0[:15]
    subpackets_length = int(subpackets_length, 2)
    print('delka', subpackets_length)   # neni s ni asi nutne pocitat / jestli ano, pak pridat do get_payload parametr limit
    subpackets = rest_0[15:]
    return subpackets


def f(binary_txt):
    versions = []
    payloads = []
    while is_zeros(binary_txt) == False:
        version, id_number, rest_of_packet = get_version_id_rest(binary_txt)
        versions.append(version)
        if id_number == 4:
            a, unused_chunks = get_payload(rest_of_packet)
            print(a, unused_chunks)
            payloads.append(a)
            # print(a)
            if is_zeros(unused_chunks) == False:
                binary_txt = unused_chunks
            else:
                payloads = [''.join(x) for x in payloads]
                payloads = [int(x, 2) for x in payloads]
                return payloads, sum(versions)
        else:
            zero_or_one, others = parse_operators(rest_of_packet)
            if zero_or_one == 1:
                subpackets_1, subpackets_count = get_number_of_subpackets(others)
                binary_txt = subpackets_1    # subpackets_count je nevyuzit, ale zbytecny, protoze ve funkci get_payload se pozna posledni balicek s payloadem
            else:
                subpackets_0 = get_lenght_of_subpackets(others)
                binary_txt = subpackets_0
    return payloads, sum(versions)


print(f(input_binary))


