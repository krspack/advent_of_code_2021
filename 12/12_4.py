import copy

"""
path se musi pri uprave kopirovat (a nasledne asi ukladat k aktualnimu uzlu..)
upravit funkci repr tak, aby tiskla i aktualni cestu k uzlu (self.path) a to pomuze k reseni

trable s omeyzenim for cyklu
sel by k tomu pouzit seznam visited small caves?
dokud v nem neni end, pokracovat v cyklovani - hledani cesty k end
jakmile je v nem end:
zapsat cestu


s kazdym sousedem se musi provest jednu z tohoto a pak jit dal:
- nenavstivit, protoze je maly a je v jeskyni visited_small_caves
- navstivit
- navstivit. Je to end > skoncit tam cestu. Je tato cesta mezi uz zapsanymi? Pak skoncit celou funkci. Neni tam jeste?
Zapsat ji tam.
Vynulovat visited_small_caves
Tento soused je tim vyrizeny. Je potreba jit na dalsiho - navazat na dosavadni zkoumani (nevracet se na start),
ale zaroven smazat probihajici path (za end uz nic nema byt) a naopak navazat na cestu tam, kde se rozvetvila. Tuto funkci by mela plnit current_path?
"""

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
        self.path = []

    def __repr__(self):
        path_repr = [x.cave_value for x in self.path]
        return ' with path: '.join((self.cave_value, ', '.join(path_repr)))

    def reset_size(self):
        if self.cave_value == self.cave_value.upper():
            self.is_big = True
        else:
            self.is_big = False


class Edge:
    def __init__(self, beginning_finish):
        self.beginning_finish = beginning_finish
        self.beginning = beginning_finish[0]   # nepouzito?
        self.finish = beginning_finish[1]   # nepouzito?

    def __repr__(self):
        return ' '.join(self.beginning_finish)

# instantiation
all_caves = [[x[0]] for x in edges] + [[x[1]] for x in edges]
all_caves = set([x for [x] in all_caves])
all_caves = {x: Cave(x) for x in list(all_caves)}
all_edges = {tuple(x): Edge(x) for x in edges}

#
def get_adjacent_caves(edges = all_edges, caves = all_caves):
    for edge in edges.values():
        caves[edge.beginning].adjacent.add(caves[edge.finish])
        caves[edge.finish].adjacent.add(caves[edge.beginning])
    # for c in caves.values():                # pryc
    # print(c, 'ma sousedy: ', c.adjacent)    # pryc


def browse(edges = all_edges, caves = all_caves):
    get_adjacent_caves()

    current_cave = caves['start']
    end_cave = caves['end']
    visited_small_caves = [current_cave]

    paths_to_end = []   # strada vsechny cesty ke konci, s kazdym projitim pribude jedna
    path = [current_cave]     # prave prochazena cesta. Pak existuji jeste self.path_to == cesta k necemu, k te se lze vratit ze slepe vetve.

    while True:
        current_cave.path = copy.deepcopy(path)    # current ma k sobe pripichnuty aktualni stav vetve. Jde se k tomu vratit z end.
        for adjacent in list(current_cave.adjacent):
            print('AAA current_cave ', current_cave, 'adjacent ', adjacent)
            print('list(current_cave.adjacent) ', list(current_cave.adjacent))
            print('pro kontrolu: vsechny current_cave.adjacent ', current_cave.adjacent)
            print('AAA current_cave ', current_cave, 'adjacent ', adjacent)
            if adjacent == end_cave:
                print('-- end --')
                # path.append(adjacent)
                end_cave.path = copy.deepcopy(path)   # je nutna copy?
                end_cave.path.append(end_cave)
                if end_cave.path not in paths_to_end:
                    paths_to_end.append(end_cave.path)
                    print('path ', path)
                    # vynulovat visited small caves?
                    # kam se vratit:
                    path = current_cave.path   # pote, co se ulozila cesta do konce, se vrati o krok zpet a prochazi se dal
                    print('path = current_cave.path , o krok zpet', path)
                    visited_small_caves.append(end_cave)  # ... a vynuluji se navstivene    ?????
                    # break # --------------------------------------
                else:
                    return paths_to_end
            else:
                adjacent.reset_size()
                if adjacent not in visited_small_caves:
                    print('ok')
                    current_cave.path = copy.deepcopy(path)
                    path.append(adjacent)
                    adjacent.path = copy.deepcopy(path)
                    if adjacent.is_big == False:
                        visited_small_caves.append(adjacent)
                        print('visited_small_caves.append', adjacent)
                    print('OLD current_cave ', current_cave)
                    current_cave = adjacent
                    print('NEW current_cave ', current_cave)
                    current_cave.path = copy.deepcopy(path)
                    print('current_cave.path ', current_cave.path)
                    print('---------------')
                else:
                    current_cave.adjacent.remove(adjacent)   # smaze se ze seznamu jeskyni, protoze pro ucely cest ke konci je k nicemu
                    print('VISITED SMALL CAVES ', visited_small_caves)
                    print('REMOVED ', adjacent, 'from ', current_cave, '. Now current has these adjacent caves left: ', current_cave.adjacent)
                    # XXXXXXXXXXXXXXXXXXXXX tady je asi nutne taky zmenit current = adjacent?" XXXXXXXXXXXXXXXXXXXXXXXXXXX
    return paths_to_end


print(browse())

"""
mají smysl jenom cesty od startu, od jiných jeskyní ne
s každým novým projitým sousedem:
naklonovat cesty, co do něj vedou a ke každé přidat jeho samého
"""





