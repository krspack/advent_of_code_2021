"""
prepsat tak, aby to nebyla funkce ve funkci, ale sada co nejmensich funkci
ty se pak volaji po sobe, jsou dobre pojmenovane a neni v tom bordel v podavani argumentu
"""




hex1 = 'D2FE28'
hex2 = '38006F45291200'  # z nejakeho duvodu nefunguje
hex3 = 'EE00D40C823060'
hex4 = '8A004A801A8002F478'

def f(input_txt):

    def get_binary_txt(hex_txt = input_txt):
        bin_txt = bin(int(hex_txt, 16))
        return bin_txt
    binary_txt = get_binary_txt()
    print(binary_txt)

    payload_storage = []

    def get_version_id_rest(payload = payload_storage, bin_txt = binary_txt):
        bin_txt = bin_txt.replace('0b', '')  # minus '0b'
        version = bin_txt[:3]
        version = int(version, 2)
        print('version ', version)
        id_number = bin_txt[3:6]
        id_number = int(id_number, 2)
        id_index_end = 5
        rest_of_packet = bin_txt[(id_index_end + 1):]
        print('get_version_id_rest: ', version, id_number, rest_of_packet)

        if id_number == 4:
            print('id_number: 4')
            def parse_literal_value(literal_bits, payload):
                chunks = [literal_bits[x * 5:(x + 1) * 5] for x in range((len(literal_bits) + 5 - 1) // 5 )]
                print(chunks)
                for ind, chunk in enumerate(chunks):    # tady je potreba uchovat zbytek chunku - muze v nich byt dalsi operacni subpaket
                    print(ind, chunk)
                    if chunk[0] != '0':
                        payload.append(chunk[1:])
                    else:
                        payload.append(chunk[1:])
                        payload = ''.join(payload)
                        payload = int(payload, 2)
                        try:
                            unused_chunks = chunks[ind+1:]
                            unused_chunks = ''.join(unused_chunks)
                            print('unused_chunks ', unused_chunks)
                            if int(unused_chunks, 2) == 0:     # meaningless zeros at the end >>> tento chunk byl posledni, lze return
                                return payload
                            else:
                                print('payload ', payload, id(payload))
                                print('payload storage ', payload_storage, id(payload_storage))
                                get_version_id_rest(payload, unused_chunks)
                        except IndexError:
                            return payload
                        return payload
            package_payload = parse_literal_value(rest_of_packet, payload_storage)
            print(package_payload)

        else:
            print('id_number: else')
            def parse_operators(rest = rest_of_packet):
                if rest[0] == '1':
                    print('If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.')
                    subpackets = rest[1:12]
                    subpackets = int(subpackets, 2)
                    print(subpackets)
                    literal_packets = rest[12:]  # a v tom dany pocet paketu
                    print(literal_packets)
                    literal_packets = [literal_packets[x * 11:(x + 1) * 11] for x in range((len(literal_packets) + 1 - 1) // 11 )]
                    print(literal_packets)
                    for packet in literal_packets:
                        print('len packet', len(packet))
                        get_version_id_rest(payload_storage, packet)

                else:
                    print('If the length type ID is 0... ')
                    subpackets_length = rest[1:16]
                    subpackets_length = int(subpackets_length, 2)
                    print(subpackets_length)
                    literal_packets = rest[(16+subpackets_length+1):]
                    print('rest ', rest)
                    print('literal packets ', literal_packets)
                    if literal_packets != '':
                        'jsou tu subpakety'
                        get_version_id_rest(payload_storage, literal_packets)
                    else:
                        'zadne subpakety'
            print(parse_operators())
    print(get_version_id_rest())

print(f(hex3))


