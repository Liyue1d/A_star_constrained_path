import numpy as np
import pickle
import networkx as nx
import os



# Hyperparameters
exec(open("./source/implementation_A_star_contrained_nodes.py").read())

while True:
	os.system('clear')
	print("############### Constrained Shortest Path Computer  ############### \n ")
	print("Enter a number among the following choices: \n ")
	print("1- Update the graph\n ")
	print("2- Compute a shortest path with mandatory nodes\n ")
	print("3- Quit\n ")
	c = input()

	if (c == '1'):
		os.system('clear')
		print("Update the graph.csv file in the input folder. \n\nThe first line of the csv file should be the number of nodes in the graph. \nFollowing lines are edges and their weight. \n\nThe lines should look like this: i,j,c if node (i,j) has a cost c. An example file exampleGraph.csv is given in the input folder. \n\nPress enter when finished. \n ")
		input()


		try:
			exec(open("./source/graph_to_pickle.py").read())

			print("\nPress enter to continue. \n")


		except IndexError:
			print("\nA The input graph is not correctly parsed. \nPress enter to continue. \n")
		except FileNotFoundError:
			print("\nFile graph.csv not found in folder input. Press enter to continue. \n")

		input()

	elif (c == '2'):
		os.system('clear')
		try:
			with open('./model_utils/data.pickle', 'rb') as f:
				data = pickle.load(f)

				# Store graph data into variables
				adjacency_cost_matrix_with_upper_bound = data.get('cost')
				adjacency_matrix_weight = data.get('weight')
				adjacency_matrix_binary = data.get('binary')
				shortest_path_matrix = data.get('short')
				number_of_nodes = data.get('number_of_nodes')
				number_of_features_per_node = 3
				g = SimpleGraph(adjacency_cost_matrix_with_upper_bound, adjacency_matrix_binary, shortest_path_matrix)


				start = int(input("Please enter the start node: \n"))
				goal = int(input("\nPlease enter the end node: \n"))
				mandatories = input("\nPlease enter the mandatory nodes separated by commas. \nExample: Enter 1,5,8 if nodes 1,5 and 8 are mandatory nodes.\n")

				mandatories = list(map(int,mandatories.split(",")))


				start_time = time.time()
				result = a_star_search(g, start, goal, mandatories, "mt")
				comp_time = float(time.time() - start_time)
				if result != False:
					[path, cost, total_cost, num] = result
					print("\n\nThe optimal path is: %s"%path[1])
					print("The cost of the path is: %.2f"%total_cost)
					print("\n\nComputation statistics:")
					print("\nNumber of nodes visited: %d"%num)
					print("Computation time: %f" %comp_time)
					print("\nPress enter to continue. \n")

				else:
					print("\n No path found")

		except ValueError:
			print("\nInvalid number. Press enter to continue. \n")
		except IndexError:
			print("\nA node that does not belong to the graph has been entered. \nPress enter to continue. \n")
		except FileNotFoundError:
			print("\nNo graph found. Please update the graph first. Press enter to continue. \n")



		input()

	elif (c == '3'):
		os.system('clear')
		break

	else :


		os.system('clear')
		print("\n Invalid command. Press enter to continue. \n")
		input()
