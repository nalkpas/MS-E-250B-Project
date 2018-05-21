import numpy as np 

# height and width of grid
height = 100
width = 100
grid_path = 'data/grids/random_grid_' + str(height) + 'x' + str(width) + '.csv'

# generate grid properties, eventually from data
def gen_square(i, j):
	# we currently randomly assign each grid square a "flammability", "utility", "population", and "fuel level"
	return (i,j, (0.5 + np.random.rand()/2) / 8, np.random.rand()*1000, np.random.rand()*100, 0.5 + np.random.rand()/2)

# make and save the grid
with open(grid_path,'w') as file: 
	for i in range(height): 
		for j in range(width):
			square = gen_square(i, j)
			for prop in square[:-1]: 
				file.write(str(prop) + ',')
			file.write(str(square[-1]) + '\n')

print('done')