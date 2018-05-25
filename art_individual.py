from copy import deepcopy
from components.individual import IndividualBase
import numpy as np

from art_config import *

class ArtIndividual(IndividualBase):
    def __init__(self, nodes = Nodes, line_per_node = EdgePerNode):

        self.nodes = nodes
        self.line_per_nodes = line_per_node
        ranges = [(0, line_per_node)] * nodes

        super(self.__class__, self).__init__()

        # Initialize individual randomly.
        self.init()

    def encode(self):
        '''
        Encode solution to gene sequence in individual using different encoding.
        '''
        chromsome = self.solution.view()
        chromsome.shape = self.nodes * self.line_per_nodes

        return chromsome

    def decode(self):
        ''' 
        Decode gene sequence to solution of target function.
        '''
        solution =  self.chromsome.view()
        solution.shape = self.nodes, self.line_per_nodes
        return solution

    def _rand_solution(self):
        solution = np.random.random((self.nodes, self.line_per_nodes)) * self.nodes
        solution=np.array(solution, dtype="uint8")
        return solution


AllPossibleEdges = Nodes * (Nodes - 1) / 2
Edges = 1000
Dencity = float(Edges) / AllPossibleEdges

class ArtIndividual2(IndividualBase):
    """
    variable-length encoding
    """
    def __init__(self, randomChrom = False):
        super(self.__class__, self).__init__()

        if randomChrom:
            len = Nodes * (Nodes - 1) / 2
            tmp = np.random.random(AllPossibleEdges)
            self.chromsome = (tmp < Dencity)
            self.init(chromsome=self.chromsome)
        else:
            self.init()

    def encode(self):
        pass

    def decode(self):
        p = 0
        solution = []
        for i in range(0, Nodes):
            for j in range(i+1, Nodes):
                if self.chromsome[p]:
                    solution.append((i, j))
                p += 1


if __name__ == '__main__':
    lines = ArtIndividual()
