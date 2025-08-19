import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self.parziale = []
        self.solutions = {}

    def getColors(self):
        return DAO.getColors()

    def createGraph(self, year, color):
        self._graph.clear()
        nodes = DAO.getNodes(color)
        for n in nodes:
            self._idMap[n.Product_number] = n
        self._graph.add_nodes_from(nodes)
        edges = DAO.getEdges(year, color)
        for e in edges:
            self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[5])


    def getEdgesMaxWeight(self):
        edgesList = list(self._graph.edges)
        edgesList.sort(key=lambda e: self._graph.get_edge_data(e[0], e[1])["weight"], reverse=True)
        return edgesList[:3]

    def getRepeatedProducts(self):
        maxEdges = self.getEdgesMaxWeight()
        prod = []
        rep = []
        for e in maxEdges:
            prod.append(e[0])
            prod.append(e[1])
        for p in prod:
            if p.Product_number not in rep:
                if prod.count(p) > 1:
                    rep.append(p.Product_number)
        return rep

    def getNumNodes(self):
        return len(self._graph.nodes())

    def getNumEdges(self):
        return len(self._graph.edges())

    def getMaxPath(self, source, graph):
        self.parziale = [source]
        self.solutions = {}
        self.findNext(self.parziale, graph)
        nmax_edges = max(self.solutions)
        return self.solutions[nmax_edges]

    def findNext(self, parziale, graph):
        neighbors = list(graph.neighbors(parziale[-1]))
        for n in neighbors:
            addable = True
            if len(parziale) >= 2:
                if n != parziale[-2]:
                    for i in range(0, len(parziale)-1):
                        if graph.get_edge_data(parziale[-1], n)['weight'] < graph.get_edge_data(parziale[i], parziale[i+1])['weight']:
                            addable = False
                            break
                    if addable:
                        parziale.append(n)
                        self.findNext(parziale, graph)
            else:
                parziale.append(n)
                self.findNext(parziale, graph)
        self.solutions[len(parziale)-1] = copy.deepcopy(parziale)
        parziale.pop()

