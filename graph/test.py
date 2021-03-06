import numpy as np

from graph.list_graph import GraphAdjList
from graph.matrix_graph import GraphAdjMatrix
from graph.node import Node

from graph.coloring import gis, dsatur


def test_get_set():
    matrix = [[np.inf, 1, np.inf],
              [1, np.inf, np.inf],
              [np.inf, np.inf, np.inf]]
    graph = GraphAdjMatrix(matrix=matrix, size=3)

    assert tuple(graph[0, 1]) == (1, 1), graph[0, 1]
    assert tuple(graph[1, 1]) == (0, np.inf), graph[0, 1]

    node_list = [Node('a'), Node('b'), Node('c')]

    graph = GraphAdjList(node_list)
    graph.add_edge((node_list[0], node_list[1]))
    graph.add_edge((node_list[1], node_list[0]))

    assert graph.nodes == node_list
    assert graph.nodes[0] == node_list[0]
    assert graph.nodes[1] == node_list[1]


def test_get_ordered_edges():
    number_nodes = 4
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]), 2)
    graph.add_double_edge((node_list[1], node_list[3]), 1)
    graph.add_double_edge((node_list[2], node_list[3]), 4)
    graph.add_double_edge((node_list[2], node_list[1]), 3)
    graph.add_double_edge((node_list[0], node_list[3]), -2)

    edges = graph.get_ordered_edges(graph.get_edges())

    for i in range(len(edges) - 1):
        assert edges[i][1] <= edges[i + 1][1]


def test_is_adjacent():
    matrix = [[np.inf, 1, np.inf],
              [1, np.inf, np.inf],
              [np.inf, np.inf, np.inf]]
    graph = GraphAdjMatrix(matrix=matrix, size=3)

    assert graph.is_adjacent((0, 1))

    node_list = [Node('a'), Node('b'), Node('c')]

    graph = GraphAdjList(node_list)

    graph.add_edge((node_list[0], node_list[1]))

    assert graph.is_adjacent((node_list[0], node_list[1]))
    assert not graph.is_adjacent((node_list[1], node_list[0]))


def test_add_edge():
    matrix = [[np.inf, 1, np.inf],
              [1, np.inf, np.inf],
              [np.inf, np.inf, np.inf]]
    graph = GraphAdjMatrix(matrix=matrix, size=3)

    graph.add_edge((1, 2), 3)
    graph.add_edge((2, 1), 3)

    assert graph.is_adjacent((1, 2))
    assert graph.is_adjacent((2, 1))

    node_list = [Node('a'), Node('b'), Node('c')]

    graph = GraphAdjList(node_list)
    graph.add_edge((node_list[1], node_list[2]))
    graph.add_edge((node_list[2], node_list[1]))
    graph.add_edge((node_list[0], node_list[2]))

    assert graph.is_adjacent((node_list[1], node_list[2]))
    assert graph.is_adjacent((node_list[2], node_list[1]))
    assert graph.is_adjacent((node_list[0], node_list[2]))
    assert not graph.is_adjacent((node_list[2], node_list[0]))


def test_remove_edge():
    matrix = [[np.inf, 1, np.inf],
              [1, np.inf, np.inf],
              [np.inf, np.inf, np.inf]]
    graph = GraphAdjMatrix(matrix=matrix, size=3)

    graph.add_edge((1, 2), 3)
    graph.add_edge((2, 1), 3)

    assert graph.is_adjacent((1, 2))
    assert graph.is_adjacent((2, 1))

    graph.remove_edge((1, 2))
    assert not graph.is_adjacent((1, 2))

    node_list = [Node('a'), Node('b'), Node('c')]

    graph = GraphAdjList(node_list)
    graph.add_edge((node_list[1], node_list[2]))
    graph.add_edge((node_list[2], node_list[1]))
    graph.add_edge((node_list[0], node_list[2]))

    assert graph.is_adjacent((node_list[1], node_list[2]))
    assert graph.is_adjacent((node_list[2], node_list[1]))
    assert graph.is_adjacent((node_list[0], node_list[2]))
    assert not graph.is_adjacent((node_list[2], node_list[0]))

    graph.remove_edge((node_list[0], node_list[2]))
    graph.remove_edge((node_list[1], node_list[2]))
    assert not graph.is_adjacent((node_list[0], node_list[2]))
    assert not graph.is_adjacent((node_list[1], node_list[2]))


