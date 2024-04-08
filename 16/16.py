import random
import copy


# test inputs
hex1 = 'D2FE28'
hex2 = '38006F45291200'
hex3 = 'EE00D40C823060'
hex4 = '8A004A801A8002F478'
hex5 = '620080001611562C8802118E34'
hex6 = 'C0015000016115A2E0802F182340'
hex7 = 'A0016C880162017C3686B18A3D4780'

b1 = 'C200B40A82'
b2 = '04005AC33890'
b3 = '880086C3E88112'
b4 = 'CE00C43D881120'
b5 = 'D8005AC2A8F0'
b6 = 'F600BC2D8F'
b6 = '9C005AC2F8F0'
b7 = '9C0141080250320F1802104A08'

# real input
with open('16_input.txt', encoding = 'utf-8-sig') as txt_file:
    lines = txt_file.readlines()
    txt = lines[0][:-1]

input_txt = txt

def get_bin_txt(hex_txt = input_txt):
    bin_txt = bin(int(hex_txt, 16))
    bin_txt = bin_txt[2:]
    first_bit = bin(int(hex_txt[0], 16))[2:]
    if len(first_bit) == 3:
        bin_txt = '0'+bin_txt
    elif len(first_bit) == 2:
        bin_txt = '00'+bin_txt
    elif len(first_bit) == 1:
        bin_txt = '000'+bin_txt
    if hex_txt[0] == '0':
        bin_txt = '00'+bin_txt
    return bin_txt

input_bin = get_bin_txt()

def is_zeros(chunks_of_bin_txt):
    if len(chunks_of_bin_txt) == 0:
        return True
    elif int(chunks_of_bin_txt, 2) == 0:
        return True
    return False

def parse_head(bin_txt):
    version = bin_txt[:3]
    version = int(version, 2)
    id_number = bin_txt[3:6]
    id_number = int(id_number, 2)
    head_len = 6
    after_head = bin_txt[head_len:]
    return version, id_number, head_len

def get_payload(rest):
    payload = []
    literal_packet_length = 0
    end_zeros = 0
    chunks = [rest[x * 5:(x + 1) * 5] for x in range((len(rest) + 5 - 1) // 5 )]
    for ind, chunk in enumerate(chunks):
        if chunk[0] == '1':
            payload.append(chunk[1:])
            literal_packet_length += 5
        else:
            payload.append(chunk[1:])
            literal_packet_length += 5
            if ind == len(chunks)-1:
                unused_chunks = None
                len_unused_chunks = 0
            else:
                unused_chunks = ''.join(chunks[(ind+1):])
                len_unused_chunks = len(unused_chunks)
                if is_zeros(unused_chunks) == True:
                    end_zeros = len_unused_chunks
            payload = ''.join(payload)
            payload = int(payload, 2)
            return payload, literal_packet_length, len_unused_chunks, end_zeros


def do_id_maths(list_payloads, id_n):
    assert id_n < 8
    if id_n == 0:
        return sum(list_payloads)
    if id_n == 1:
        result = 1
        for item in list_payloads:
            result *= item
        return result
    if id_n == 2:
        return min(list_payloads)
    if id_n == 3:
        return max(list_payloads)
    if id_n == 5:
        assert len(list_payloads) == 2
        if list_payloads[0] > list_payloads[1]:
            return 1
        else:
            return 0
    if id_n == 6:
        assert len(list_payloads) == 2
        if list_payloads[0] < list_payloads[1]:
            return 1
        else:
            return 0
    if id_n == 7:
        assert len(list_payloads) == 2
        if list_payloads[0] == list_payloads[1]:
            return 1
        else:
            return 0

def parse_operators(txt_input):
    if txt_input[0] == '0':
        packet_len = int(txt_input[1:16], 2)
        no_packets = None
        index_jump = 16
    else:
        no_packets = int(txt_input[1:12], 2)
        packet_len = None
        index_jump = 12
    return packet_len, no_packets, index_jump





# b

def f_indices(bin_txt, i, sub_payloads):
    len_unused_chunks = 0
    version, id_number, head_len = parse_head(bin_txt[i:])
    i += head_len
    while is_zeros(bin_txt[i:]) != True:
        if id_number != 4:
            payload = 0
            packet_len, no_packets, index_jump = parse_operators(bin_txt[i:])
            i += index_jump
            sub_payloads = []
            if packet_len != None:
                next_packet_start = copy.deepcopy(i)+packet_len
                while i < next_packet_start:
                    if is_zeros(bin_txt[i:]) != True:
                        i, sub_payload = f_indices(bin_txt, i, sub_payloads)
                        sub_payloads.append(sub_payload)
                payload = do_id_maths(sub_payloads, id_number)
                return i, payload
            else:
                for _ in range(no_packets):
                    if is_zeros(bin_txt[i:]) != True:
                        i, sub_payload = f_indices(bin_txt, i, sub_payloads)
                        sub_payloads.append(sub_payload)
                payload = do_id_maths(sub_payloads, id_number)
                return i, payload
        else:
            payload, packet_length, len_unused_chunks, end_zeros = get_payload(bin_txt[i:])
            i += packet_length
            if is_zeros(bin_txt[i:]) == True:
                i += end_zeros
                assert len(bin_txt) == i
            return i, payload

    return i, payload
print(f_indices(input_bin, 0, []))




