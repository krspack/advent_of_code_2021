
import copy

with open('12_1test_input.txt', encoding = 'utf-8-sig') as txt:
    edges = txt.readlines()
    edges = [x.strip('\n') for x in edges]
    edges = [x.split('-') for x in edges]
    print(edges)


class Cave:
    def __init__(self, cave_value):
        self.cave_value = cave_value
        self.visited = False
        self.is_big = False
        self.adjacent = set()
        self.route = []
        self.follower = None
        self.in_queue = False

    def __repr__(self):
        # path_repr = [x.cave_value for x in self.path]
        return self.cave_value
        # return ' with path: '.join((self.cave_value, ', '.join(path_repr)))

    def get_adjacent_caves_not_in(self, visited_small):
        return [x for x in list(self.adjacent) if x not in visited_small]

    def set_follower(self, other_cave):
        self.follower = other_cave


class Edge:
    def __init__(self, beginning_finish):
        self.beginning_finish = beginning_finish
        self.beginning = beginning_finish[0]   # nepouzito?
        self.finish = beginning_finish[1]   # nepouzito?

    def __repr__(self):
        return ' '.join(self.beginning_finish)


class Queue:   # fifo queue with caves to be explored
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, cave):
        if self.size == 0:
            self.head = cave
            self.tail = cave
        else:
            self.tail.set_follower(cave)
            self.tail = cave
        cave.in_queue = True    # ko, jak s timto naklada devitka -------------------
        self.size += 1

    def dequeue(self):
        self.head.in_queue = False
        if self.head.is_big == False:
            self.head.visited = True
        second_to_head = self.head.follower
        self.head = second_to_head
        self.size -= 1

# instantiation
all_caves = [[x[0]] for x in edges] + [[x[1]] for x in edges]
all_caves = set([x for [x] in all_caves])
all_caves = {x: Cave(x) for x in list(all_caves)}
all_edges = {tuple(sorted(x)): Edge(x) for x in edges}

def get_adjacent_caves(edges = all_edges, caves = all_caves):
    for edge in edges.values():
        caves[edge.beginning].adjacent.add(caves[edge.finish])
        caves[edge.finish].adjacent.add(caves[edge.beginning])

def reset_sizes(caves = all_caves):
    for cave in caves.values():
        if cave.cave_value == cave.cave_value.upper():
            cave.is_big = True


def visit(cave, parent_cave, all_routes_list):
    cave.route = copy.copy(parent_cave.route)
    cave.route.append(cave)
    all_routes_list.append(cave.route)
    # cave.visited = True  # duplicitni
    return

"""
def browse(caves = all_caves, edges = all_edges):
    get_adjacent_caves()
    all_routes = []
    fifo = Queue()
    caves['start'].route = ['start']
    fifo.enqueue(caves['start'])
    # je potreba menit, co je current, nebo se currentu uplne zbavit
    while fifo.size > 0:
        for a in fifo.head.adjacent:
            print('fifo head ', fifo.head, 'adjacent ', a)
            if a.visited == False:
                print('navstivit')
                visit(a, fifo.head, all_routes)
                fifo.enqueue(a)
        fifo.dequeue()
        print('--')
    return all_routes
print(browse())
"""

def browse(caves = all_caves, edges = all_edges):
    get_adjacent_caves()
    reset_sizes()

    all_routes = []
    fifo = Queue()
    caves['start'].route = ['start']
    fifo.enqueue(caves['start'])
    # je potreba menit, co je current, nebo se currentu uplne zbavit
    while fifo.size > 0:
        for a in fifo.head.adjacent:
            print('fifo head ', fifo.head, 'adjacent ', a)
            if a.visited == False:
                print('navstivit')
                visit(a, fifo.head, all_routes)
                fifo.enqueue(a)
        fifo.dequeue()
        print(fifo.size)
        print('--')
    return all_routes
print(browse())

"""
poladit:
- skoncit prochazeni u endu
- nedava to ty nejdelsi vysledky - fifo asi neni dost dlouha?
- dava to vicero sad nekompletnich vysledku - bude nutne je bud shromazdovat (ale jak dlouho?) nebo:
... vyhodit set a nahradit ho listem

"""



# 2. filtruj vysledky:
# - pokud cesta konci v end, uloz ji do routes_to_end
# - pokud cesta konci