def test_add_vertex():
    matrix = [[np.inf, 1, np.inf],
              [1, np.inf, np.inf],
              [np.inf, np.inf, np.inf]]
    graph = GraphAdjMatrix(matrix=matrix, size=3)

    graph.add_vertex()

    assert graph.size == 4
    assert graph.matrix['weight'][0][1] == 1
    assert graph.matrix['weight'][3][3] == np.inf

    assert graph.matrix['is_inc'][0][1] == 1
    assert graph.matrix['is_inc'][3][3] == 0

    node_list = [Node('a'), Node('b'), Node('c')]

    graph = GraphAdjList(node_list)
    graph.add_vertex()

    assert len(graph.nodes) == 4
    assert graph.nodes[-1].name == chr(ord('c') + 1)


def test_remove_vertex():
    matrix = [[np.inf, np.inf, 1],
              [np.inf, np.inf, np.inf],
              [1, np.inf, np.inf]]
    graph = GraphAdjMatrix(matrix=matrix, size=3)

    graph.remove_vertex(1)
    assert graph.size == 2
    assert tuple(graph[0, 1]) == (1, 1)
    assert tuple(graph[1, 0]) == (1, 1)

    node_list = [Node('a'), Node('b'), Node('c')]
    graph = GraphAdjList(node_list.copy())
    graph.add_edge((node_list[0], node_list[2]))
    graph.add_edge((node_list[1], node_list[2]))
    graph.add_edge((node_list[1], node_list[0]))

    assert graph.is_adjacent((node_list[1], node_list[2]))
    assert graph.is_adjacent((node_list[1], node_list[0]))
    graph.remove_vertex(node_list[1])

    assert graph.is_adjacent((node_list[0], node_list[2]))
    assert not graph.is_adjacent((node_list[1], node_list[0]))
    assert not graph.is_adjacent((node_list[1], node_list[2]))


def test_neighbors():
    matrix = [[np.inf, 2, 1],
              [np.inf, np.inf, 3],
              [1, 3, np.inf]]
    graph = GraphAdjMatrix(matrix=matrix, size=3)

    assert graph.get_neighbors(1) == [2]
    assert graph.get_neighbors(2) == [0, 1]

    node_list = [Node('a'), Node('b'), Node('c')]
    graph = GraphAdjList(node_list.copy())
    graph.add_edge((node_list[0], node_list[2]))
    graph.add_edge((node_list[1], node_list[2]))
    graph.add_edge((node_list[1], node_list[0]))

    for node_neighbor in node_list[0].get_neighbors():
        assert node_neighbor[0] in [node_list[2]]
    for node_neighbor in node_list[1].get_neighbors():
        assert node_neighbor[0] in [node_list[2], node_list[0]]


def test_euler_cycle():
    number_nodes = 6
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    correct_answer = ['a', 'b', 'c', 'd', 'f', 'c', 'e', 'a', 'd', 'e', 'f', 'a']

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[0], node_list[3]))
    graph.add_double_edge((node_list[0], node_list[4]))
    graph.add_double_edge((node_list[0], node_list[5]))

    graph.add_double_edge((node_list[4], node_list[2]))
    graph.add_double_edge((node_list[4], node_list[3]))
    graph.add_double_edge((node_list[4], node_list[5]))

    graph.add_double_edge((node_list[2], node_list[1]))
    graph.add_double_edge((node_list[2], node_list[3]))
    graph.add_double_edge((node_list[2], node_list[5]))

    graph.add_double_edge((node_list[5], node_list[3]))

    path = graph.euler_cycle()

    for node, correct_answer in zip(path, correct_answer):
        assert node.name == correct_answer

    graph.remove_edge((node_list[0], node_list[1]))
    graph.remove_edge((node_list[1], node_list[0]))

    assert graph.euler_cycle() == []


def test_width_bypass():
    number_nodes = 9
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[1], node_list[2]))
    graph.add_double_edge((node_list[0], node_list[2]))
    graph.add_double_edge((node_list[2], node_list[3]))
    graph.add_double_edge((node_list[2], node_list[4]))
    graph.add_double_edge((node_list[5], node_list[6]))
    graph.add_double_edge((node_list[7], node_list[8]))

    graph.width_bypass()

    print()
    print(graph)

    assert node_list[0].get_mark() == 0
    assert node_list[1].get_mark() == 1
    assert node_list[2].get_mark() == 1
    assert node_list[3].get_mark() == 2
    assert node_list[4].get_mark() == 2
    assert node_list[5].get_mark() == 0
    assert node_list[6].get_mark() == 1
    assert node_list[7].get_mark() == 0
    assert node_list[8].get_mark() == 1


