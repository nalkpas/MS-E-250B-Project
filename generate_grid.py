import numpy as np 

# height and width of grid
height = 100
width = 100

# generate grid properties, eventually from data
def gen_square(i, j):
	return (i,j, np.random.rand() / 8)

# make and save the grid
with open('data/grid.txt','w') as file: 
	for i in range(height): 
		for j in range(width):
			square = gen_square(i, j)
			for prop in square[:-1]: 
				file.write(str(prop) + ",")
			file.write(str(square[-1]) + "\n")

print('done')