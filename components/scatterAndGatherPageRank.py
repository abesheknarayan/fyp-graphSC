from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch

#Graph List structure (u, v, isVertex, data, covid risk, rho, residue, degree, dist, closenessCentrality)
class ScatterAndGatherPageRank:

    def __init__(self, M,  alpha, type):
        self.M = M
        self.rho = []*M
        self.y = 1
        self.alpha = alpha
        self.oneMinusAlpha = 1
        self.type = type
    
    def scatterAcrossEdges(self, graphList):
        
        valS = 0
        for i in range(0, self.M):
            isV = graphList[i][2]

            #Get Yj+1/Yj
            weightToSubtract = self.oneMinusAlpha*self.alpha   
            term1 = (self.y - weightToSubtract)/self.y

            degreeNotZero = (graphList[i][7] != 0)

            if self.type == 0:
                degreeNotZero = degreeNotZero.get_plain_text()
            
            term2 = 0

            if degreeNotZero:
                term2 = (graphList[i][6]/graphList[i][7])

            finalTerm = term1*term2

            valS = isV*finalTerm + (1-isV)*valS
            graphList[i][3] = isV*graphList[i][3] + (1-isV)*valS
    

    def gatherFromEdges(self, graphList):
        agg = 0
        for i in range(0, self.M):
            isV = graphList[i][2]

            term1 = (self.alpha*self.oneMinusAlpha)/self.y  
            term1 = term1*graphList[i][6]
            term2 = term1 + graphList[i][5]

            #update rho only if vertex
            graphList[i][5] = graphList[i][5]*(1-isV) + isV*term2

            term3 = agg

            #update residue only if vertex
            graphList[i][6] = graphList[i][6]*(1-isV) + isV*term3

            term4 = agg + graphList[i][3]
            #Set agg as 0 if vertex
            agg = (1-isV)*term4

            #Update y
            self.y = self.y - (self.alpha*self.oneMinusAlpha)

            #Update oneMinusAlpha
            self.oneMinusAlpha = self.oneMinusAlpha*(1-self.alpha)