def test_number_of_connected_components():
    number_nodes = 8
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[1], node_list[2]))
    graph.add_double_edge((node_list[0], node_list[2]))
    graph.add_double_edge((node_list[2], node_list[3]))
    graph.add_double_edge((node_list[2], node_list[4]))
    graph.add_double_edge((node_list[5], node_list[6]))

    assert graph.number_of_connected_components() == 3

    graph.width_bypass()
    graph.add_double_edge((node_list[2], node_list[5]))

    assert graph.number_of_connected_components() == 2


def test_is_connected():
    number_nodes = 8
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[1], node_list[2]))
    graph.add_double_edge((node_list[0], node_list[2]))
    graph.add_double_edge((node_list[2], node_list[3]))
    graph.add_double_edge((node_list[2], node_list[4]))
    graph.add_double_edge((node_list[5], node_list[6]))

    graph.width_bypass()

    assert not graph.is_connected()

    graph.add_double_edge((node_list[2], node_list[5]))
    graph.add_double_edge((node_list[5], node_list[7]))

    graph.width_bypass()

    assert graph.is_connected()


def test_is_bipartite():
    number_nodes = 8
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[1], node_list[2]))
    graph.add_double_edge((node_list[0], node_list[2]))
    graph.add_double_edge((node_list[2], node_list[3]))
    graph.add_double_edge((node_list[2], node_list[4]))
    graph.add_double_edge((node_list[5], node_list[6]))
    graph.add_double_edge((node_list[2], node_list[5]))
    graph.add_double_edge((node_list[5], node_list[7]))

    is_bipartite, *args = graph.is_bipartite()

    assert not is_bipartite

    graph.remove_double_edge((node_list[0], node_list[1]))

    is_bipartite, *args = graph.is_bipartite()

    assert is_bipartite

    graph.add_double_edge((node_list[4], node_list[6]))

    is_bipartite, *args = graph.is_bipartite()

    assert is_bipartite


def test_has_cycle():
    number_nodes = 6
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[1], node_list[2]))
    graph.add_double_edge((node_list[0], node_list[2]))

    assert graph.has_cycle()

    graph.remove_double_edge((node_list[0], node_list[1]))

    assert not graph.has_cycle()

    graph.add_double_edge((node_list[3], node_list[1]))
    graph.add_double_edge((node_list[3], node_list[4]))
    graph.add_double_edge((node_list[4], node_list[0]))

    assert graph.has_cycle()

    graph.remove_double_edge((node_list[3], node_list[1]))

    assert not graph.has_cycle()

    graph.add_double_edge((node_list[2], node_list[4]))

    assert graph.has_cycle()


def test_kruskal():

    number_nodes = 5
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]), 2)
    graph.add_double_edge((node_list[0], node_list[3]), 3)
    graph.add_double_edge((node_list[1], node_list[2]), 4)
    graph.add_double_edge((node_list[1], node_list[3]), 4)
    graph.add_double_edge((node_list[1], node_list[4]), 1)
    graph.add_double_edge((node_list[3], node_list[4]), 2)

    kruskal_graph = graph.kruskal()

    assert kruskal_graph.nodes[0].get_neighbors_names() == {'b'}
    assert kruskal_graph.nodes[1].get_neighbors_names() == {'e', 'a', 'c'}
    assert kruskal_graph.nodes[2].get_neighbors_names() == {'b'}
    assert kruskal_graph.nodes[3].get_neighbors_names() == {'e'}
    assert kruskal_graph.nodes[4].get_neighbors_names() == {'b', 'd'}


def test_prim():

    number_nodes = 5
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]), 2)
    graph.add_double_edge((node_list[0], node_list[3]), 3)
    graph.add_double_edge((node_list[1], node_list[2]), 4)
    graph.add_double_edge((node_list[1], node_list[3]), 4)
    graph.add_double_edge((node_list[1], node_list[4]), 1)
    graph.add_double_edge((node_list[3], node_list[4]), 2)

    prim_graph = graph.prim()

    assert prim_graph.nodes[0].get_neighbors_names() == {'b'}
    assert prim_graph.nodes[1].get_neighbors_names() == {'e', 'a', 'c'}
    assert prim_graph.nodes[2].get_neighbors_names() == {'b'}
    assert prim_graph.nodes[3].get_neighbors_names() == {'e'}
    assert prim_graph.nodes[4].get_neighbors_names() == {'b', 'd'}


