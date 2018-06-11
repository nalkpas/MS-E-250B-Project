import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pdb

map_names = ['main_grid', 'firebreaks']
scenarios = {'main_grid': ['InitialValues', 'DefensibleSpace', 'IWUIC', 'Buildings', 'Vegetation'],
			 'firebreaks': ['InitialValues']}
hist_names = ['damage_hist', 'lives_hist', 'length_hist']
hist_titles = ['Building Damage', 'Number of Deaths', 'Fire Lengths']
hist_axis_labels = ['Building Damage ($)', 'Number of Deaths', 'Fire Length (time steps)']
ylabel = '# episodes'

n = len(hist_names)
hists = []
file_names = []
for map_name in map_names:
	for scenario in scenarios[map_name]:
		hist_set = []
		data_path = path = 'charts/histograms/' + scenario + '_' + map_name
		for hist_name in hist_names:
			with open(data_path + '/' + hist_name + '.txt', 'r') as file:
				hist_set.append(np.array([float(line.strip()) for line in file]))
		hists.append(hist_set)

		file_names.append('charts/' + scenario + '-' + map_name + '_histogram.png')

hist_maxes = [0] * 3
for scenario in hists:
	for i in range(n):
		if np.max(scenario[i]) > hist_maxes[i]:
			hist_maxes[i] = np.max(scenario[i])
hist_maxes = [hist_max * 2/3 for hist_max in hist_maxes]

for scenario, file_name in zip(hists, file_names):
	num_episodes = len(scenario[0])

	fig, axs = plt.subplots(ncols = n)

	print(file_name)
	for i in range(n):
		axs[i] = sns.distplot(a=scenario[i], ax=axs[i], hist=True, kde=False, norm_hist=False, axlabel=hist_axis_labels[i][0])
		axs[i].set_title(hist_titles[i] + ' (' + str(num_episodes) + ' episodes)')
		axs[i].set(ylabel = ylabel)
		axs[i].text(hist_maxes[i]*0.6,num_episodes*0.825,'mean : {0:.3e}\nstdev:  {1:.3e}'.format(np.mean(scenario), np.std(scenario)) ,fontsize=12)
		axs[i].set_xlim(left=0,right=hist_maxes[i])
		axs[i].set_ylim(bottom=0,top=num_episodes)
		print(round(np.mean(scenario[i]),3))

	fig.set_figwidth(20)
	fig.savefig(file_name)