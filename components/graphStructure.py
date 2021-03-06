from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
from numpy import source
import torch
import bitonicSort

#Graph List structure (u, v, isVertex, data, covid risk, rho, residue, degree, )
class EdgeListEncodedGraph:

    #M is the size of the graph
    def __init__(self, M, graphList, scatterAndGatherObject):
        self.M = M
        self.graphList = graphList
        self.scatterAndGatherObject = scatterAndGatherObject

    #Source Sort where after the sorting protocol, 
    #the edge list representation will have vertices followed 
    #by all edges originating from that edges in the vertex
    def sourceSort(self):
        sortObject = bitonicSort.BitonicSort(self.graphList, 0, 2, 1, -1)
        sortObject.startSort()

    #Destination Sort where after the sorting protocol, 
    #the edge list representation will have edges that end at a 
    #particular vertex followed by the vertex itself
    def destinationSort(self):
        sortObject = bitonicSort.BitonicSort(self.graphList, 1, 2, 1, 1)
        sortObject.startSort()

    def performScatter(self):
        self.sourceSort()
        self.scatterAndGatherObject.scatterAcrossEdges(self.graphList)
    
    def performGather(self):
        self.destinationSort()
        self.scatterAndGatherObject.gatherFromEdges(self.graphList)
    
    def updateClosenessCentrality(self, sourceVertex):
        
        #Update closeness centrality of source vertex in 2 steps.
        #First get sum of all d(sV, v) for all v and number of vertices n
        sd = 0
        nv = 0
        for i in range(0, len(self.graphList)):
            if self.graphList[i][0] == self.graphList[i][1]:
                sd = sd + self.graphList[i][8]
                nv = nv + 1

       
        #Find n-1/d which is closeness centrality
        self.graphList[i][9] = (nv-1)/sd
        

