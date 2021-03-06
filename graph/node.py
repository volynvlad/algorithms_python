class Node:
    def __init__(self, name: str = "", number=None, neighbors=None):  # multi (name, weight) in set
        if neighbors is None:
            neighbors = []
        self.name = name
        self.number = number
        self.neighbors = neighbors
        self.mark = None
        self.marker_node = None

    def __str__(self):
        string = "Node["
        string += "number = {}".format(self.number)
        if self.neighbors is None:
            string += ", neighbors = {}".format(self.neighbors)
        else:
            string += ", neighbors = "
            for neighbor in self.neighbors:
                string += "({} {})".format(neighbor[0].number, neighbor[1])

        string += ", mark = {}, marker = {}".format(self.mark,
                                                    self.marker_node.name if self.marker_node is not None else None)

        return string + "]"

    def __eq__(self, node):
        if self is None or node is None:
            return False
        if type(node) == type(tuple()):
            return self.name == node[0].name
        return self.name == node.name

    def get_neighbors(self):
        return self.neighbors

    def get_neighbors_names(self):
        return {node.name for node, _ in self.neighbors}

    def get_neighbor_by_name(self, name):
        for neighbor in self.neighbors:
            if neighbor[0].name == name:
                return neighbor[0]
        return None

    def get_neighbor_weight_by_name(self, name):
        for neighbor in self.neighbors:
            if neighbor[0].name == name:
                return neighbor[1]
        return None

    def degree(self):
        return len(self.get_neighbors())

    def set_mark(self, mark):
        self.mark = mark

    def get_mark(self):
        return self.mark

    def is_marked(self):
        return self.mark is not None

    def set_marker(self, marker_node):
        self.marker_node = marker_node

    def get_marker(self):
        return self.marker_node

    def is_all_neighbors_marked(self):
        for neighbor, _ in self.neighbors:
            if not neighbor.is_marked():
                return False
        return True

    def is_any_neighbors_marked(self):
        for neighbor, _ in self.neighbors:
            if neighbor.is_marked():
                return True
        return False
