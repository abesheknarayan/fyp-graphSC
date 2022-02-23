from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
from numpy import source
import torch
import bitonicSort
import scatterAndGather


class EdgeListEncodedGraph:

    #M is the size of the graph
    def __init__(self, M, graphList):
        self.M = M
        self.graphList = graphList

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
        scatterGatherObject = scatterAndGather.ScatterAndGather(self.M)
        scatterGatherObject.scatterAcrossEdges(self.graphList)
    
    def performGather(self):
        self.destinationSort()
        scatterGatherObject = scatterAndGather.ScatterAndGather(self.M)
        scatterGatherObject.gatherFromEdges(self.graphList)

        

