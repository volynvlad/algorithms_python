import numpy as np


class GraphAdjMatrix:
    def __init__(self, matrix, size=0):
        self.size = size
        self.matrix = np.zeros((self.size, self.size),
                               dtype=({
                                   'names': ['is_inc', 'weight'],
                                   'formats': [int, float]}))

        for i in range(self.size):
            for j in range(self.size):
                if i == j:
                    self.matrix[i][j]['weight'] = np.inf
                    self.matrix[i][j]['is_inc'] = 0
                else:
                    if matrix[i][j] == np.inf or matrix[i][j] == -np.inf:
                        self.matrix[i][j]['weight'] = matrix[i][j]
                        self.matrix[i][j]['is_inc'] = 0
                    else:
                        self.matrix[i][j]['weight'] = matrix[i][j]
                        self.matrix[i][j]['is_inc'] = 1

    def __setitem__(self, position, weight=1):
        if self.matrix[position[0]][position[1]]['is_inc'] == 0:
            self.matrix[position[0]][position[1]]['is_inc'] = 1
        self.matrix[position[0]][position[1]]['weight'] = weight

    def __getitem__(self, position):
        return self.matrix[position[0]][position[1]]

    def __str__(self):
        string = ""
        for i in range(self.size):
            for j in range(self.size):
                string += "{} ".format(str(self.matrix[i][j]))
            string += "\n"
        return string

    def add_edge(self, edge, weight):
        if edge[0] >= self.size or edge[1] >= self.size:
            return

        self.__setitem__((edge[0], edge[1]), weight)

    def is_adjacent(self, edge):

        if edge[0] >= self.size or edge[1] >= self.size:
            print("return")
            return

        return self.matrix[edge[0]][edge[1]]['is_inc'] == 1
