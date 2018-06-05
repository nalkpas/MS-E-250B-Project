import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pdb
from PIL import Image

path = 'charts/heatmap_541975/'
image_path = 'charts/jefferson_county.JPG'
fire_length = 12

map_image = Image.open(image_path)
for i in range(fire_length + 1):
	grid_state = np.loadtxt(path + str(i) + '.txt', delimiter=',')
	fig, ax = plt.subplots(figsize=(5, 5))
	sns.heatmap(grid_state, fmt="d", linewidths=.5, ax=ax, vmin=0, vmax=1, cmap='YlOrRd', alpha=0.4, cbar=False, zorder=2)
	ax.imshow(map_image, aspect=ax.get_aspect(), extent=ax.get_xlim() + ax.get_ylim(), zorder = 1)
	fig.savefig(path + "time_" + str(i) + "_heatmap.png")

print('done')