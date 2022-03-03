from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch
import sys

import math
  
int_infinity = 100000000  
# adding components to the system path
sys.path.insert(0, '../components')

import bitonicSort
import scatterAndGatherPageRank
import graphStructure


#Initialise Crypten
crypten.init()

torch.set_num_threads(1)


def nextPowerOf2(n):
    count = 0
 
    # First n in the below
    # condition is for the
    # case where n is 0
    if (n and not(n & (n - 1))):
        return n
     
    while( n != 0):
        n >>= 1
        count += 1
     
    return 1 << count

#Graph List structure (u, v, isVertex, data, covid risk, rho, residue, degree)
@mpc.run_multiprocess(world_size=2)
def testScatterAndGatherContactTracing():

    arr_used = [[1, 1, 1, 0, 0, 0, 1/4, 1, 0, 0], [2, 2, 1, 0, 3, 0, 1/4, 2, 0, 0], [3, 3, 1, 0, 0, 0, 1/4, 3, 0, 0], [4, 4, 1, 0, 0, 0, 1/4, 2, 0, 0], [1, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 1, 0, 0, 0, 0, 0, 0, 0, 0], [3, 4, 0, 0, 1, 0, 0, 0, 0, 0], [4, 3, 0, 0, 1, 0, 0, 0, 0, 0], [4, 2, 0, 0, 0, 0, 0, 0, 0, 0], [2, 4, 0, 0, 0, 0, 0, 0, 0, 0], [2, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 2, 0, 0, 0, 0, 0, 0, 0, 0]]
    nearestPowerOf2 = nextPowerOf2(len(arr_used))

    
    for i in range(0, nearestPowerOf2 - len(arr_used)):
        arr_used.append([int_infinity, int_infinity,int_infinity, int_infinity, int_infinity, int_infinity, int_infinity, int_infinity, int_infinity, int_infinity])
    for i in range(0, len(arr_used)): 
        arr_used[i][8] = int_infinity
    
    arr_used[0][8] = 0

    a_enc = crypten.cryptensor(arr_used, ptype=crypten.mpc.arithmetic)

    scatterAndGatherContactPageRankObject = scatterAndGatherPageRank.ScatterAndGatherPageRank(len(arr_used), 0.15)
    graphStructureObject = graphStructure.EdgeListEncodedGraph(len(arr_used), a_enc, scatterAndGatherContactPageRankObject)

    L = 2

    for i in range(0, L):
        graphStructureObject.performScatter()
        graphStructureObject.performGather()

    rank = comm.get().get_rank()
    afterGraph = graphStructureObject.graphList.get_plain_text()
    if rank == 0:
        for i in range(0, len(afterGraph)):
            if afterGraph[i][0] == afterGraph[i][1]:
                print(afterGraph[i][0], afterGraph[i][1], afterGraph[i][5])

testScatterAndGatherContactTracing()
