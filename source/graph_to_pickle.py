import pickle
import numpy as np
from numpy import linalg as LA
from scipy.linalg import fractional_matrix_power


def node_degree(x):
	#Returns the node degree matrix corresponding
	# to the input adjacency matrix x
	# Input: x is a numpy matrix
	# Output: nd_x is a numpy matrix
	size = x.shape[0]
	nd_x = np.matrix(np.zeros((size,size)))
	for i in range(size):
		nd_x[i,i] = np.sum(x[i])
	return nd_x


#Adjacency matrix definition
exec(open("./source/graph.py").read())
#print("adj binary =  %s \n", adjacency_matrix_binary)
#print("adj cost =  %s \n", adjacency_cost_matrix_with_upper_bound)
#print("adj weight =  %s \n", adjacency_matrix_weight)


#Number of nodes is stored into variable m_size
m_size = adjacency_matrix_weight.shape[0]

a_chap = adjacency_matrix_weight + np.eye(m_size)
#print("achap = \n", a_chap)

d_chap = node_degree(a_chap)
#print("dchap \n", d_chap)

inv_sq_root_d_chap = np.matrix(fractional_matrix_power(d_chap, -0.5))
#print("inv_sq_root_d_chap =  \n", inv_sq_root_d_chap)
#print("(inv_sq_root_d_chap*inv_sq_root_d_chap)^-1 =  \n", LA.inv(inv_sq_root_d_chap*inv_sq_root_d_chap))

sym_norm = inv_sq_root_d_chap * a_chap * inv_sq_root_d_chap
#print("sym_norm =  \n", sym_norm)


g = SimpleGraph(adjacency_cost_matrix_with_upper_bound, adjacency_matrix_binary, None)

number_of_s = m_size * m_size
count = 0

for i in range(m_size):
	for j in range(m_size):
		shortest_path_matrix[i,j] = a_star_search(g, i, j, [], "dijkstra")[2]
		count += 1

		progress = math.floor(count*100/number_of_s)
		hash = ((60*progress)//100)
		print("[{}{}] {}%".format('#' * hash, ' ' * (60-hash), progress), end="\r")

data = {'binary': adjacency_matrix_binary, 'cost': adjacency_cost_matrix_with_upper_bound, 'weight': adjacency_matrix_weight, 'prod_matrix': sym_norm, 'number_of_nodes': m_size, 'short': shortest_path_matrix}

#Write the data into a pickle file
with open('./model_utils/data.pickle', 'wb') as f:
	# Pickle the 'data' dictionary using the highest protocol available.
	pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
