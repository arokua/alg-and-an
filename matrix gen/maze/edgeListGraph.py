# ------------------------------------------------------------------------
# Please COMPLETE the IMPLEMENTATION of this class.
# Adjacent list implementation.
#
# __author__ = 'Jeffrey Chan', <YOU>
# __copyright__ = 'Copyright 2024, RMIT University'
# ------------------------------------------------------------------------


from typing import List, Set, Dict, Tuple

from maze.util import Coordinates
from maze.graph import Graph


class EdgeListGraph(Graph):
    """
    Represents an undirected graph using a dictionary for edge storage.
    """

    def __init__(self, rowNum:int, colNum:int):
        #Empty adjacent list initializtion
        self.vertexSet: Set[Coordinates] = set()
        self.edgeDict: list[Coordinates, Dict[Coordinates, bool]] = {} #Actually acts like adjacency matrix , decrease run time
        self.nRows = 0
        self.nCols = 0


    def addVertex(self, label: Coordinates):
        """Add a single vertex if it doesn't already exist."""
        if label not in self.vertexSet:
            self.vertexSet.add(label)
            self.edgeDict[label] = {} # Newly added node/vertex have no edges


    def addVertices(self, vertLabels: List[Coordinates]):
        """Add multiple vertices, ensuring no duplicates."""
        for v in vertLabels:
            self.addVertex(v)
    def addEdge(self, vert1: Coordinates, vert2: Coordinates, addWall: bool = False) -> bool:
        """Adds an edge to the graph. An edge is defined by two vertex labels."""
        if vert1 in self.vertexSet and vert2 in self.vertexSet and vert1.isAdjacent(vert2):
            if vert2 not in self.edgeDict[vert1]:
                self.edgeDict[vert1][vert2] = addWall
                self.edgeDict[vert2][vert1] = addWall  # Undirected graph
                return True
        return False

    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool) -> bool:
        """Updates the wall status between two adjacent vertices."""
        if vert2 in self.edgeDict[vert1]:
            self.edgeDict[vert1][vert2] = wallStatus
            self.edgeDict[vert2][vert1] = wallStatus  # Undirected graph
            return True
        return False

    def removeEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """Removes an edge between two vertices."""
        if vert2 in self.edgeDict[vert1]:
            del self.edgeDict[vert1][vert2]
            del self.edgeDict[vert2][vert1]  # Undirected graph
            return True
        return False

    def hasEdge(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """Checks if an edge exists between two vertices."""
        return vert2 in self.edgeDict[vert1]

    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates) -> bool:
        """Gets the wall status between two vertices."""
        return self.edgeDict.get(vert1, {}).get(vert2, False)
    
    def getEdgesList(self):
        for vert in self.edgeDict:
            x=vert.getRow
            y=vert.getCol
            print((x,y),self.edgeDict[vert])
        pass


    def neighbours(self, label: Coordinates) -> List[Coordinates]:
        """retrieves all the neighobors of a vertex"""
        return list(self.edgeDict[label].keys())
        