import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pdb

map_names = ['CityGrid_JeffersonCounty_CSV', 'JeffCo_firebreaks']
scenarios = {'CityGrid_JeffersonCounty_CSV': ['InitialValues', 'DefensibleSpace', 'IWUIC', 'Buildings', 'Vegetation'],
			 'JeffCo_firebreaks': ['InitialValues']}

for map_name in map_names:
	for scenario in scenarios[map_name]:
		data_path = path = 'charts/histograms/' + scenario + '_' + map_name
		with open(data_path + '/damage_hist.txt', 'r') as file:
			damage_hist = np.array([float(line.strip()) for line in file])
		with open(data_path + '/lives_hist.txt', 'r') as file:
			lives_hist = np.array([float(line.strip()) for line in file])
		with open(data_path + '/length_hist.txt', 'r') as file:
			length_hist = np.array([float(line.strip()) for line in file])

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

		for ax in axs:
			ax.set_xlim(left=0)

		fig.set_figwidth(20)
		fig.savefig('charts/' + scenario + '-' + map_name + '_histogram.png')