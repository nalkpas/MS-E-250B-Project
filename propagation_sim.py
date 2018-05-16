import numpy as np 
import time
import os
import pdb

####################################################################################################																			
# parameters
####################################################################################################

# number of simulations
num_simulations = 1

# whether to make damage histographs
hist_flag = False
# whether to a heatmap series
heatmap_flag = True

# number of simulations

# grid parameters
grid_height = 10
grid_width = 10
grid_path = 'data/grid_' + str(height) + 'x' + str(width) + '.txt'
num_covariates = 4

# small number to handle rounding errors/dividing by zero
eps = 0.0000001

# load grid data
# order of covariates: flammability, utility, population, fuel level 
master_grid_data = np.zeros((grid_height, grid_width, num_covariates))
with open(grid_path,'r') as file:
	for line in file:
		row = line.strip().split(',')
		master_grid_data[int(row[0]), int(row[1])] = np.array(row[2:])

# define what squares wind effects, randomly decide wind direction
wind_lookup = {0: [[-2,0]],
			   1: [[2,0]],
			   2: [[0,2]],
			   3: [[0,-2]]}
wind = np.random.choice(range(4))

####################################################################################################																			
# helper functions
####################################################################################################

# return a list of neighbors for a grid square, accounting for borders
neighbor_offsets  = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]] + wind_lookup[wind]
neighbor_offsets = [np.array(offset) for offset in neighbor_offsets]
def get_neighbors(index):
	neighbors_candidates = [index + offset for offset in neighbor_offsets]
	return [tuple(neighbor) for neighbor in neighbors_candidates if 0 <= neighbor[0] < grid_height and 0 <= neighbor[1] < grid_width]

# find how many nearby squares are on fire
def get_fire_sum(grid_data, grid_state, index):
	neighbors = get_neighbors(index)
	states = [grid_state[index][0] for index in neighbors]
	return np.sum(states)

