# ------------------------------------------------------------------------
# Please COMPLETE the IMPLEMENTATION of this class.
# Adjacent matrix implementation.
#
# __author__ = 'Jeffrey Chan', <YOU>
# __copyright__ = 'Copyright 2024, RMIT University'
# ------------------------------------------------------------------------


from typing import List, Dict, Tuple, Set
from maze.util import Coordinates
from maze.graph import Graph

class IncMatGraph(Graph):
    """
    Represents an undirected graph using an optimized adjacency matrix.
    """

    def __init__(self):
        self.vertexList: List[Coordinates] = []  # Store vertices
        self.vertexIndex: Dict[Coordinates, int] = {}  # Map each vertex to an index
        self.edgeMatrix: List[List[bool]] = []  # 2D list for adjacency matrix
        self.nVertices = 0  # Track the number of vertices

    def addVertex(self, label: Coordinates):
        """Add a single vertex if it doesn't already exist."""
        if label not in self.vertexIndex:
            self.vertexIndex[label] = self.nVertices
            self.vertexList.append(label)
            self.nVertices += 1

            # Expand the adjacency matrix for the new vertex
            for row in self.edgeMatrix:
                row.append(False)  # Add False to each existing row for the new vertex
            self.edgeMatrix.append([False] * self.nVertices)  # Add a new row for the new vertex

    def addVertices(self, vertLabels: List[Coordinates]):
        """Add multiple vertices, ensuring no duplicates."""
        for v in vertLabels:
            self.addVertex(v)

    def addEdge(self, vert1: Coordinates, vert2: Coordinates, addWall: bool = False) -> bool:
        """Adds an edge to the graph. An edge is defined by two vertex labels."""
        if vert1 in self.vertexIndex and vert2 in self.vertexIndex and vert1.isAdjacent(vert2):
            i, j = self.vertexIndex[vert1], self.vertexIndex[vert2]
            if not self.edgeMatrix[i][j]:  # Add edge only if it doesn't exist
                self.edgeMatrix[i][j] = addWall
                self.edgeMatrix[j][i] = addWall  # Symmetric for undirected graph
                return True
        return False

    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool) -> bool:
        """Updates the wall status between two adjacent vertices."""
        if vert1 in self.vertexIndex and vert2 in self.vertexIndex:
            i, j = self.vertexIndex[vert1], self.vertexIndex[vert2]
            self.edgeMatrix[i][j] = wallStatus
            self.edgeMatrix[j][i] = wallStatus  # Symmetric for undirected graph
            return True
        return False

    def removeEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """Removes an edge between two vertices."""
        if vert1 in self.vertexIndex and vert2 in self.vertexIndex:
            i, j = self.vertexIndex[vert1], self.vertexIndex[vert2]
            if self.edgeMatrix[i][j]:
                self.edgeMatrix[i][j] = False
                self.edgeMatrix[j][i] = False  # Symmetric for undirected graph
                return True
        return False

    def hasVertex(self, label: Coordinates) -> bool:
        """Checks if a vertex exists in the graph."""
        return label in self.vertexIndex

    def hasEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """Checks if an edge exists between two vertices."""
        if vert1 in self.vertexIndex and vert2 in self.vertexIndex:
            i, j = self.vertexIndex[vert1], self.vertexIndex[vert2]
            return self.edgeMatrix[i][j]
        return False

    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """Gets the wall status between two vertices."""
        if vert1 in self.vertexIndex and vert2 in self.vertexIndex:
            i, j = self.vertexIndex[vert1], self.vertexIndex[vert2]
            return self.edgeMatrix[i][j]
        return False

    def neighbours(self, label: Coordinates) -> List[Coordinates]:
        """Retrieves all the neighbours of a vertex."""
        if label in self.vertexIndex:
            index = self.vertexIndex[label]
            return [self.vertexList[j] for j in range(self.nVertices) if self.edgeMatrix[index][j]]
        return []