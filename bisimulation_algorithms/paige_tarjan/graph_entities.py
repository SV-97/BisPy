from llist import dllist, dllistnode


class _Vertex:
    """The internal representation of the vertex of a graph. This is used by the algorithm to hold all the needed data structure, in order to access them in O(1).

    Attributes:
        label                   The unique identifier of this vertex.
        qblock                  The QBlock instance this vertex belongs to.
        visited                 A flag used in the algorithm to mark vertexes which it has already visited.
        counterimage            A list of _Edge instances such that edge.destination = self. This shouldn't be touched manually.
        image                   A list of _Edge instances such that edge.source = self. This shouldn't be touched manually.
        aux_count               An auxiliary _Count instance used to compute |B cap E({self})|.
        in_second_splitter      A flag used during the computation of the counterimage of blocks to avoid duplicates.
        dllistnode              A reference to the instance of dllistobject representing this vertex in the QBlock it belongs to.
    """

    def __init__(self, label):
        """The constructor of the class Vertex.

        Args:
            label (int): A unique label which identifies this vertex among all the others (usually its index in a list of vertexes).
        """

        self.label = label
        self.qblock = None
        self.dllistnode = None

        self.visited = False
        self.in_second_splitter = False

        self.counterimage = []
        self.image = []

        self.aux_count = None

    def add_to_counterimage(self, edge):
        self.counterimage.append(edge)

    def add_to_image(self, edge):
        self.image.append(edge)

    def visit(self):
        self.visited = True

    def release(self):
        self.visited = False

    def added_to_second_splitter(self):
        self.in_second_splitter = True

    def clear_second_splitter_flag(self):
        self.in_second_splitter = False

    def __str__(self):
        return "V{}".format(self.label)

    def __repr__(self):
        return "V{}".format(self.label)


class _Edge:
    """Represents an edge between two _Vertex instances.

    Attributes:
        source                  The source _Vertex of this edge.
        destination             The destination _Vertex of this edge.
        count                   A _Count instance which holds |E({source}) cap S|, where S is the block of X destination belongs to.
    """

    def __init__(self, source: _Vertex, destination: _Vertex):
        self.source = source
        self.destination = destination

        # holds the value count(source,S) = |E({source}) \cap S|
        self.count = None

    # this is only used for testing purposes
    def __hash__(self):
        return hash("{}-{}".format(self.source.label, self.destination.label))

    def __eq__(self, other):
        return (
            isinstance(other, _Edge)
            and self.source == other.source
            and self.destination == other.destination
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "<{},{}>".format(self.source, self.destination)

    def __repr__(self):
        return "<{},{}>".format(self.source, self.destination)


class _QBlock:
    """A block of Q in the Paige-Tarjan algorithm.

    Attributes:
        size                    The number of vertexes in this block. This is updated automatically by append/remove_vertex.
        vertexes                A dllist which contains the vertexes in this block.
        xblock                  The (unique) block S of X such that S = A cup self, for some A.
        split_helper_block      A reference for O(1) access to a new block created from this block during the split phase.
        dllistnode              A reference to the dllistobject which represents this QBlock in xblock.
    """

    def __init__(self, vertexes, xblock):
        self.size = len(vertexes)
        self.vertexes = dllist(vertexes)
        self.xblock = xblock
        self.split_helper_block = None
        self.dllistnode = None

    # this doesn't check if the vertex is a duplicate.
    # make sure that vertex is a proper _Vertex, not a dllistnode
    def append_vertex(self, vertex: _Vertex):
        self.size += 1
        vertex.dllistnode = self.vertexes.append(vertex)
        vertex.qblock = self

    # throws an error if the vertex isn't inside this qblock
    def remove_vertex(self, vertex: _Vertex):
        self.size -= 1
        self.vertexes.remove(vertex.dllistnode)
        vertex.qblock = None

    def initialize_split_helper_block(self):
        self.split_helper_block = _QBlock([], self.xblock)

    def reset_helper_block(self):
        self.split_helper_block = None

    def __str__(self):
        return "Q({})".format(",".join([str(vertex) for vertex in self.vertexes]))

    def __repr__(self):
        return "Q({})".format(",".join([str(vertex) for vertex in self.vertexes]))


class _XBlock:
    """A block of X in the Paige-Tarjan algorithm.

    Attributes:
        qblocks                     A dllist which contains the blocks Q1,...,Qn such that the union of Q1,...,Qn is equal to self.
    """

    def __init__(self):
        self.qblocks = dllist([])

    def append_qblock(self, qblock: _QBlock):
        qblock.dllistnode = self.qblocks.append(qblock)
        qblock.xblock = self

    def remove_qblock(self, qblock: _QBlock):
        self.qblocks.remove(qblock.dllistnode)
        qblock.xblock = None

    def __str__(self):
        return "X[{}]".format(",".join([str(qblock) for qblock in self.qblocks]))

    def __repr__(self):
        return "X[{}]".format(",".join([str(qblock) for qblock in self.qblocks]))


# holds the value of count(vertex,_XBlock) = |_XBlock \cap E({vertex})|
class _Count:
    """A class whcih represents a value. This is used to hold, share, and propagate changes in O(1) between all the interested entities (vertexes in the case of vertex.aux_count, edges in the case of edge.count).

    Attributes:
        vertex                    The vertex this instance is associated to, namely the x such that self = count(x,A).
        xblock                    The XBlock this isntance is associated to, namely the S such that self = count(x,S).
        value                     The current value of this instance (shared between all the "users" of the reference).
    """

    def __init__(self, vertex: _Vertex):
        self.vertex = vertex
        self.value = 0

    def __str__(self):
        return "C{}:{}".format(self.vertex, self.label)

    def __repr__(self):
        return "C{}:{}".format(self.vertex, self.label)
