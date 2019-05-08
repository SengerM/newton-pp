NUMBER_OF_SNAPSHOTS = 4

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as mpl_animation
import os
import psystems

simulation_number = '2019_05_08_11_25_44'#os.listdir('simulation_results')[-1]

print('Reading data...')
system = psystems.crystal_and_particle('../simulation_results/' + simulation_number + '/simulation_output.txt')
print('Data has been loaded')
print('Plotting...')
figs, frame_numbers = psystems.plot_snapshots(system)
print('Saving images...')
if 'snapshots' not in os.listdir('../simulation_results/' + simulation_number):
	os.mkdir('../simulation_results/' + simulation_number + '/snapshots')
for idx,fig in enumerate(figs):
	fig.savefig(
		'../simulation_results/' + simulation_number + '/snapshots/frame_' + str(frame_numbers[idx]) + '.png',
		facecolor = (0,0,0)
	)
