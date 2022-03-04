from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch

class ScatterAndGatherContactTracing:

    def __init__(self, M):
        self.M = M
    
    def scatterAcrossEdges(self, graphList):
        valS = 0
        for i in range(0, self.M):
            isV = graphList[i][2]

            valS = isV*graphList[i][4] + (1-isV)*valS
            graphList[i][3] = isV*graphList[i][3] + (1-isV)*valS
        

    def gatherFromEdges(self, graphList):
        agg = 0
        for i in range(0, self.M):
            isV = graphList[i][2]

            #Check if data in edge is more than aggregate if so  need to update
            boolCheck = (graphList[i][3] > agg)
            
            #Need to update agg only if edge
            updateAgg = boolCheck*(1-isV)

            #Update aggregate in case of edge
            agg = updateAgg*(graphList[i][3]) + (1-updateAgg)*agg

            #Check if aggreagate is more than 1
            checkAgg = (agg >= 1)
            #Check if aggreagate is more than 1 plus the vertex value
            aggMoreValue = (agg >= graphList[i][4] + 1)
            #Condition to update vertex data
            updateVertex = checkAgg*isV*aggMoreValue

            #Getting value needed to update vertex
            valToSet = updateVertex*(agg - 1) 

            graphList[i][4] = updateVertex*valToSet + (1 - updateVertex)*graphList[i][4]
    
    







