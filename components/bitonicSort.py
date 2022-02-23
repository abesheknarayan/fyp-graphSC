from ctypes import addressof
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
import torch

class BitonicSort:
	def __init__(self, a):
		self.a = a
		self.n = len(a)


	def compAndSwap(self, i, j, dire):
		greaterThan = (self.a[i] > self.a[j])

		boolVal = greaterThan.get_plain_text()

		if (dire == 1 and boolVal) or (dire == 0 and not boolVal):

			te = self.a.share[i]
			te1 = self.a.share[j]

			newShare = []
			b = self.a.share

			for k in range(0, len(b)):
				if k == i:
					newShare.append(te1)
				elif k == j:
					newShare.append(te)
				else:
					newShare.append(b[k])
		
			self.a.share = torch.tensor(newShare)


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

