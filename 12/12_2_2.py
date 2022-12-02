
"""
snapshot neni route stejne jako queue neni route - ne vsechno, co je projito, se promitne do vysledne cesty, viz d.
projit prochazeni s pampirem a udelat stejnou zmenu jako u prochazeni do sirky
"""



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
        self.small = True
        self.adjacent = set()
        self.route = []
        self.follower = None
        self.in_queue = False
        self.parent = None

    def __repr__(self):
        # path_repr = [x.cave_value for x in self.path]
        return self.cave_value
        # return ' with path: '.join((self.cave_value, ', '.join(path_repr)))

    def set_follower(self, other_cave):
        self.follower = other_cave


class Edge:
    def __init__(self, beginning_finish):
        self.beginning_finish = beginning_finish
        self.beginning = beginning_finish[0]   # nepouzito?
        self.finish = beginning_finish[1]   # nepouzito?

    def __repr__(self):
        return ' '.join(self.beginning_finish)

""" smazat
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
        if cave.small:
            cave.in_queue = True    # ko, jak s timto naklada devitka -------------------
        self.size += 1

    def dequeue(self):
        self.head.in_queue = False
        if self.head.small == True:
            self.head.visited = True
        second_to_head = self.head.follower
        self.head = second_to_head
        self.size -= 1
"""

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
            cave.small = False


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

"""
# funkce urcena k tomu, aby nasla vsechny cesty do vsech bodu a ty se pak budou v dalsim kroku filtrovat - kam maji jit
# nenajde vsechno - asi kvuli podmince len(q) > 0
def browse(caves = all_caves, edges = all_edges):
    get_adjacent_caves()
    reset_sizes()

    all_routes = []

    queue = Queue()
    queue.enqueue(caves['start'])

    def queuing(current, q):
        current.route.append(current.cave_value)
        all_routes.append(current.route)
        if not current.is_big:
            current.visited = True
        q.dequeue()
        print('current ', current)
        for a in current.adjacent:
            print('adjacent ', a)
            if (a.visited == False and a.in_queue == False):
                q.enqueue(a)
                print(a, 'in queue')
                a.route = copy.copy(current.route)
        if q.size == 0:
            return all_routes
        else:
            queuing(queue.head, queue)
    queuing(caves['start'], queue)

    return all_routes
print(2, browse())

for cave in all_caves.values():
    print(cave, cave.route)

"""

"""
poladit:
- proc to nenaslo start-b-end? a start-a-b-end?
- skoncit prochazeni u endu
- nedava to ty nejdelsi vysledky - q asi neni dost dlouha?
- dava to vicero sad nekompletnich vysledku - bude nutne je bud shromazdovat (ale jak dlouho?) nebo:
... vyhodit set a nahradit ho listem

"""



# 2. filtruj vysledky:
# - pokud cesta konci v end, uloz ji do routes_to_end
# - pokud cesta konci

# ---
"""
# pokus: zde dobre zaveden parent

def browse(caves = all_caves, edges = all_edges):
    get_adjacent_caves()
    reset_sizes()

    all_routes = []

    queue = Queue()
    queue.enqueue(caves['start'])

    def queuing(current, q):
        current.route.append(current.cave_value)
        all_routes.append(current.route)
        if not current.is_big:
            current.visited = True
        q.dequeue()
        print('current ', current)
        for a in current.adjacent:
            print('adjacent ', a)
            a.parent = current
            if (a.visited == False and a.in_queue == False):
                q.enqueue(a)
                print(a, 'in queue')
                a.route = copy.copy(a.parent.route)
        if q.size == 0:
            return all_routes
        else:
            queuing(queue.head, queue)
    queuing(caves['start'], queue)

    return all_routes
print(2, browse())

for cave in all_caves.values():
    print(cave, cave.route)
"""

"""
# pokus 2: DFS, parent vyhozen
def browse(caves = all_caves, edges = all_edges):
    get_adjacent_caves()
    reset_sizes()

    all_routes = []

    def depth_first(current):
        current.route.append(current.cave_value)
        if current.small:
            current.visited = True
        for a in current.adjacent:
            if a.visited == True:
                continue
            else:
                print(1, 'adjacent ', a, a.visited)
                if a.cave_value == 'end':
                    print('end found')
                    a.route = copy.copy(current.route)
                    a.route.append(a.cave_value)
                    if a.route not in all_routes:  # posledni pridane
                        all_routes.append(a.route)
                        return 'return 2', all_routes
                    else:
                        continue
                else:
                    print(2, 'adjacent ', a, a.visited)
                    a.route = copy.copy(current.route)
                    print(depth_first(a))
    depth_first(caves['start'])

print(browse())
"""

# pokus n: depth_first a v nem stack namisto queue

class Stack:
  def __init__(self, top_cave = None):
    self.top_cave = top_cave

  def is_empty(self):
    if self.top_cave == None:
        return True
    else:
        return False

  def push(self, cave):
    if self.top_cave == None:
        self.top_cave = cave
    else:
        cave.set_follower(self.top_cave)
        self.top_cave = cave

  def pop(self):
    cave_to_remove = self.top_cave
    self.top_cave = cave_to_remove.follower

  def snapshot(self):  # a potomn all routes append snapshot
    if self.top_cave == None:
        return []
    else:
        current_cave = self.top_cave
        route = [current_cave]
        print(66, route)
        while current_cave.follower != None:
            route.append(current_cave.follower)
            print(666, route)
            current_cave = current_cave.follower
    return route

"""
browse:
pridavat items do stacku
jakmile se najde end (current je end), pak udelat snapshot stacku, a jestlize tam jeste neni, ulozit ho do all_routes
potom: odebirat ze stacku. Odebrat end = vratit se k posledni krizovatce a jit po ni jinou cestou a hledat end tamtudy. Jeslti to nevyjde,
vratit se zase o krizovatku dal atd.
"""


def browse(caves = all_caves, edges = all_edges):
    get_adjacent_caves()
    reset_sizes()
    s = Stack()
    all_routes = []

    def depth_first(current):
        s.push(current)
        if current.small == True:
            current.visited = True
        print('current ', current, current.visited)
        if current == caves['end']:  # alternativa
            return s.snapshot()
            # s.pop()  # tj se stacku se vyhodi end = udela se krok zpatky, current je predchozi uzel (proto se musi zmenit na unvisited), prochazi se sourozenci endu
            # s.top_cave.visited = False
        else:
            for a in current.adjacent:
                print('adjacent ', a)
                if a.visited == False:
                    depth_first(current = a)
        return s.snapshot()

    route = depth_first(caves['start'])
    print('one route ', route)
    all_routes.append(route)
    return all_routes

print(browse())