def test_dijkstra():

    number_nodes = 7
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]), 2)
    graph.add_double_edge((node_list[0], node_list[2]), 4)
    graph.add_double_edge((node_list[0], node_list[3]), 5)
    graph.add_double_edge((node_list[1], node_list[2]), 1)
    graph.add_double_edge((node_list[1], node_list[4]), 8)
    graph.add_double_edge((node_list[2], node_list[4]), 3)
    graph.add_double_edge((node_list[2], node_list[3]), 3)
    graph.add_double_edge((node_list[3], node_list[5]), 2)
    graph.add_double_edge((node_list[4], node_list[5]), 2)
    graph.add_double_edge((node_list[4], node_list[6]), 3)
    graph.add_double_edge((node_list[5], node_list[6]), 1)

    graph.dijkstra(node_list[0])

    assert graph.nodes[0].get_mark() is None
    assert graph.nodes[0].get_marker() is None
    assert graph.nodes[1].get_mark() == 2
    assert graph.nodes[1].get_marker().name == 'a'
    assert graph.nodes[2].get_mark() == 3
    assert graph.nodes[2].get_marker().name == 'b'
    assert graph.nodes[3].get_mark() == 5
    assert graph.nodes[3].get_marker().name == 'a'
    assert graph.nodes[4].get_mark() == 6
    assert graph.nodes[4].get_marker().name == 'c'
    assert graph.nodes[5].get_mark() == 7
    assert graph.nodes[5].get_marker().name == 'd'
    assert graph.nodes[6].get_mark() == 8
    assert graph.nodes[6].get_marker().name == 'f'


def test_gale_shepley_matrix4x4():
    employees_ranks = [
        [1, 0, 2, 3],  # for 1st employee preferences of tasks
        [3, 1, 0, 2],
        [0, 2, 1, 3],
        [3, 2, 1, 0]]
    tasks_ranks = [
        [2, 0, 1, 3],
        [0, 3, 2, 1],
        [1, 0, 2, 3],
        [0, 2, 3, 1]]

    result1, sum_emp_tasks1, sum_tasts_emp1 = GraphAdjMatrix.gale_shapley(employees_ranks, tasks_ranks)
    result2, sum_tasts_emp2, sum_emp_tasks2 = GraphAdjMatrix.gale_shapley(tasks_ranks, employees_ranks)

    print()

    print("sum emp emp->tasks = {}, sum tasks emp->tasks = {}".format(sum_emp_tasks1, sum_tasts_emp1))
    print("sum emp tasks->emp = {}, sum tasks tasks->emp = {}".format(sum_emp_tasks2, sum_tasts_emp2))

    print(result1)
    print(result2)

    assert result1 == {0: [2], 1: [0], 2: [1], 3: [3]}
    assert result2 == {0: [1], 1: [2], 2: [0], 3: [3]}


def test_gale_shepley_matrix5x5():
    employees_ranks = [
        [1, 0, 3, 4, 2],  # for 1st employee preferences of tasks
        [3, 1, 0, 2, 4],
        [0, 2, 1, 4, 3],
        [1, 2, 4, 0, 3],
        [1, 3, 0, 4, 2]]
    tasks_ranks = [
        [1, 2, 0, 4, 3],
        [0, 4, 3, 2, 1],
        [1, 4, 3, 2, 0],
        [0, 3, 1, 4, 2],
        [0, 2, 4, 3, 1]]

    result1, sum_emp_tasks1, sum_tasts_emp1 = GraphAdjMatrix.gale_shapley(employees_ranks, tasks_ranks)
    result2, sum_tasts_emp2, sum_emp_tasks2 = GraphAdjMatrix.gale_shapley(tasks_ranks, employees_ranks)

    print()

    print("sum emp emp->tasks = {}, sum tasks emp->tasks = {}".format(sum_emp_tasks1, sum_tasts_emp1))
    print("sum emp tasks->emp = {}, sum tasks tasks->emp = {}".format(sum_emp_tasks2, sum_tasts_emp2))

    print(result1)
    print(result2)

    assert result1 == {0: [2], 1: [0], 2: [3], 3: [1], 4: [4]}
    assert result2 == {0: [1], 1: [0], 2: [4], 3: [3], 4: [2]}


def test_floid():
    matrix = [[np.inf, 2, 1, -2, np.inf],
              [1, 3, 2, -1, 1],
              [np.inf, 1, np.inf, np.inf, np.inf],
              [np.inf, np.inf, np.inf, np.inf, 3],
              [np.inf, 1, 10, np.inf, np.inf]]
    graph = GraphAdjMatrix(matrix=matrix, size=5)

    print()
    print(graph)

    graph.floid()

    inquiry_matrix = graph._inquiry

    print(graph)

    for row in inquiry_matrix:
        print(row)


def test_place_station():
    matrix = [[np.inf, 2, 1, 2, np.inf],
              [1, 3, 2, 1, 1],
              [np.inf, 1, np.inf, np.inf, np.inf],
              [np.inf, np.inf, np.inf, np.inf, 3],
              [np.inf, 1, 10, np.inf, np.inf]]
    graph = GraphAdjMatrix(matrix=matrix, size=5)

    print()

    assert graph.place_station() == 1


