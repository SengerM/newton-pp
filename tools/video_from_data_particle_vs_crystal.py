# ~ This script produces an animation of the last simulation data available.
# ~ The data is processed as if the first "N-1" particles conform a crystal
# ~ and the last particle, the "N-th particle", is a projectile that crashes
# ~ the crystal.

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as mpl_animation
import os
import psystems

simulation_number = os.listdir('../simulation_results')[-1]

print('Reading data...')
system = psystems.crystal_and_particle('../simulation_results/' + simulation_number + '/simulation_output.txt')
print('Data has been loaded')
print('Plotting...')
fig, ax = plt.subplots()
scat = ax.scatter(
	x = system.get_scatter_x(0),
	y = system.get_scatter_y(0),
	c = system.get_scatter_color(0),
	s = 2
)
ax.axis('equal')
ax.axis('off')
fig.patch.set_facecolor('black')
print('Plotting finished')

def boundcolor(number):
	if number < 0:
		return 0
	if number > 1:
		return 1
	return number

def update(frame_number):
	scat.set_offsets([[system.get_scatter_x(frame_number)[i], system.get_scatter_y(frame_number)[i]] for i in range(len(system.get_scatter_x(frame_number)))])
	scat.set_color(system.get_scatter_color(frame_number))

print('Creating animation...')
animation = FuncAnimation(fig, update, interval=1, save_count=system.nframes())

print('Saving video file...')
animation.save(
	'../simulation_results/' + simulation_number + '/animation.mp4', 
	fps = 30,
	savefig_kwargs = {'facecolor':'black'},
)
