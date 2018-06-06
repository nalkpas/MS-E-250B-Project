import numpy as np

values_of_life = [5,10]
wildfire_rate = 2
costs = {'main_grid':0, 'firebreaks':10, 'InitialValues':0, 'DefensibleSpace':5, 'IWUIC':10, 'Buildings':5, 'Vegetation':5}

map_names = ['main_grid', 'firebreaks']
scenarios = {'main_grid': ['InitialValues', 'DefensibleSpace', 'IWUIC', 'Buildings', 'Vegetation'],
			 'firebreaks': ['InitialValues']}
file_names = ['damage_hist', 'lives_hist', 'length_hist']

data = {}
for map_name in map_names:
	for scenario in scenarios[map_name]:
		data_set = []
		data_path = path = 'charts/histograms/' + scenario + '_' + map_name
		for file_name in file_names:
			with open(data_path + '/' + file_name + '.txt', 'r') as file:
				data_set.append(np.array([float(line.strip()) for line in file]))
		data[(scenario, map_name)] = data_set

outputs = []
for value_of_life in values_of_life:
	for instance in data.keys():
		scenario, map_name = instance
		avg_damage = np.mean(data[instance][0])
		avg_deaths = np.mean(data[instance][1])

		total_damages = avg_damage + avg_deaths * value_of_life
		instance_cost = costs[scenario] + costs[map_name]

		if total_damages > instance_cost:
			result = 'do'
		else: 
			result = 'don\'t'
		output = scenario + '_' + map_name + ': \t' + result + '\tcost: ' + str(instance_cost) + '\tdamages: ' + str(total_damages)

		print(output)
		outputs.append(output)

with open('charts/policy_analysis.txt','w') as file:
	for output in outputs:
		file.write(output)
		file.write('\n')