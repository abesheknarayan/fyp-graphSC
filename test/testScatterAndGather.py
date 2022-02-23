from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch
import sys
  
# adding components to the system path
sys.path.insert(0, '../components')

import bitonicSort
import scatterAndGather
import graphStructure

#Initialise Crypten
crypten.init()

torch.set_num_threads(1)

@mpc.run_multiprocess(world_size=2)
def testScatterAndGather():

    arr_used = [[1, 1, 1, 0], [2, 2, 1, 3], [3, 3, 1, 0], [4, 4, 1, 0], [1, 3, 0, 6], [3, 4, 0, 1], [4, 2, 0, 20], [2, 3, 0, -1]]

    a_enc = crypten.cryptensor(arr_used, ptype=crypten.mpc.arithmetic)

    graphStructureObject = graphStructure.EdgeListEncodedGraph(len(arr_used), a_enc)

    L = 1

    for i in range(0, L):
        graphStructureObject.performScatter()
        graphStructureObject.performGather()

    rank = comm.get().get_rank()
    afterGraph = graphStructureObject.graphList.get_plain_text()
    if rank == 0:
        print(afterGraph)

   

testScatterAndGather()
