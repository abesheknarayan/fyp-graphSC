from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch
int_infinity = 100000000  

#Graph List structure (u, v, isVertex, data, covid risk, rho, residue, degree, dist, closenessCentrality)
class ScatterAndGatherClosenessCentrality:

    def __init__(self, M):
        self.M = M
    
    def scatterAcrossEdges(self, graphList):
      
        valS = 0
        for i in range(0, self.M):
            isV = graphList[i][2]

            valS = isV*graphList[i][8] + (1-isV)*valS
    
            graphList[i][3] = isV*graphList[i][3] + (1-isV)*valS

        rank = comm.get().get_rank()
        afterGraph = graphList.get_plain_text()
        # if rank == 0:
        #     for i in range(0, len(afterGraph)):
        #         print(afterGraph[i][0], afterGraph[i][1], afterGraph[i][3])


    def gatherFromEdges(self, graphList):

        agg = int_infinity
        for i in range(0, self.M):
            isV = graphList[i][2]

            #First step is to get minimum dist from all incoming edges
            condition1 = (graphList[i][3] < agg)
            conditionToUpdateAggregate = (1-isV)*(condition1)
            agg = conditionToUpdateAggregate*graphList[i][3] + (1-conditionToUpdateAggregate)*agg


            #Next, if tuple is vertex and the value in the distance is inf, update the minDist provided agg 
            condition2 = isV*(agg < int_infinity)
            conitionUpdateVertex = condition2*(graphList[i][8] >= int_infinity)
            graphList[i][8] = conitionUpdateVertex*(agg+1) + (1-conitionUpdateVertex)*graphList[i][8]

            #Set agg as int_infinity if vertex
            agg = isV*int_infinity + (1-isV)*agg





