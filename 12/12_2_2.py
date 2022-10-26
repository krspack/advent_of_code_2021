
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
        self.is_big = None
        self.adjacent = set()
        self.route = []
        self.follower = None
        self.in_queue = False

    def __repr__(self):
        # path_repr = [x.cave_value for x in self.path]
        return self.cave_value
        # return ' with path: '.join((self.cave_value, ', '.join(path_repr)))

    def reset_size(self):
        if self.cave_value == self.cave_value.upper():
            self.is_big = True
        else:
            self.is_big = False

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
        cave.in_queue = True
        self.size += 1

    def dequeue(self):
        self.head.in_queue = False
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


def visit(cave, parent_cave, all_routes_list):
    cave.route = copy.copy(parent_cave.route)
    cave.route.append(cave)
    all_routes_list.append(cave.route)
    return

def browse(caves = all_caves, edges = all_edges):
    get_adjacent_caves()
    current = caves['start']
    current.route = [caves['start']]
    all_routes = []
    fifo = Queue()
    fifo.enqueue(current)
    print('fifo head cave value ', fifo.head.cave_value)

    while fifo.size > 0:
        for a in fifo.head.adjacent:
            visit(a, current, all_routes)
            fifo.enqueue(a)
        fifo.dequeue()
        print(fifo.size)

    return all_routes
print(browse())

# 2. filtruj vysledky:
# - pokud cesta konci v end, uloz ji do routes_to_end
# - pokud cesta konci







