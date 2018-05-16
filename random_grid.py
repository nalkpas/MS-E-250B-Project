import numpy as np 

# height and width of grid
height = 100
width = 100

# generate grid properties, eventually from data
def gen_square(i, j):
	# we currently randomly assign each grid square a "flammability", "utility", "population", and "fuel level"
	return (i,j, np.random.rand() / 12, np.random.rand()*1000, np.random.rand()*100, np.random.rand())

# make and save the grid
with open('data/grid.txt','w') as file: 
	for i in range(height): 
		for j in range(width):
			square = gen_square(i, j)
			for prop in square[:-1]: 
				file.write(str(prop) + ',')
			file.write(str(square[-1]) + '\n')

print('done')