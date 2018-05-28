from copy import deepcopy
import numpy as np
from scipy import sparse

from art_config import *


def _initTemplet():
	chrom = np.zeros(AllPossibleEdges, dtype="bool")
	mat = np.zeros((Nodes, Nodes), dtype="bool")

	edgePerNode = Edges*2 / Nodes
	step = Nodes / (2 * edgePerNode)
	for i in range(0, Nodes):
	    j= (i + step) % Nodes
	    for k in range(0, edgePerNode/2):
		if i < j:
		    mat[i, j] = True
		else:
		    mat[j, i] = True
		j = (j + step) % Nodes

	start = 0
	for i in range(0, Nodes):
	    length = Nodes - i - 1
	    chrom[start: start + length] = mat[i, Nodes-length:Nodes]
	    start += length
	return chrom.reshape((AllPossibleEdges/GenLen, GenLen))
      

_chromTemplet = _initTemplet()


class ArtIndividual(object):
    """
    variable-length encoding
    """
    #mask = ~ np.tril(np.ones((Nodes, Nodes), dtype="bool"))

    def __init__(self, initMethod = 0):
        super(self.__class__, self).__init__()

        if initMethod == 1:    # random
            tmp = np.random.random(AllPossibleEdges)
            chrom = (tmp < (Dencity)).reshape((AllPossibleEdges/GenLen, GenLen))
            #chrom = (tmp < (0.1)).reshape((AllPossibleEdges/GenLen, GenLen))
            self.setChrom(chrom)
        elif initMethod == 2:
            chrom = _chromTemplet.copy()
            self.setChrom(chrom)

    def setChrom(self, chrom):
        assert chrom.size == AllPossibleEdges
        self.chromsome = chrom
        self._chromsome = chrom.ravel()
        self._gen_chrom_mat()
        self._gen_solution()

    def _gen_solution(self):
        coo = sparse.coo_matrix(self.mat)
        self.solution = np.array(zip(coo.row, coo.col), dtype="uint8")

    def _gen_chrom_mat(self):
        mat = np.zeros((Nodes, Nodes), dtype="bool")
        start = 0
        len = Nodes - 1
        for i in range(0, Nodes-1):
            mat[i, i+1: Nodes] = self._chromsome[start: start+len]
            start += len
            len -= 1
        self.mat = mat

    def clone(self):
        indv = self.__class__()
        indv.setChrom(self.chromsome.copy())
        return indv




if __name__ == '__main__':
    a=ArtIndividual(2)
    print "***************"
    print a.chromsome
    print len(a.chromsome)
    print a.chromsome.sum()
    print "***************"
    print a.mat
    print a.mat.sum()
    print "***************"
    print a.solution
    print len(a.solution)
