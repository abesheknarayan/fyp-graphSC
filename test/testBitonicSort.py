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

    arr_used = [4, 1, 2, 3]

    a_enc = crypten.cryptensor(arr_used, ptype=crypten.mpc.arithmetic)
    sortObject = bitonicSort.BitonicSort(a_enc)
    
    sortObject.startSort()
    a = a_enc.get_plain_text() 

    rank = comm.get().get_rank()

    list.sort(arr_used)

    if rank == 0:
        for i in range(0, len(a)):
            assert(a[i] == arr_used[i])


testBitonicSort()
