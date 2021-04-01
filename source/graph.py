import csv
import numpy as np
import sys
inf_bound = sys.float_info.max

csvfile = open('input/graph.csv')
reader = csv.reader(csvfile)


number_of_nodes = int(next(reader)[0])

adjacency_matrix_binary = np.zeros([number_of_nodes, number_of_nodes])
adjacency_cost_matrix_with_upper_bound = np.zeros([number_of_nodes, number_of_nodes])
adjacency_matrix_weight = np.zeros([number_of_nodes, number_of_nodes])
shortest_path_matrix = np.zeros([number_of_nodes, number_of_nodes])

for row in reader:
    i = int(row[0])
    j = int(row[1])
    cost = float(row[2])
    #print("i = %d \n"%i)
    #print("j = %d \n"%j)
    #print("cost = %f \n"%cost)
    adjacency_matrix_binary[i,j] = 1
    adjacency_cost_matrix_with_upper_bound[i,j] = cost
    adjacency_matrix_weight[i,j] = cost


adjacency_cost_matrix_with_upper_bound = (adjacency_matrix_binary == 0) * inf_bound + adjacency_cost_matrix_with_upper_bound

#print(adjacency_matrix_binary)
#print(adjacency_cost_matrix_with_upper_bound)
#print(adjacency_matrix_weight)