# choose an initial cell based on the relative flammability of each cell
def get_init_square():
	p = master_grid_data[...,0].reshape(-1,1).flatten()
	p = p / np.sum(p)
	start_index = np.random.choice(range(grid_height*grid_width), p=p)
	return (start_index // grid_width, start_index % grid_width)

####################################################################################################																		
# transition functions
####################################################################################################

# calculate transition probabilities for a grid square
def get_P(grid_data, grid_state, index):
	# the lower the fuel level, the higher the probability that the fire goes out (when fuel = 0, p = 1)
	if grid_state[index][0] == 1:
		p = np.exp(-grid_data[index][3])
		return (p, 1 - p)

	# otherwise, probability of a fire starting is some fixed probability times the number of neighbors on fire
	fire_sum = get_fire_sum(grid_data, grid_state, index)
	p = min(grid_data[index][0]*fire_sum,1)
	return (1 - p, p)

# calculate the probability of getting an alert
def get_p_alert(grid_data, grid_state, index):
	# baseline alert rate + how many nearby squares are on fire
	fire_sum = get_fire_sum(grid_data, grid_state, index)
	return 0.05 + fire_sum / len(neighbor_offsets) * 0.95

# calculate damage for a grid square for a time step 
def get_damage(grid_data, grid_state, index): 
	# a fixed proportion of damage happens each time step
	return (grid_state[index][0] * grid_data[index][1] * 0.05, grid_state[index][0] * grid_data[index][2] * 0.05)

# calculate how many people evacuate
def get_evac(grid_data, grid_state, index):
	# currently uses modified sigmoid function so that a greater proportion of people evacuate over time
	return (2 / (1 + np.exp(-grid_state[index][1])) - 1) * grid_data[index][2]

# calculate how much fuel burns
def get_consumed_fuel(grid_data, grid_state, index):
	# a fixed proportion of fuel burns each time step
	return grid_state[index][0]*grid_data[index][3] * 0.1

####################################################################################################																		
# simulation
####################################################################################################

# initialize graphs
if hist_flag:
	damage_hist = []
	lives_hist = []
	length_hist = []

if heatmap_flag:
	example_fire = np.random.choice(range(num_simulations))
	folder_label = np.random.choice(999999)
	path = 'charts/heatmap_' + str(folder_label)

	if not os.path.exists(path):
		os.makedirs(path)
	else:
		print('bad hash, exiting')
		exit()

# simulation loop
for i in range(num_simulations):
	# initialize environment
	grid_data = master_grid_data.copy()
	# first coordinate is fire status. 0 means no fire, positive integers for various fire states (currently, just 1 means fire)
	# second coordinate is how many time steps the square has been alerted of a fire
	grid_state = np.zeros((grid_height, grid_width, 2), dtype=int)

	# start a fire
	grid_state[get_init_square()] = 1

	# initialize trackers
	start_time = time.time()
	total_building_damage = 0
	total_lives_lost = 0
	fire_lifespan = 0

	if heatmap_flag:
		if i == example_fire:
			np.savetxt(path + '/' + str(fire_lifespan) + '.txt', grid_state[...,0], fmt='%1i' ,delimiter=',')

	# simulate
	while np.sum(grid_state[...,0]) > eps:
		# print(str(fire_lifespan) + ": " + str(np.sum(grid_state[...,0]) / grid_height / grid_width))
		if fire_lifespan > 10000: 
			print('fire never extinguished')
			break

		new_state = grid_state.copy()
		for x in range(grid_height): 
			for y in range(grid_width):
				index = (x,y)

				# update the grid
				P = get_P(grid_data, grid_state, index)
				if np.min(P) < 0:
					pdb.set_trace()
				new_state[index][0] = np.random.choice(len(P), p = P)

				if grid_state[index][1] > 0:
					new_state[index][1] += 1
				elif grid_state[index][0] > 0:
					new_state[index][1] += 1
				else:
					p_alert = get_p_alert(grid_data, grid_state, index)
					new_state[index][1] += np.random.choice(range(2), p = [1 - p_alert, p_alert])

				# calculate damage
				building_damage, lives_lost = get_damage(grid_data, grid_state, index)
				total_building_damage += building_damage
				total_lives_lost += lives_lost

				# calculate how many people have evacuated and how much fuel burns
				people_evacuated = get_evac(grid_data, grid_state, index)
				consumed_fuel = get_consumed_fuel(grid_data, grid_state, index)

				# update grid covariates
				grid_data[index][1] = max(grid_data[index][1] - building_damage, 0)
				grid_data[index][2] = max(grid_data[index][2] - lives_lost - people_evacuated, 0)
				grid_data[index][3] = max(grid_data[index][3] - get_consumed_fuel, 0)
		grid_state = new_state

		fire_lifespan += 1
		if heatmap_flag:
			if i == example_fire:
				np.savetxt(path + '/' + str(fire_lifespan) + '.txt', grid_state[...,0], fmt='%1i' ,delimiter=',')

	if hist_flag:
		damage_hist.append(total_building_damage)
		lives_hist.append(total_lives_lost)
		length_hist.append(fire_lifespan)
	print(str(i) + ': ' + str(time.time() - start_time) + 's')

# create histograms
if hist_flag:
	import matplotlib.pyplot as plt
	import seaborn as sns

	fig, axs = plt.subplots(ncols = 3)

	ax1 = sns.distplot(a=damage_hist, ax = axs[0])
	ax1.set_title('Histogram of Building Damage')
	ax1.set(xlabel = 'Building Damage', ylabel = 'Proportion of Fires')

	ax2 = sns.distplot(a=lives_hist, ax = axs[1])
	ax2.set_title('Histogram of Lives Lost')
	ax2.set(xlabel = 'Lives Lost', ylabel = 'Proportion of Fires')

	ax3 = sns.distplot(a=length_hist, ax = axs[2])
	ax3.set_title('Histogram of Fire Length')
	ax3.set(xlabel = 'Fire Length', ylabel = 'Proportion of Fires')

	fig.set_figwidth(20)
	fig.savefig("histograms_" + str(num_simulations) + "sims.png")
	fig.show()