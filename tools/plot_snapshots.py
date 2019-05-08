NUMBER_OF_SNAPSHOTS = 4

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as mpl_animation
import os
import readers

simulation_number = '2019_05_08_11_59_45'#os.listdir('simulation_results')[-1]

print('Reading data...')
time, particle, crystal = readers.particle_vs_crystal('../simulation_results/' + simulation_number + '/simulation_output.txt')
print('Data has been loaded')
print('Plotting...')

frame_numbers = []
for k in range(NUMBER_OF_SNAPSHOTS):
	frame_number = int((len(time)-1)*float(k)/float(NUMBER_OF_SNAPSHOTS))
	frame_numbers.append(frame_number)
	particles_x = [p[0] for p in crystal[frame_number]] + [particle[frame_number][0]]
	particles_y = [p[1] for p in crystal[frame_number]] + [particle[frame_number][1]]
	fig, ax = plt.subplots()
	scat = ax.scatter(
		x = particles_x,
		y = particles_y,
		c = [(.3,.3,.8)]*len(crystal[0]) + [(.7,0,0)],
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
