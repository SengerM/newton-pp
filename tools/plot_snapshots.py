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

frame_numbers = []
for k in range(NUMBER_OF_SNAPSHOTS):
	frame_number = int((system.nframes()-1)*float(k)/float(NUMBER_OF_SNAPSHOTS))
	frame_numbers.append(frame_number)
	fig, ax = plt.subplots()
	scat = ax.scatter(
		x = system.get_scatter_x(frame_number),
		y = system.get_scatter_y(frame_number),
		c = system.get_scatter_color(frame_number),
		s = 2
	)
	ax.axis('equal')
	ax.axis('off')
	fig.patch.set_facecolor('black')

print('Plotting finished')

figs = [plt.figure(n) for n in plt.get_fignums()]
if 'snapshots' not in os.listdir('../simulation_results/' + simulation_number):
	os.mkdir('../simulation_results/' + simulation_number + '/snapshots')
for idx,fig in enumerate(figs):
	fig.savefig(
		'../simulation_results/' + simulation_number + '/snapshots/frame_' + str(frame_numbers[idx]) + '.png',
		facecolor = (0,0,0)
	)
