import numpy as np 
import random
import time
import pdb

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
height = np.max([int(square[0]) for square in squares])
width = np.max([int(square[1]) for square in squares])

# return a list of neighbors for a grid square, accounting for borders
neighbor_offsets  = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]
neighbor_offsets = [np.array(offset) for offset in neighbor_offsets]
def get_neighbors(index):
	neighbors_candidates = [index + offset for offset in neighbor_offsets]
	return [neighbor for neighbor in neighbors_candidates if 0 <= neighbor[0] <= height and 0 <= neighbor[1] <= width]

# calculate transition probabilities for a grid square
def get_P(index):
	# squares on fire stay on fire for now
	if grid_state[index] == 1:
		return (0,1)

	# otherwise, probability of a fire starting is some fixed probability times the number of neighbors on fire
	neighbors = [tuple(neighbor) for neighbor in get_neighbors(index)]
	states = [grid_state[index] for index in neighbors]
	fire_sum = np.sum(states)
	p = grid_data[index][0]*fire_sum

	return (1 - p, p)

# time steps in an epoch
epoch_len = 10

# start some fires, since currently fires can only spread
initial_percent_fires = 0.05
start_fires = random.sample(squares, k=int(np.rint((height + 1) * (width + 1) * initial_percent_fires)))
grid_state.update(zip(start_fires, [1] * len(start_fires)))

# simulate
start_time = time.time()
for _ in range(epoch_len):
	new_state = grid_state.copy()
	for square in squares: 
		P = get_P(square)
		new_state[square] = np.random.choice(len(P), p = P)
	grid_state = new_state
	print(time.time() - start_time)

# print % of squares on fire as a sanity check
percent_fires = np.sum(list(grid_state.values())) / (height + 1) / (width + 1)
print(percent_fires)

