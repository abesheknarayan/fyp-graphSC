from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch
import sys
  
# adding components to the system path
sys.path.insert(0, '../components')

import bitonicSort
int_infinity = 100000000  

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


@mpc.run_multiprocess(world_size=2)
def testBitonicSort():

    arr_used = [[1, 1, 1, 0, 0, 0, 1/4, 1, 0, 0], [2, 2, 1, 0, 3, 0, 1/4, 2, 0, 0], [3, 3, 1, 0, 0, 0, 1/4, 3, 0, 0], [4, 4, 1, 0, 0, 0, 1/4, 2, 0, 0], [1, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 1, 0, 0, 0, 0, 0, 0, 0, 0], [3, 4, 0, 0, 1, 0, 0, 0, 0, 0], [4, 3, 0, 0, 1, 0, 0, 0, 0, 0], [4, 2, 0, 0, 0, 0, 0, 0, 0, 0], [2, 4, 0, 0, 0, 0, 0, 0, 0, 0], [2, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 2, 0, 0, 0, 0, 0, 0, 0, 0]]

    nearestPowerOf2 = nextPowerOf2(len(arr_used))

    for i in range(0, nearestPowerOf2 - len(arr_used)):
        arr_used.append([int_infinity, int_infinity,int_infinity, int_infinity, int_infinity, int_infinity, int_infinity, int_infinity, int_infinity, int_infinity])
    a_enc = crypten.cryptensor(arr_used, ptype=crypten.mpc.arithmetic)

    print(a_enc)
    sortObject = bitonicSort.BitonicSort(a_enc, 0, 2, 1, -1)
    
    sortObject.startSort()
    a = a_enc.get_plain_text() 

    rank = comm.get().get_rank()
   
    if rank == 0:
        print(a)

testBitonicSort()
