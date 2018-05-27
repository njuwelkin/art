from art_individual import *

chrom = np.zeros(AllPossibleEdges, dtype="bool")
mat = np.zeros((Nodes, Nodes), dtype="bool")

edgePerNode = Edges / Nodes
step = Nodes / (4 * edgePerNode)
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
    length = Nodes - start - 1
    chrom[start: length] = mat[i, Nodes-length:]
    start += length


print mat[0]
print mat[Nodes / 2]
print mat[Nodes - 1]
