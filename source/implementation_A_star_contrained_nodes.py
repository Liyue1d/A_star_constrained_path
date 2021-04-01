import heapq
import random
import collections
import numpy as np
import math
import time

inf_bound = math.pow(10,29)

def arrayStatetoString(arrayState):
	return "[" + ','.join(list(map(str, arrayState))) + "]"

def stringStatetoArrayState(stringState):
	return list(map(int,stringState.replace("[","").replace("]","").split(",")))

def state_mandatory_nodes(arrayState, number_of_nodes):
	mandatories = []
	for i in range(number_of_nodes):
		if arrayState[i * 3 + 2] == 1:
			mandatories.append(i)

	return mandatories

def state_end_node(arrayState, number_of_nodes):
	for i in range(number_of_nodes):
		if arrayState[i * 3 + 1] == 1:
			return i


def state_departure_node(arrayState, number_of_nodes):
	for i in range(number_of_nodes):
		if arrayState[i * 3] == 1:
			return i

def is_goal_state(arrayState, number_of_nodes):
	dep_arr = False
	no_mandatory = True
	for i in range(number_of_nodes):
		if arrayState[i * 3] == 1:
			if arrayState[i * 3 + 1] == 1:
				dep_arr = True
		if arrayState[i * 3 + 2] == 1:
			no_mandatory = False

	return dep_arr and no_mandatory


class SimpleGraph:
	def __init__(self, adjacency_cost_matrix_with_upper_bound, adjacency_matrix_binary, short):
		self.adjacency_matrix_binary = adjacency_matrix_binary
		self.adjacency_cost_matrix_with_upper_bound = adjacency_cost_matrix_with_upper_bound
		self.short = short
		self.number_of_nodes = adjacency_matrix_binary.shape[0]

	def getShort(self):
		return self.short

	def neighbors(self, arrayState):
		current_node = state_departure_node(arrayState, self.number_of_nodes)
		neighbors = np.where(np.squeeze(np.asarray(self.adjacency_matrix_binary[current_node])) == 1)[0]
		neighbor_list = []

		for neighbor_id in neighbors:
			neighbor_state = list(arrayState)
			neighbor_state[current_node * 3] = 0
			neighbor_state[neighbor_id * 3] = 1
			neighbor_state[neighbor_id * 3 + 2] = 0
			neighbor_list.append(arrayStatetoString(neighbor_state))

		return neighbor_list

	def cost(self, current_state, next_state):
		array_current_state = stringStatetoArrayState(current_state)
		array_next_state = stringStatetoArrayState(next_state)
		dep_node = state_departure_node(array_current_state, self.number_of_nodes)
		arr_node = state_departure_node(array_next_state, self.number_of_nodes)

		return adjacency_cost_matrix_with_upper_bound[dep_node, arr_node]

	def getNumberofNodes(self):
		return self.number_of_nodes




class PriorityQueue:
	def __init__(self):
		self.elements = []

	def randItem(self):
		ind = random.randint(0,len(self.elements))
		element = self.elements[ind]
		del self.elements[ind]
		return element

	def empty(self):
		return len(self.elements) == 0

	def put(self, item, priority):
		heapq.heappush(self.elements, (priority, item))

	def get(self):
		return heapq.heappop(self.elements)[1]



def reconstruct_path(came_from, start, goal, number_of_nodes):

	current = goal
	statePath = []
	nodePath = []

	while current != start:
		statePath.append(current)
		nodePath.append(state_departure_node(stringStatetoArrayState(current), number_of_nodes))
		current = came_from[current]

	statePath.append(start)
	nodePath.append(state_departure_node(stringStatetoArrayState(start), number_of_nodes))

	statePath.reverse()
	nodePath.reverse()

	return [statePath, nodePath]

def heuristic1(str_state):

	return 0

def heuristic2(str_state, g):
	number_of_nodes = g.getNumberofNodes()
	arrayState = stringStatetoArrayState(str_state)
	start = state_departure_node(arrayState, number_of_nodes)
	end = state_end_node(arrayState, number_of_nodes)
	mandatories = state_mandatory_nodes(arrayState, number_of_nodes)
	s_mat = g.getShort()

	if mandatories == []:
		return s_mat[start, end]
	else:


		start_to_mand_min = np.min(s_mat[start,mandatories])
		mand_to_end_min = np.min(s_mat[end,mandatories])

		short_graph = nx.from_numpy_matrix(s_mat)
		short_graph_mand = short_graph.subgraph(mandatories)
		T = nx.minimum_spanning_tree(short_graph_mand)
		mand_length = T.size('weight')
		return start_to_mand_min + mand_length + mand_to_end_min

def a_star_search(graph, start, goal, mandatories, heur):
	number_of_nodes = graph.getNumberofNodes()
	array_start_state = []
	array_goal_state = []
	number_of_visits = 0


	for i in range(number_of_nodes * 3):
		array_start_state.append(0)
		array_goal_state.append(0)

	array_start_state[start * 3] = 1
	array_start_state[goal * 3 + 1] = 1

	for m in mandatories:
		array_start_state[m * 3 + 2] = 1

	array_goal_state[goal * 3] = 1
	array_goal_state[goal * 3 + 1] = 1

	string_start_state = arrayStatetoString(array_start_state)
	string_goal_state = arrayStatetoString(array_goal_state)

	frontier = PriorityQueue()
	frontier.put(string_start_state, 0)
	came_from = {}
	cost_so_far = {}
	came_from[string_start_state] = None
	cost_so_far[string_start_state] = 0

	while not frontier.empty():
		currentStringState = frontier.get()
		number_of_visits += 1

		if currentStringState == string_goal_state:
			break

		currentArrayState = stringStatetoArrayState(currentStringState)


		for next in graph.neighbors(currentArrayState):
			new_cost = cost_so_far[currentStringState] + graph.cost(currentStringState, next)

			if next not in cost_so_far or new_cost < cost_so_far[next]:
				cost_so_far[next] = new_cost
				if heur == 'dijkstra':
					priority = new_cost + heuristic1(next)
				else :
					priority = new_cost + heuristic2(next, graph)
				frontier.put(next, priority)
				came_from[next] = currentStringState

	if string_goal_state not in came_from:
		return False

	return [reconstruct_path(came_from, string_start_state, string_goal_state, number_of_nodes), cost_so_far, cost_so_far[string_goal_state], number_of_visits]

def adj_matrix_creator(adjacency_cost_matrix):
	adjacency_matrix_binary = (adjacency_cost_matrix > 0)
	adjacency_cost_matrix_with_upper_bound = adjacency_cost_matrix + inf_bound * (adjacency_cost_matrix == 0)
	return adjacency_cost_matrix_with_upper_bound, adjacency_matrix_binary
