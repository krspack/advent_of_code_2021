import random

"""
prekopat:
dostat se k payloadum, jako vedlejsi produkt funkce dat pocet vyuzitych bitu
pak diky tomu budu umet vyhodnotit, jestli parent node ma prostor pro dany paket
postupovta krok po kroku

"""


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
b7 = '9C0141080250320F1802104A08'   # toci se donekonecna

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

def parse_head(bin_txt):
    version = bin_txt[:3]
    version = int(version, 2)
    version = random.randint(0, 100)    # smazat
    id_number = bin_txt[3:6]
    id_number = int(id_number, 2)
    id_index_end = 5
    after_head = bin_txt[(id_index_end + 1):]
    return version, id_number, after_head

def get_payload(rest):
    # print('rest 1', rest)
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
            payload = ''.join(payload)
            packet_length = len(payload) + 1 + 6 # head length
            payload = int(payload, 2)
            return payload, unused_chunks, packet_length


def skip_operators(rest):
    zero_one = rest[0]
    if zero_one == '0':
        rest = rest[16:]
    else:
        rest = rest[12:]
    return rest


def do_id_maths(literal_payload, id_n):
    assert id_n < 8
    # print('literal payload a idn ', literal_payload, id_n)
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

class Tree_node:
    def __init__(self, version, id_number, after_head):
        self.version = version
        self.id_number = id_number
        self.after_head = after_head
        self.children = []
        self.parent = None
        self.packet_length = 0
        if self.id_number == 4:
            self.has_space = False
            self.limit_length = 0
            self.limit_no_packets = 0
        else:
            self.has_space = True
            self.limit_length = 10000
            self.limit_no_packets = 10000



    def add_child(self, child_node):
        assert self.has_space == True
        print("Adding ", child_node.version, 'to', self.version)
        self.children.append(child_node)
        self.limit_length -= child_node.packet_length
        self.limit_no_packets -= 1
        child_node.parent = self

    def apply_limit(self, child):
        if self.limit_no_packets <= 0:
            self.has_space = False
        if self.limit_length < child.packet_length:
            self.has_space = False
        print(self.version, 'has space? ', self.has_space, self.limit_length, self.limit_no_packets)

    def add_to_newly_found_parent(self, current_parent):
        assert (current_parent.id_number != 4 and current_parent.has_space == False)
        while current_parent.parent != root:
            print('current_parent.version ', current_parent.version)
            current_parent.parent.apply_limit(self)
            if current_parent.parent.has_space == True:
                current_parent = current_parent.parent
                current_parent.add_child(self)
        print("Adding ", self.version, 'to', current_parent.version)

    def add_to_tree(self, current_parent):
        current_parent.apply_limit(self)
        if current_parent.has_space == True:
            current_parent.add_child(self)
        else:
            print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
            self.add_to_newly_found_parent(current_parent)

    def parse_operators(self):
        assert self.id_number != 4
        if self.after_head[0] == '0':
            self.limit_length = int(self.after_head[1:16], 2)
            self.limit_no_packets = 10000
            rest = self.after_head[16:]
        else:
            self.limit_no_packets = int(self.after_head[1:12], 2)
            self.limit_length = 10000
            rest = self.after_head[12:]
        return rest

    def get_packet_length(self):
        current_packet = self
        l = []
        while is_zeros(current_packet.after_head) != True:
            while current_packet.id_number != 4:     # do l pridej delku obalky a opakuj kolecko se retezcem zmensenym o obalku
                res = current_packet.parse_operators()
                if current_packet.after_head[0] == '0':
                    l.append(15 + 1 + 6)
                else:
                    l.append(11 + 1 + 6)
                v, id_nu, after_head = parse_head(res)
                current_packet = Tree_node(v, id_nu, after_head)  # protoze vstup musi byt ve formatu tree_node

            p, u, packet_length = get_payload(after_head)
            l.append(packet_length)
            self.packet_length = sum(l)
            if is_zeros(u) == False:
                v, id_nu, after_head = parse_head(u)
                current_packet = Tree_node(v, id_nu, after_head)
            else:
                # print('l', l, sum(l), self.packet_length)
                return self.packet_length





