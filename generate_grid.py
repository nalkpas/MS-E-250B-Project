import numpy as np 
import pdb

grid = []
with open('data/CityGrid_JeffersonCounty_CSV.csv', 'r') as file:
	for line in file:
		grid.append(line.strip().split(","))
grid = np.array(grid, dtype=float)

lookup = {}

unique_values = np.unique(grid)
for value in unique_values:
	lookup[value] = (np.random.rand() / 12, np.random.rand()*1000, np.random.rand()*100, np.random.rand())

height = len(grid)
width = len(grid[0])

with open('data/test_grid.txt', 'w') as file:
	for x in range(height):
		for y in range(width):
			file.write(str(x) + ',' + str(y) + ',')
			covariates = lookup[grid[x][y]]
			for covariate in covariates[:-1]:
				file.write(str(covariate) + ',')
			file.write(str(covariates[-1]) + '\n')

print('dimensions: ' + str(height) + ' x ' + str(width))