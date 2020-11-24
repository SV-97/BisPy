import networkx as nx

initial_partitions = [
    [[0]],
    [[0], [1]],
    [[0], [1, 2]],
    [[0, 3], [1, 2]],
    [[0, 3, 4], [1, 2]],
    [[0, 3, 4], [1, 2], [5]],
    [[0, 3, 4], [1, 2], [5], [6]],
    [
        [0, 3, 4],
        [1, 2],
        [5],
        [6],
        [7],
    ],
    [
        [0, 3, 4],
        [1, 2],
        [5, 8],
        [6],
        [7],
    ],
    [
        [0, 3, 4],
        [1, 2, 9],
        [5, 8],
        [6],
        [7],
    ],
]


def create_graph(edges):
    top_node = max([max(edge[0], edge[1]) for edge in edges])
    nodes = [i for i in range(top_node + 1)]

    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    return graph


def create_graph_partition_tuple(graph):
    return (graph, initial_partitions[len(graph.nodes) - 1])


graph_partition_tuples = list(
    map(
        lambda edges: create_graph_partition_tuple(create_graph(edges)),
        [
            [
                (0, 6),
                (1, 2),
                (1, 4),
                (2, 7),
                (3, 7),
                (4, 2),
                (5, 2),
                (5, 8),
                (6, 1),
                (6, 4),
                (6, 8),
                (8, 1),
                (9, 2),
                (9, 4),
            ],
            [
                (0, 1),
                (0, 7),
                (0, 8),
                (3, 2),
                (4, 2),
                (4, 6),
                (7, 1),
                (7, 2),
                (8, 0),
                (8, 1),
                (8, 9),
                (9, 6),
            ],
            [
                (0, 2),
                (0, 3),
                (0, 5),
                (1, 3),
                (1, 4),
                (2, 6),
                (2, 9),
                (4, 9),
                (5, 8),
                (6, 7),
                (7, 9),
                (8, 3),
            ],
            [
                (0, 6),
                (1, 0),
                (1, 2),
                (1, 4),
                (2, 0),
                (2, 3),
                (3, 1),
                (4, 1),
                (4, 5),
                (6, 2),
                (9, 4),
                (9, 6),
            ],
            [(0, 2), (2, 0), (2, 3), (2, 4), (3, 0), (3, 1), (4, 0), (4, 2), (4, 3)],
            [(0, 3), (1, 3), (2, 1), (2, 3), (3, 0), (3, 4), (4, 0), (4, 2), (4, 3)],
            [(0, 1), (0, 2), (0, 3), (1, 2), (2, 4), (3, 0), (3, 2), (4, 1), (4, 3)],
            [
                (0, 2),
                (0, 3),
                (1, 2),
                (1, 3),
                (2, 0),
                (2, 1),
                (2, 3),
                (3, 2),
                (4, 0),
                (4, 1),
                (4, 2),
                (4, 3),
            ],
            [(0, 1), (0, 2), (1, 0), (2, 0), (2, 1)],
            [(0, 1), (0, 2), (1, 0), (1, 2)],
            [(0, 1), (1, 2), (2, 0), (2, 1)],
            [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)],
        ],
    )
)

graph_partition_rscp_tuples = [
    (
        create_graph(
            [
                (2, 0),
                (3, 1),
                (4, 3),
                (4, 2),
                (5, 0),
                (5, 3),
                (6, 3),
                (7, 4),
                (7, 5),
                (7, 6),
            ]
        ),
        [(7,), (6, 5, 4), (3, 2), (1, 0)],
        set([(7,), (0, 1), (2, 3), (4, 6), (5,)]),
    )
]
