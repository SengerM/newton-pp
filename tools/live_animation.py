import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import psystems

simulation_number = '2019_05_08_11_25_44'#os.listdir('simulation_results')[-1]

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

plt.show()
