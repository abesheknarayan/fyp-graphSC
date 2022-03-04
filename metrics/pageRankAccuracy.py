
#Contact Tracing times on graphs of sizes 10 to 1e6(1 iteration)
from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch
import sys
import random
import re
import time
import csv

  
# adding components to the system path
sys.path.insert(0, '../components')

import bitonicSort
import scatterAndGatherPageRank
import graphStructure
import graphStructurePlainText
import math
int_infinity = 100000000  


#Initialise Crypten
crypten.init()

torch.set_num_threads(1)

#Graph List structure (u, v, isVertex, data, covid risk, rho, residue, degree, dist, closenessCentrality)
@mpc.run_multiprocess(world_size = 2)
def getScatterAndGatherPageRankMetrics():

    L = 10
    f = open(str(L)+'.csv', 'r')
    csv_reader = csv.reader(f)
    
    arr_used = []

    for row in csv_reader:
        cur = []
        for j in row:

            cur.append(float(j))
        
        arr_used.append(cur)
    
    a_enc = crypten.cryptensor(arr_used, ptype=crypten.mpc.arithmetic)

    scatterAndGatherContactPageRankObject = scatterAndGatherPageRank.ScatterAndGatherPageRank(len(arr_used), 0.15, 0)
    scatterAndGatherContactPageRankObjectNE = scatterAndGatherPageRank.ScatterAndGatherPageRank(len(arr_used), 0.15, 1)
    graphStructureObjectEncrypted = graphStructure.EdgeListEncodedGraph(len(arr_used), a_enc, scatterAndGatherContactPageRankObject)
    graphStructureObject = graphStructurePlainText.EdgeListEncodedGraph(len(arr_used), arr_used, scatterAndGatherContactPageRankObjectNE)

    L = 2

    for i in range(0, L):
        graphStructureObjectEncrypted.performScatter()
        graphStructureObjectEncrypted.performGather()
        graphStructureObject.performScatter()
        graphStructureObject.performGather()
    
    rank = comm.get().get_rank()
    afterGraph = graphStructureObjectEncrypted.graphList.get_plain_text()
    afterGraphNE = graphStructureObject.graphList

    maxError = 0
    if rank == 0:

        for i in range(0, L):
            if afterGraph[i][0] == afterGraph[i][1]:
                print()
                maxError = max(maxError, abs(afterGraph[i][5] - afterGraphNE[i][5]))
        print(maxError)

getScatterAndGatherPageRankMetrics()
