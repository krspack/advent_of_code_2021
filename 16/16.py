import random

# test inputs
hex1 = 'D2FE28'
hex2 = '38006F45291200'
hex3 = 'EE00D40C823060'
hex4 = '8A004A801A8002F478'
hex5 = '620080001611562C8802118E34'
hex6 = 'C0015000016115A2E0802F182340'
hex7 = 'A0016C880162017C3686B18A3D4780'

b1 = 'C200B40A82'
b2 = '04005AC33890'  # ID 1, finds the product of 6 and 9, resulting in the value 54.
b3 = '880086C3E88112'
b4 = 'CE00C43D881120'
b5 = 'D8005AC2A8F0'
b6 = 'F600BC2D8F'
b6 = '9C005AC2F8F0'
b7 = '9C0141080250320F1802104A08'

# real input
with open('16_input.txt', encoding = 'utf-8-sig') as txt:
    txt = txt.readlines()
    txt = txt[0][:-1]

input_txt = b7

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

def get_payload(rest, lenght, no_packets):
    print('rest 1', rest)
    payload = []
    chunks = [rest[x * 5:(x + 1) * 5] for x in range((len(rest) + 5 - 1) // 5 )]

    if lenght != None:
        print('lenght')
        rest = rest[:lenght]   # omezeni je v delce - zbytek jsou rovnou unused chunks = nejsou soucasti tohoto paketu. ? Pokud jsou taky id4, patri nadrazenemu paketu?
        unused_chunks = rest[lenght:]
        chunks = [rest[x * 5:(x + 1) * 5] for x in range((len(rest) + 5 - 1) // 5 )]
        print('chunks ', chunks)
        for chunk in chunks:
            payload.append(chunk[1:])
            print(payload, unused_chunks)
            return payload, unused_chunks
    if no_packets != None:
        print('no packets')
        chunks = [rest[x * 5:(x + 1) * 5] for x in range((len(rest) + 5 - 1) // 5 )]
        print('chunks ', chunks)
        for ind, chunk in enumerate(chunks[:no_packets]):  # omezeni je v poctu paketu
            if chunk[0] == '1':
                payload.append(chunk[1:])
            else:
                payload.append(chunk[1:])
                if ind == len(chunks)-1:
                    unused_chunks = None
                else:
                    unused_chunks = ''.join(chunks[(ind+1):])
                print(payload, unused_chunks)
                return payload, unused_chunks
    else:
        print('literal value ', chunks)
        print('chunks ', chunks)
        for ind, chunk in enumerate(chunks):   # bez omezeni delky a poctu paketu
            if chunk[0] == '1':
                payload.append(chunk[1:])
            else:
                payload.append(chunk[1:])
                if ind == len(chunks)-1:
                    unused_chunks = None
                else:
                    unused_chunks = ''.join(chunks[(ind+1):])
                print(payload, unused_chunks)
                return payload, unused_chunks


def parse_operators(rest):
    zero_one = rest[0]
    if zero_one == '0':
        lenght = int(rest[1:16], 2)
        no_packets = None
        rest = rest[16:]
    else:
        no_packets = int(rest[1:12], 2)
        rest = rest[12:]
        lenght = None
    print('rest - lenght - no packets ', rest, lenght, no_packets)
    return rest, lenght, no_packets

"""
# a  # lze prepsat na get version a nezalamovat se s payloady
def (binary_txt):
    versions = []
    payloads = []
    while is_zeros(binary_txt) == False:
        version, id_number, rest_of_packet = get_version_id_rest(binary_txt)
        print(id_number)
        versions.append(version)
        if id_number == 4:
            a, unused_chunks = get_payload(rest_of_packet)
            payloads.append(a)
            print(a)
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
"""

def do_id_maths(literal_payload, id_n):
    assert id_n < 8
    print('literal payload a idn ', literal_payload, id_n)
    if id_n == 0:
        return sum(literal_payload)
    if id_n == 1:
        result = 0
        for i in literal_payload:
            for ii in literal_payload:
                result += i*ii
        return result
    if id_n == 2:
        return min(literal_payload)
    if id_n == 3:
        return max(literal_payload)
    if id_n == 5:
        assert len(literal_payload) == 2
        if literal_payload[0] > literal_payload[1]:
            return 1
        else:
            return 0
    if id_n == 6:
        assert len(literal_payload) == 2
        if literal_payload[0] < literal_payload[1]:
            return 1
        else:
            return 0
    if id_n == 7:
        assert len(literal_payload) == 2
        if literal_payload[0] == literal_payload[1]:
            return 1
        else:
            return 0

tree = []

class Tree_node:
    def __init__(self, id_number, children, payload):
        self.id_number = id_number
        self.parent = None
        self.children = []
        self.payload = payload
        self.children_payloads = []
        print("initializing node...", id_number)

    def add_child(self, child_node):
        print("Adding ", child_node.id_number, 'to', self.id_number)
        self.children.append(child_node)
        # self.children_payloads.append(child_node.payload)
        child_node.parent = self

    def traverse(self):
        print("Traversing...")
        nodes_to_visit = [self]
        while len(nodes_to_visit) > 0:
          current_node = nodes_to_visit.pop()
          print(current_node.value)
          nodes_to_visit += current_node.children


root = Tree_node('root', [], None)


# b
def f(binary_txt):
    current_parent = root
    payloads = []
    while is_zeros(binary_txt) == False:
        version, id_number, rest_of_packet = get_version_id_rest(binary_txt)
        print(version, id_number, rest_of_packet)
        if id_number == 4:
            a, unused_chunks = get_payload(rest_of_packet, lenght = None, no_packets = None)
            a = ''.join(a)
            a = int(a, 2)
            payloads.append(a)
            current_tree_node = Tree_node(id_number, None, a)
            current_parent.add_child(current_tree_node)
            print('a', a)
            if is_zeros(unused_chunks) == False:
                binary_txt = unused_chunks
            else:
                # payloads = [''.join(x) for x in payloads]
                # payloads = [int(x, 2) for x in payloads]
                return payloads, current_tree_node
            print('---')
        else:
            current_tree_node = Tree_node(id_number, None, None)
            current_parent.add_child(current_tree_node)
            current_parent = current_tree_node
            rest, lenght, no_packets = parse_operators(rest_of_packet)
            binary_txt = rest
            print('-------------')

    return payloads, current_tree_node

f(input_binary)    # dodat print


def traverse(node):
    current_node = node
    print('node ', id(node), node.payload)
    while node.payload == None:
        print('current_node id, payload, childrens payload', id(current_node), current_node.id_number, current_node.payload, current_node.children_payloads)
        if current_node.children_payloads != []:
            current_node.payload = do_id_maths(current_node.children_payloads, current_node.id_number)
            current_node = current_node.parent
        else:    # zkusit sem poslat Pracovni?
            for child in current_node.children:
                print('id current node: ', id(current_node), 'a id child: ', id(child), child.id_number)
                if child.payload != None:
                    current_node.children_payloads.append(child.payload)    # nejprve vsechny payloady shromazdit
            for child in current_node.children:
                if child.payload == None:
                    current_node = child   # ... a teprve pak se vyadat o uroven niz

    return node.payload

def traverse1(node):
    current_node = node
    while True:
        if current_node.payload != []:
            return current_node.payload
        else:
            print('current_node id, payload, childrens payload', id(current_node), current_node.id_number, current_node.payload, current_node.children_payloads)
            if current_node.children_payloads != []:
                current_node.paylad = do_id_maths(current_node.children_payloads, current_node.id_number)
            else:
                for child in current_node.children:
                    print('ch ', child.id_number)
                    if child.payload != []:
                        current_node.children_payloads.append(child.payload)
                    else:
                        current_node = child
    return node.payload


for ch in root.children:
    print('traverse... ', traverse(ch))






