import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pdb

map_names = ['CityGrid_JeffersonCounty_CSV', 'JeffCo_firebreaks']
scenarios = {'CityGrid_JeffersonCounty_CSV': ['InitialValues', 'DefensibleSpace', 'IWUIC', 'Buildings', 'Vegetation'],
			 'JeffCo_firebreaks': ['InitialValues']}
hist_names = ['damage_hist', 'lives_hist', 'length_hist']
hist_titles = ['Building Damage', '# Deaths', 'Fire Lengths']
hist_axis_labels = [('Building Damage', 'Proportion of Fires'), ('Lives Lost', 'Proportion of Fires'), ('Fire Length', 'Proportion of Fires')]
num_episodes = 500

n = len(hist_names)
hists = []
for map_name in map_names:
	for scenario in scenarios[map_name]:
		data_path = path = 'charts/histograms/' + scenario + '_' + map_name
		for hist_name in hist_names:
			with open(data_path + '/' + hist_name + '.txt', 'r') as file:
				hists.append(np.array([float(line.strip()) for line in file]))

		fig, axs = plt.subplots(ncols = n)

		for i in range(n):
			axs[i] = sns.distplot(a=hists[i], ax=axs[i], hist=True, kde=False, norm_hist=False, axlabel=hist_axis_labels[i][0])
			axs[i].set_title(hist_titles[i] + ' (' + str(num_episodes) + ' episodes)')
			# ax[i].set(xlabel = hist_axis_labels[i][0], ylabel = hist_axis_labels[i][1])
			axs[i].set_xlim(left=0)
			axs[i].set_ylim(bottom=0,top=num_episodes * 3.5/5)

		fig.set_figwidth(20)
		fig.savefig('charts/' + scenario + '-' + map_name + '_histogram.png')