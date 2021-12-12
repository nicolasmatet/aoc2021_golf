from collections import defaultdict


def lines():
    for l in open("input.txt"):
        yield tuple(l.strip().split('-'))


class Network:
    def __init__(self):
        self.nodes = dict()
        self.edges = defaultdict(set)

    def add_node(self, node_id, properties):
        self.nodes[node_id] = properties

    def add_edge(self, source, target):
        self.edges[source].add(target)
        self.edges[target].add(source)

    def has_node(self, node_id):
        return node_id in self.nodes

    def get_neighbors(self, node_id):
        return self.edges[node_id]

    def get_property(self, node_id, name):
        return self.nodes[node_id].get(name, None)


class Path:
    def __init__(self, start, end):
        self.start = start
        self.last_visited = start
        self.end = end
        self.visited = set()

    def branch(self, from_node):
        new_path = Path(from_node, self.end)
        new_path.start = self.start
        new_path.visited.update(self.visited)
        return new_path


class PathTwice(Path):
    def __init__(self, start, end):
        super().__init__(start, end)
        self.visited_twice = None

    def branch(self, from_node):
        new_path = PathTwice(from_node, self.end)
        new_path.start = self.start
        new_path.visited.update(self.visited)
        new_path.visited_twice = self.visited_twice
        return new_path


def get_network():
    global network
    network = Network()

    for source, target in lines():
        if not network.has_node(source):
            network.add_node(source, {'is_small': source.islower()})
        if not network.has_node(target):
            network.add_node(target, {'is_small': target.islower()})
        network.add_edge(source, target)
    return network


def count_path_no_return(network: Network, path: Path):
    if path.last_visited == path.end:
        return 1
    path_count = 0
    neighs = network.get_neighbors(path.last_visited)
    for neigh in neighs:
        if neigh not in path.visited:
            new_path = path.branch(neigh)
            if network.get_property(neigh, 'is_small'):
                new_path.visited.add(neigh)
            path_count += count_path_no_return(network, new_path)
    return path_count


def count_path_return(network: Network, path: PathTwice):
    path_count = 0
    if path.last_visited == path.end:
        return 1
    if path.visited_twice:
        return count_path_no_return(network, path)
    neighs = network.get_neighbors(path.last_visited)
    for neigh in neighs:
        if neigh == path.start:
            continue
        new_path = path.branch(neigh)
        if neigh in new_path.visited:
            new_path.visited_twice = neigh
        if network.get_property(neigh, 'is_small'):
            new_path.visited.add(neigh)
        path_count += count_path_return(network, new_path)
    return path_count


def solve1():
    network = get_network()
    path = Path('start', 'end')
    path.visited.add('start')
    return count_path_no_return(network, path)


def solve2():
    network = get_network()
    path = PathTwice('start', 'end')
    path.visited.add('start')
    return count_path_return(network, path)


count1 = solve1()
count2 = solve2()
print(count1)
print(count2)
assert count1 == 3410
assert count2 == 98796
