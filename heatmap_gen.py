import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pdb

path = 'charts/heatmap_541975/'
fire_length = 12

for i in range(fire_length + 1):
	grid_state = np.loadtxt(path + str(i) + '.txt', delimiter=',')
	fig, ax = plt.subplots(figsize=(6, 5))
	sns.heatmap(grid_state, fmt="d", linewidths=.5, ax=ax, vmin=0, vmax=1, cmap="GnBu")
	fig.savefig(path + "time_" + str(i) + "_heatmap.png")

print('done')