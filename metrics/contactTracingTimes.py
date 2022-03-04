
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
import scatterAndGatherContactTracing
import graphStructure
import math
int_infinity = 100000000  


#Initialise Crypten
crypten.init()

torch.set_num_threads(1)




#Graph List structure (u, v, isVertex, data, covid risk, rho, residue, degree, dist, closenessCentrality)
@mpc.run_multiprocess(world_size = 2)
def getScatterAndGatherContactTracingMetrics():

    L = 10
    f = open(str(L)+'.csv', 'r')
    csv_reader = csv.reader(f)
    
    arr_used = []

    for row in csv_reader:
        cur = []
        for j in row:
            cur.append(int(j))
        arr_used.append(cur)

    a_enc = crypten.cryptensor(arr_used, ptype=crypten.mpc.arithmetic)

    scatterAndGatherContactTracingObject = scatterAndGatherContactTracing.ScatterAndGatherContactTracing(len(arr_used))
    graphStructureObject = graphStructure.EdgeListEncodedGraph(len(arr_used), a_enc, scatterAndGatherContactTracingObject)

    start_time = time.time()
    graphStructureObject.performScatter()
    graphStructureObject.performGather()
    end_time = time.time()

    print(end_time - start_time)

   

getScatterAndGatherContactTracingMetrics()
