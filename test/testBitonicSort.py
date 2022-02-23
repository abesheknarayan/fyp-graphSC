from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch
import sys
  
# adding components to the system path
sys.path.insert(0, '../components')

import bitonicSort

#Initialise Crypten
crypten.init()

torch.set_num_threads(1)

@mpc.run_multiprocess(world_size=2)
def testBitonicSort():

    arr_used = [[1, 1, 1, 2], [2, 2, 1, 3], [3, 3, 1, 3], [4, 4, 1, 5], [1, 3, 0, 6], [3, 4, 0, 1], [4, 2, 0, 20], [2, 3, 0, -1]]

    a_enc = crypten.cryptensor(arr_used, ptype=crypten.mpc.arithmetic)

    print(a_enc)
    sortObject = bitonicSort.BitonicSort(a_enc, 0, 2, 1, -1)
    
    sortObject.startSort()
    a = a_enc.get_plain_text() 

    rank = comm.get().get_rank()
    
    expectedResult = [[1, 1, 1, 2], [1, 3, 0, 6], [2, 2, 1, 3], [2, 3, 0, -1], [3, 3, 1, 3], [3, 4, 0, 1], [4, 4, 1, 5], [4, 2, 0, 20]]

    if rank == 0:
        for i in range(0, len(a)):
            for j in range(0, 4):
                assert(a[i][j] == expectedResult[i][j])


testBitonicSort()
