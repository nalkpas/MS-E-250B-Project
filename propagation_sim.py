import numpy as np 
import random
import time
import pdb

# control parameters
graph_flag = True

# load grid data
grid_data = {}
with open('data/grid.txt','r') as file:
	for line in file:
		row = line.strip().split(",")
		grid_data[(int(row[0]), int(row[1]))] = list(map(float, row[2:]))

# 0 means no fire, positive integers for various fire states (currently, just 1 means fire)
squares = list(grid_data.keys())
grid_state = {square:0 for square in squares}

# find grid dimensions
min_height = np.min([int(square[0]) for square in squares])
max_height = np.max([int(square[0]) for square in squares])
min_width = np.min([int(square[1]) for square in squares])
max_width = np.max([int(square[1]) for square in squares])
grid_size = (max_height - min_height + 1) * (max_width - min_width + 1)

# return a list of neighbors for a grid square, accounting for borders
neighbor_offsets  = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]
neighbor_offsets = [np.array(offset) for offset in neighbor_offsets]
def get_neighbors(index):
	neighbors_candidates = [index + offset for offset in neighbor_offsets]
	return [neighbor for neighbor in neighbors_candidates if min_height <= neighbor[0] <= max_height and min_width <= neighbor[1] <= max_width]

# calculate transition probabilities for a grid square
def get_P(index):
	# squares on fire stay on fire for now
	if grid_state[index] == 1:
		return (0,1)

	# otherwise, probability of a fire starting is some fixed probability times the number of neighbors on fire
	neighbors = [tuple(neighbor) for neighbor in get_neighbors(index)]
	states = [grid_state.get(index,0) for index in neighbors]
	fire_sum = np.sum(states)
	p = grid_data[index][0]*fire_sum

	return (1 - p, p)

# calculate damage for a grid square for a time step 
def get_damage(index): 
	# the level of fire times the value of the square times a fixed proportion of damage over a time step
	return grid_state[index] * grid_data[index][1] * 0.0001

# time steps in an epoch
epoch_len = 60

# start some fires, since currently fires can only spread
initial_prop_fires = 0.05
start_fires = random.sample(squares, k=int(np.rint(grid_size * initial_prop_fires)))
grid_state.update(zip(start_fires, [1] * len(start_fires)))

# initialization for the simulation
total_damage = 0
if graph_flag:
	graph = []
start_time = time.time()
print('period\tcalc time\tprop fires\ttotal damage')

# simulate
for t in range(epoch_len):
	new_state = grid_state.copy()
	for square in squares: 
		P = get_P(square)
		new_state[square] = np.random.choice(len(P), p = P)

		damage = get_damage(square)
		total_damage += damage
		grid_data[square][1] -= damage
	grid_state = new_state

	if graph_flag:
		prop_fires = np.sum(list(grid_state.values())) / grid_size
		end_time = time.time()
		print(str(t) + '\t' + str(round(end_time - start_time,3)) + '\t\t' + str(round(prop_fires,3)) + '\t\t' + str(round(total_damage,3)))
		start_time = end_time
		graph.append([t, prop_fires, total_damage])

# graph damage over time
if graph_flag:
	import matplotlib.pyplot as plt
	graph = np.array(graph)
	times = graph[:,0]
	fires = graph[:,1]
	damages = graph[:,2]

	plt.subplot(1,2,1)
	plt.plot(times,fires)
	plt.title('Fire Proliferation Over Time')
	plt.xlabel('time')
	plt.ylabel('percent squares on fire')

	plt.subplot(1,2,2)
	plt.title('Damage Over Time')
	plt.plot(times,damages)
	plt.xlabel('time')
	plt.ylabel('damage')

	plt.show()

