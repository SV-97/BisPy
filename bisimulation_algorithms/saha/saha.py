import networkx as nx
from bisimulation_algorithms.dovier_piazza_policriti.graph_entities import (
    _Vertex,
    _Block,
)
from typing import List, Tuple


def check_old_blocks_relation(
    old_rscp: List[List[_Block]],
    new_edge: Tuple[_Vertex],
) -> bool:
    """Calling the new edge u->v, if in the old RSCP [u] => [v], the addition
    of the new edge doesn't change the RSCP.

    Args:
        old_rscp (List[Tuple[int]]): The RSCP before the addition of the edge
            (each index of the outer-most list is linked to the rank of the
            blocks in the inner-most lists).
        new_edge (Tuple[_Vertex]): A tuple representing the new edge.

    Returns:
        bool: True if [u] => [v], False otherwise
    """

    for rank in old_rscp:
        for block in rank:
            for node in block.vertexes:
                if node == new_edge[0].label:
                    source_block = block
                elif node == new_edge[1].label:
                    destination_block = block

    if source_block is None:
        raise Exception(
            """It wasn't possible to determine the block of the source of the
            new edge"""
        )
    if destination_block is None:
        raise Exception(
            """It wasn't possible to determine the block of the destination of
            the new edge"""
        )

    # in fact the outer-most for-loop loops 2 times at most
    for vertex in predecessor_block:
        # we're interested in vertexes which aren't the source vertex of the
        # new edge.
        if vertex is not new_edge[0]:
            for dest in vertex.image:
                if dest.qblock == successor_block:
                    return True
            # we visited the entire image of a single block (not u) of [u], and
            # it didn't contain an edge to [v], therefore we conclude (since
            # the old partition is stable if we don't consider the new edge)
            # that an edge from [u] to [v] can't exist
            return False


def update_rscp(
    old_rscp: List[List[_Block]],
    new_edge: Tuple[int],
    initial_partition: List[Tuple[int]],
):
    source_vertex = None
    destination_vertex = None

    # if the new edge connects two blocks A,B such that A => B before the edge
    # is added we don't need to do anything
    if check_old_blocks_relation(
        old_rscp, (source_vertex, destination_vertex)
    ):
        return old_rscp
