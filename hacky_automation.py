import os

map_names = ['CityGrid_JeffersonCounty_CSV', 'JeffCo_firebreaks']
scenarios = {'CityGrid_JeffersonCounty_CSV': ['InitialValues', 'DefensibleSpace', 'IWUIC', 'Buildings', 'Vegetation'],
			 'JeffCo_firebreaks': ['InitialValues']}

for map_name in map_names:
	for scenario in scenarios[name]:
		os.system('python3 propagation_sim.py ' + scenario + ' ' + map_name)

print('\ndone')