root = Tree_node('root', 'root', 'root')



# b

def f(binary_txt, current_parent):
    while True:
        print('current parent ', current_parent.version)
        version, id_number, after_head = parse_head(binary_txt)
        current_node = Tree_node(version, id_number, after_head)
        if current_node.id_number == 4:
            current_node.payload, current_node.rest, current_node.packet_length = get_payload(after_head)
            print('payload ', current_node.payload, 'length of packet: ', current_node.packet_length, 'zbyva bitu: ', len(current_node.rest))  # rovnou ve funkci to prekodovat
            # print('current node rest ', current_node.rest)
            current_node.add_to_tree(current_parent)

            if is_zeros(current_node.rest) == False:
                binary_txt = current_node.rest
            else:
                binary_txt = current_node.rest
                print('zerossssssssss: ', binary_txt)
                return
        else:
            rest = current_node.parse_operators()
            print('current node ', current_node.version, 'limit_len ', current_node.limit_length, 'no_packets', current_node.limit_no_packets, 'delka rest: ', len(rest))
            if current_node.limit_length < 5000:
                current_node.packet_length = current_node.limit_length + (6 + 1 + 15)
            else:
                # current_node.packet_length  = current_node.get_packet_length()    # toto je nove, proverit
                current_node.packet_length = 6 + 1 + 11
                print(current_node.packet_length)
            current_node.add_to_tree(current_parent)
            current_parent = current_node
            binary_txt = rest
    print('zerossssssssss: ', binary_txt)
    return
print(f(input_binary, root))


"""
def f(binary_txt):
    current_parent = root
    while is_zeros(binary_txt) == False:
        current_parent.apply_limit(current_tree_node)
        version, id_number, rest_of_packet = get_version_id_rest(binary_txt)
        if id_number == 4:
            a, unused_chunks, len_used_chunks = get_payload(rest_of_packet)
            a = ''.join(a)
            a = int(a, 2)
            print('a', a)
            current_tree_node = Tree_node(id_number, None, a, rest_of_packet, len_used_chunks)
            if is_zeros(unused_chunks) == False:
                binary_txt = unused_chunks
            else:
                for ch in root.children:
                    return ch.payload
        else:
            rest, length, no_packets = parse_operators(rest_of_packet)
            current_tree_node = Tree_node(id_number, None, None, rest, rest_of_packet)
            current_tree_node.limit_length = length
            current_tree_node.limit_no_packets = no_packets
            print('--')
            print(current_tree_node.rest)
            current_parent.apply_limit(current_tree_node)
            if current_parent.has_space != True:
                grandparent = current_parent.parent
                current_parent = grandparent
            else:
                current_parent.add_child(current_tree_node)
            current_parent = current_tree_node
            binary_txt = rest
            print('-------------')

    for ch in root.children:
        return ch.payload

print(f(input_binary))



"""
def traverse(node):
    current_node = node
    print('node ', id(node), node.payload)
    while node.payload == None:
        print('current_node id, payload, childrens payload', id(current_node), current_node.id_number, current_node.payload, current_node.children_payloads)
        if current_node.children_payloads != []:
            current_node.payload = do_id_maths(current_node.children_payloads, current_node.id_number)
            current_node = current_node.parent
        else:
            for child in current_node.children:
                print('id current node: ', id(current_node), 'a id child: ', id(child), child.id_number)
                if child.payload != None:
                    current_node.children_payloads.append(child.payload)    # nejprve vsechny payloady shromazdit
            for child in current_node.children:
                if child.payload == None:
                    current_node = child   # ... a teprve pak se vyadat o uroven niz

    return node.payload









