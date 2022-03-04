import sys
import random
import re
import time
import math
import csv

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


#n -> number of vertices
def generateGraph(n, arr_used, sparsity):
 
        adjacencyMatrix = []

        for i in range (0, n):
            row = []
            
            for j in range(0, n):
                if i == j:
                    row.append(0)
                else:
                    randVal =  random.random()
                    if randVal < sparsity:
                        row.append(1)
                    else:
                        row.append(0)
                    adjacencyMatrix.append(row)


        #Number of elements in each tuple
        L = 10

        #Create tuple for vertices
        for i in range(0, n):
            curTuple = []
            for j in range(0, L):
                curTuple.append(0)
            curTuple[0] = i+1
            curTuple[1] = i+1
            arr_used.append(curTuple)
        
        #Create tuple for edges
        for i in range(0, n):
            for j in range(0, n):
                if adjacencyMatrix[i][j]:
                    curTuple = []
                    for k in range(0, L):
                        curTuple.append(0)
                    curTuple[0] = i+1
                    curTuple[1] = j+1
                    arr_used.append(curTuple)

        #Add contact tracing data for n/10 vertices
        for i in range(0, math.floor(n/10)):
            arr_used[i][4] = 3

#Create seperate files for data sets of different sizes
def createSets():

    L = 10
    sparsity = 0.1
    for i in range(0, 4):
        arr_used = []
        random.seed(L)
        generateGraph(L, arr_used, sparsity)
        f = open(str(L)+'.csv', 'w')
        writer = csv.writer(f)

        for j in range(0, len(arr_used)):
            writer.writerow(arr_used[j])
        
        f.close()
        L = L*10
        sparsity /= 10

createSets()
