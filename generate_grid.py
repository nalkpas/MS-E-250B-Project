import numpy as np 
import csv
import pdb

scenario = 'InitialValues'
map_path = 'data/CityGrid_JeffersonCounty_CSV.csv'
lookup_path = 'data/cell_lookups/' + scenario + '.csv'


with open(map_path, 'r') as file:
	grid = [line.strip().split(",") for line in file]
grid = np.array(grid, dtype=float)

lookup = {}
with open(lookup_path, 'rU') as file:
	reader = csv.reader(file)
	for line in reader:	
		lookup[float(line[0])] = line[1:]

def read_covariate(covariate):
	if '-' in covariate:
		bottom, top = covariate.split('-')
		return (float(bottom), float(top))
	else:
		return float(covariate)

for key in lookup.keys():
	lookup[key] = map(read_covariate,lookup[key])

# unique_values = np.unique(grid)
# for value in unique_values:
# 	lookup[value] = (np.random.rand() / 12, np.random.rand()*1000, np.random.rand()*100, np.random.rand())

height = len(grid)
width = len(grid[0])
grid_path = 'data/grids/' + scenario + '_grid_' + str(height) + 'x' + str(width) + '.csv'

def process_covariate(covariate):
	if type(covariate) == float:
		return covariate
	elif type(covariate) == tuple:
		bottom, top = covariate
		return bottom + np.random.rand()*(top - bottom)

with open(grid_path, 'w') as file:
	for x in range(height):
		for y in range(width):
			file.write(str(x) + ',' + str(y) + ',')
			covariates = lookup[grid[x][y]]
			for covariate in covariates[:-1]:
				file.write(str(process_covariate(covariate)) + ',')
			file.write(str(process_covariate(covariates[-1])) + '\n')

print('dimensions: ' + str(height) + ' x ' + str(width))