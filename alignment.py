# authors: Daniel Gribel, Joao Paulo Forny

import numpy as np
import random
import time
import copy

start_time = time.time()

def init_memory_quad(m, n, delta):
	M = np.zeros((m, n))
	for i in range(0, m):
		M[i, 0] = i*delta
	for j in range(0, n):
		M[0, j] = j*delta

	return M

def init_memory_linear(m, delta):
	current = [0 for i in range(m)]
	for i in range(0, m):
		current[i] = i*delta

	return current

# get cost in quadratic space: O(n^2) time, O(n^2) space
def get_cost_quad(x, y, delta, alpha):
	m = len(x)
	n = len(y)

	M = init_memory_quad(m+1, n+1, delta)
	
	for i in range(1, m+1):
		for j in range(1, n+1):
			mismatch = M[i-1, j-1]
			if x[i-1] != y[j-1]:
				mismatch = mismatch + alpha
			
			M[i, j] = min(mismatch, delta + M[i-1, j], delta + M[i, j-1])
	
	return M

# get cost in linear space: O(n^2) time, O(2n) space
def get_cost_linear(x, y, delta, alpha):
	m = len(x)
	n = len(y)

	current = init_memory_linear(m+1, delta)

	for j in range(1, n+1):
		last = copy.copy(current)
		current[0] = j*delta
		for i in range(1, m+1):
			mismatch = last[i-1]
			if x[i-1] != y[j-1]:
				mismatch = mismatch + alpha
			current[i] = min(mismatch, delta + last[i], delta + current[i-1])

	return current

# find sequence for quadratic storage: O(2n) time, O(n^2) space
def find_sequence_iterative(M, x, y, delta, alpha):
	i = len(x)
	j = len(y)
	
	while(i != 0 and j != 0):
		mismatch = M[i-1, j-1]
		if x[i-1] != y[j-1]:
			mismatch = mismatch + alpha
		if M[i, j] == mismatch:
			i = i-1
			j = j-1
			alignment.append( (x[i], y[j]) )
		else:
			if M[i,j] == delta + M[i-1, j]:
				i = i-1
			else:
				j = j-1

# find sequence for linear storage
def divide_conquer_alignment(x, y, delta, alpha):
	m = len(x)
	n = len(y)
	
	if m <= 2 or n <= 2:
		M = get_cost_quad(x, y, delta, alpha)
		return find_sequence_iterative(M, x, y, delta, alpha)

	else:
		f_alignment = get_cost_linear(x, y[:(n/2)], delta, alpha)
		b_alignment = get_cost_linear(x[::-1], y[(n/2):][::-1], delta, alpha)
		
		sum_alignments = [a + b for a, b in zip(f_alignment, b_alignment[::-1])]
		q = sum_alignments.index(min(sum_alignments))

		divide_conquer_alignment(x[:q], y[:(n/2)], delta, alpha)
		divide_conquer_alignment(x[q:], y[(n/2):], delta, alpha)


delta = 0.7
alpha = 1
alphabet = "abcd"

# x = "mean"
# y = "name"

# alignment = list()
# M1 = get_cost_linear(x, y, delta, alpha)
# divide_conquer_alignment(x, y, delta, alpha)
# print 'alignment cost:', M1[len(x)]
# print alignment

# print '---------------------'

# alignment = list()
# M2 = get_cost_quad(x, y, delta, alpha)
# find_sequence_iterative(M2, x, y, delta, alpha)
# print 'alignment cost:', M2[len(x), len(y)]
# print alignment

mean_times_linear = list()
mean_times_quad = list()
length_list = list()

# genarating multiple instances
for i in range(0, 11):
	
	times_linear = list()
	times_quad = list()

	for j in range(0, 10):

		string_length = 10 * pow(2, i+1)

		x = [random.choice(alphabet) for _ in range(string_length)]
		y = [random.choice(alphabet) for _ in range(string_length)]
		
		# linear storage
		alignment = list()
		st_linear = time.time()
		M1 = get_cost_linear(x, y, delta, alpha)
		divide_conquer_alignment(x, y, delta, alpha)
		times_linear.append(time.time() - st_linear)

		# quadratic storage
		alignment = list()
		st_quad = time.time()
		M2 = get_cost_quad(x, y, delta, alpha)
		find_sequence_iterative(M2, x, y, delta, alpha)
		times_quad.append(time.time() - st_quad)

		if M1[len(x)] != M2[len(x), len(y)]:
			print 'error: costs are different'

		del M1
		del M2
		del alignment

	print 'i =', i+1, sum(times_linear)/len(times_linear), sum(times_quad)/len(times_quad), (time.time() - start_time)
	
	mean_times_linear.append(sum(times_linear)/len(times_linear))
	mean_times_quad.append(sum(times_quad)/len(times_quad))
	length_list.append(string_length)

	del times_linear
	del times_quad

print mean_times_linear, mean_times_quad, length_list