def test_depth_first_search():
    number_nodes = 7
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_edge((node_list[0], node_list[1]))
    graph.add_edge((node_list[0], node_list[2]))
    graph.add_edge((node_list[1], node_list[3]))
    graph.add_edge((node_list[1], node_list[4]))
    graph.add_edge((node_list[2], node_list[5]))
    graph.add_edge((node_list[4], node_list[6]))

    graph.depth_first_search()

    print()
    print(graph)

    assert graph.nodes[0].get_mark() == 0
    assert graph.nodes[1].get_mark() == 1
    assert graph.nodes[3].get_mark() == 2
    assert graph.nodes[2].get_mark() == 3
    assert graph.nodes[5].get_mark() == 4
    assert graph.nodes[4].get_mark() == 5
    assert graph.nodes[6].get_mark() == 6


def test_hron_sequence():
    number_nodes = 4
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_edge((node_list[0], node_list[1]))
    graph.add_edge((node_list[0], node_list[2]))
    graph.add_edge((node_list[1], node_list[2]))
    graph.add_edge((node_list[3], node_list[1]))
    graph.add_edge((node_list[3], node_list[2]))

    order = graph.hron_sequence()

    print()
    print(graph)

    for i, node in enumerate(order):
        print("{}: {}".format(len(order) - 1 - i, node))


def test_gis():
    number_nodes = 5
    node_list = [Node() for _ in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[1], node_list[2]))
    graph.add_double_edge((node_list[1], node_list[3]))
    graph.add_double_edge((node_list[3], node_list[4]))
    graph.add_double_edge((node_list[0], node_list[4]))

    related_colors = gis(graph)

    assert related_colors == {0: 1, 1: 2, 2: 1, 3: 1, 4: 2}

    number_nodes = 10
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[1], node_list[2]))
    graph.add_double_edge((node_list[2], node_list[3]))
    graph.add_double_edge((node_list[3], node_list[4]))
    graph.add_double_edge((node_list[4], node_list[0]))

    graph.add_double_edge((node_list[5], node_list[7]))
    graph.add_double_edge((node_list[7], node_list[9]))
    graph.add_double_edge((node_list[9], node_list[6]))
    graph.add_double_edge((node_list[6], node_list[8]))
    graph.add_double_edge((node_list[8], node_list[5]))

    graph.add_double_edge((node_list[0], node_list[5]))
    graph.add_double_edge((node_list[1], node_list[6]))
    graph.add_double_edge((node_list[2], node_list[7]))
    graph.add_double_edge((node_list[3], node_list[8]))
    graph.add_double_edge((node_list[4], node_list[9]))

    related_colors = gis(graph)

    assert related_colors == {0: 1, 1: 2, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 3, 8: 3, 9: 2}


def test_dsatur():
    number_nodes = 5
    node_list = [Node() for _ in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[1], node_list[2]))
    graph.add_double_edge((node_list[1], node_list[3]))
    graph.add_double_edge((node_list[3], node_list[4]))
    graph.add_double_edge((node_list[0], node_list[4]))

    related_colors = dsatur(graph)

    assert related_colors == {0: 1, 1: 0, 2: 1, 3: 1, 4: 0}

    number_nodes = 10
    node_list = [Node(chr(ord('a') + i)) for i in range(number_nodes)]

    graph = GraphAdjList(node_list.copy())

    graph.add_double_edge((node_list[0], node_list[1]))
    graph.add_double_edge((node_list[1], node_list[2]))
    graph.add_double_edge((node_list[2], node_list[3]))
    graph.add_double_edge((node_list[3], node_list[4]))
    graph.add_double_edge((node_list[4], node_list[0]))

    graph.add_double_edge((node_list[5], node_list[7]))
    graph.add_double_edge((node_list[7], node_list[9]))
    graph.add_double_edge((node_list[9], node_list[6]))
    graph.add_double_edge((node_list[6], node_list[8]))
    graph.add_double_edge((node_list[8], node_list[5]))

    graph.add_double_edge((node_list[0], node_list[5]))
    graph.add_double_edge((node_list[1], node_list[6]))
    graph.add_double_edge((node_list[2], node_list[7]))
    graph.add_double_edge((node_list[3], node_list[8]))
    graph.add_double_edge((node_list[4], node_list[9]))

    related_colors = dsatur(graph)

    assert related_colors == {0: 0, 1: 1, 2: 0, 3: 1, 4: 2, 5: 1, 6: 0, 7: 2, 8: 2, 9: 1}


