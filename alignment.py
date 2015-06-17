# authors: Daniel Gribel, Joao Paulo Forny

import numpy as np
import random
import time

start_time = time.time()

def init_memory(m, n, delta, alpha):
	M = np.zeros((m, n))
	
	for i in range(0, m):
		M[i, 0] = i*delta
	for j in range(0, n):
		M[0, j] = j*delta

	return M

# get alignment cost: O(n^2)
def get_alignment_cost(x, y, delta, alpha):
	m = len(x)
	n = len(y)
	M = init_memory(m+1, n+1, delta, alpha)
	
	for i in range(1, m+1):
		for j in range(1, n+1):
			mismatch = M[i-1, j-1]
			if x[i-1] != y[j-1]:
				mismatch = mismatch + alpha
			
			M[i, j] = min(mismatch, delta + M[i-1, j], delta + M[i, j-1])
	
	print M[m, n]
	return M

# find sequence: O(2n)
def find_sequence_iterative(M, i, j, x, y, delta, alpha):
	while(i != 0 and j != 0):
		mismatch = M[i-1, j-1]
		if x[i-1] != y[j-1]:
			mismatch = mismatch + alpha
		if M[i, j] == mismatch:
			#print(x[i-1], y[j-1])
			i = i-1
			j = j-1
		else:
			if M[i,j] == delta + M[i-1, j]:
				i = i-1
			else:
				j = j-1

alphabet = "abcd"
string_length = 10 * pow(2,7)
x = [random.choice(alphabet) for _ in range(string_length)]
y = [random.choice(alphabet) for _ in range(string_length)]

delta = 0.7
alpha = 1
M = get_alignment_cost(x, y, delta, alpha)
#print M
find_sequence_iterative(M, len(x), len(y), x, y, delta, alpha)

print(time.time() - start_time)