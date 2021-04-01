import numpy as np
import pickle
import networkx as nx

# Hyperparameters
exec(open("./implementation_A_star_contrained_nodes.py").read())


# Load the graph data
with open('../model_utils/data.pickle', 'rb') as f:
    data = pickle.load(f)

# Store graph data into variables
adjacency_cost_matrix_with_upper_bound = data.get('cost')
adjacency_matrix_weight = data.get('weight')
adjacency_matrix_binary = data.get('binary')
shortest_path_matrix = data.get('short')


number_of_nodes = data.get('number_of_nodes')
number_of_features_per_node = 3

g = SimpleGraph(adjacency_cost_matrix_with_upper_bound, adjacency_matrix_binary, shortest_path_matrix)



start = 11
goal = 15
mandatories = [0,1,2,3,4,5,6,7,8,9,10,12,13,14,16,17]

start_time = time.time()


result = a_star_search(g, start, goal, mandatories, "dijkstra")

if result != False:
	[path, cost, total_cost, num] = result
	print("\n The optimal path is: %s"%path[1])
	print("\n The cost is: %f"%total_cost)
	print("\n Number of visits: %f"%num)
	print("--- %s seconds ---" % (time.time() - start_time))

else:
	print("\n No path found")
