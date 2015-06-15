# authors: Daniel Gribel, Joao Paulo Forny

import numpy as np

def init_memory(m, n, delta, alpha):
	M = np.zeros((m, n))
	
	for i in range(0, m):
		M[i, 0] = i*delta
	for j in range(0, n):
		M[0, j] = j*delta

	return M

def sequence_alignment(x, y, delta, alpha):
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

def find_sequence(M, i, j, x, y, delta, alpha):
	if i == 0 or j == 0:
		return
	else:
		mismatch = M[i-1, j-1]
		if x[i-1] != y[j-1]:
			mismatch = mismatch + alpha
		if M[i, j] == mismatch:
			print(x[i-1], y[j-1])
			return find_sequence(M, i-1, j-1, x, y, delta, alpha)
		else:
			if M[i,j] == delta + M[i-1, j]:
				return find_sequence(M, i-1, j, x, y, delta, alpha)
			else:
				return find_sequence(M, i, j-1, x, y, delta, alpha)

x = "sapo"
y = "pato"

delta = 0.7
alpha = 1
M = sequence_alignment(x, y, delta, alpha)
print M
find_sequence(M, len(x), len(y), x, y, delta, alpha)