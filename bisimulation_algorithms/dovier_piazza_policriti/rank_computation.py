from .graph_entities import _Vertex
from typing import List

_BLACK = 10
_GRAY = 11
_WHITE = 12


def counterimage_dfs(
    current_vertex_idx: int,
    vertexes: List[_Vertex],
    finishing_list: List[_Vertex],
    colors: List[int],
):
    # mark this vertex as "visiting"
    colors[current_vertex_idx] = _GRAY
    # visit the counterimage of the current vertex
    for counterimage_vertex in vertexes[current_vertex_idx].counterimage:
        # if the vertex isn't white, a visit is occurring, or has already
        # occurred.
        if colors[current_vertex_idx] == _WHITE:
            counterimage_dfs(
                current_vertex_idx=counterimage_vertex.label,
                vertexes=vertexes,
                finishing_list=finishing_list,
                colors=colors,
            )
    # this vertex visit is over: add the vertex to the ordered list of
    # finished vertexes
    finishing_list.append(vertexes[current_vertex_idx])
    # mark this vertex as "visited"
    colors[current_vertex_idx] = _BLACK


def dfs_and_rank(
    current_vertex_idx: int,
    vertexes: List[_Vertex],
    colors: List[int],
):
    # mark this vertex as "visiting"
    colors[current_vertex_idx] = _GRAY

    if len(vertexes[current_vertex_idx].image) == 0:
        # this is a leaf
        vertexes[current_vertex_idx].rank = 0
    else:
        max_rank = float("-inf")

        # visit the counterimage of the current vertex
        for image_vertex in vertexes[current_vertex_idx].image:
            # if image_vertex's finishing time is before current_vertex's,
            # current_vertex is NWF
            image_vertex_color = colors[image_vertex.label]
            if (
                image_vertex_color == _WHITE
                or image_vertex_color == _GRAY
                or not image_vertex.wf
            ):
                vertexes[current_vertex_idx].wf = False

            # if the vertex isn't white, a visit is occurring, or has already
            # occurred. Therefore skip.
            if image_vertex_color == _WHITE:
                dfs_and_rank(
                    current_vertex_idx=image_vertex.label,
                    vertexes=vertexes,
                    colors=colors,
                )

            if image_vertex.rank is not None:
                max_rank = max(
                    max_rank, image_vertex.rank + (1 if image_vertex.wf else 0)
                )

        # set the rank
        vertexes[current_vertex_idx].rank = max_rank
    # mark this vertex as "visited"
    colors[current_vertex_idx] = _BLACK


def compute_rank(vertexes: List[_Vertex]):
    counterimage_dfs_colors = [_WHITE for _ in range(len(vertexes))]
    counterimage_finishing_list = []
    # perform counterimage DFS
    for idx in range(len(vertexes)):
        if counterimage_dfs_colors[idx] == _WHITE:
            counterimage_dfs(
                current_vertex_idx=idx,
                vertexes=vertexes,
                finishing_list=counterimage_finishing_list,
                colors=counterimage_dfs_colors,
            )

    # perform a visit using the order induced by the finishing time of the
    # counterimage DFS (for decreasing values of finishing time)
    image_dfs_colors = [_WHITE for _ in range(len(vertexes))]
    for idx in range(len(vertexes) - 1, -1, -1):
        if image_dfs_colors[idx] == _WHITE:
            dfs_and_rank(
                current_vertex_idx=idx,
                vertexes=vertexes,
                colors=image_dfs_colors,
            )
