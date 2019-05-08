# ~ This script produces an animation of the last simulation data available.
# ~ The data is processed as if the first "N-1" particles conform a crystal
# ~ and the last particle, the "N-th particle", is a projectile that crashes
# ~ the crystal.

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as mpl_animation
import os
import readers

simulation_number = os.listdir('simulation_results')[-1]

print('Reading data...')
time, particle, crystal = readers.particle_vs_crystal('simulation_results/' + simulation_number + '/simulation_output.txt')
print('Data has been loaded')
print('Plotting...')
particles_x = [p[0] for p in crystal[0]] + [particle[0][0]]
particles_y = [p[1] for p in crystal[0]] + [particle[0][1]]
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

def boundcolor(number):
	if number < 0:
		return 0
	if number > 1:
		return 1
	return number

def update(frame_number):
	particles_x = [p[0] for p in crystal[frame_number]] + [particle[frame_number][0]]
	particles_y = [p[1] for p in crystal[frame_number]] + [particle[frame_number][1]]
	scat.set_offsets([[particles_x[i], particles_y[i]] for i in range(len(particles_x))])
	distance = [((particles_x[i]-crystal[0][i][0])**2 + (particles_y[i]-crystal[0][i][1])**2)**.5 for i in range(len(crystal[0]))]
	new_colors = [
		(
		boundcolor(.3 + 2*distance[i]**.3), # Red
		boundcolor(.3 + 5*distance[i]**.7), # Green
		boundcolor(.8 - distance[i]**.5) # Blue
		)
		for i in range(len(crystal[0]))
		] + [(.7,0,0)] # This is the color of the projectile
	scat.set_color(new_colors)

print('Creating animation...')
animation = FuncAnimation(fig, update, interval=1, save_count=len(time))

print('Saving video file...')
animation.save(
	'simulation_results/' + simulation_number + '/animation.mp4', 
	fps = 30,
	savefig_kwargs = {'facecolor':'black'},
)
