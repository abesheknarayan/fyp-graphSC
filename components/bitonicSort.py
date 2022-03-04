from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch

class BitonicSort:
	def __init__(self, a, firstPriority, secondPriority, dir1, dir2):
		self.a = a
		self.n = len(a)
		self.firstPriority = firstPriority
		self.secondPriority = secondPriority
		self.dir1 = dir1
		self.dir2 = dir2


	def breakTie(self, i, j):
		greaterThan = (self.dir2*self.a[i][self.secondPriority] > self.dir2*self.a[j][self.secondPriority])
		
		return greaterThan

	def compAndSwap(self, i, j, dire):
		greaterThan = (self.dir1*self.a[i][self.firstPriority]> self.dir1*self.a[j][self.firstPriority])
		lessThan = (self.dir1*self.a[i][self.firstPriority] < self.dir1*self.a[j][self.firstPriority])

		boolValGT = greaterThan.get_plain_text()
		boolValLT = lessThan.get_plain_text()

		res = False

		if not boolValGT and not boolValLT:
			res = self.breakTie(i, j).get_plain_text()
		else:
			res = boolValGT

		if (dire == 1 and res) or (dire == 0 and not res):

			te = self.a.share[i]
			te1 = self.a.share[j]

			newShare = torch.zeros([len(self.a), 10], dtype=torch.long)
			b = self.a.share

			for k in range(0, len(b)):
				if k == i:
					newShare[k] = te1
				elif k == j:
					newShare[j] = te
				else:
					newShare[k] = b[k]

			rank = comm.get().get_rank()
		
			self.a.share = newShare


	def bitonicMerge(self, low, cnt, dire):
		if cnt > 1:
			k = cnt//2
			for i in range(low , low+k):
				self.compAndSwap(i, i+k, dire)
			self.bitonicMerge(low, k, dire)
			self.bitonicMerge(low+k, k, dire)


	def bitonicSort(self, low, cnt,dire):
		if cnt > 1:
			k = cnt//2
			self.bitonicSort(low, k, 1)
			self.bitonicSort(low+k, k, 0)
			self.bitonicMerge(low, cnt, dire)


	def sort(self, up):
		self.bitonicSort(0, self.n, up)

	
	def startSort(self):
		self.bitonicSort(0, self.n, 1)

