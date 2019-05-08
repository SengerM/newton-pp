NUMBER_OF_SNAPSHOTS = 4

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as mpl_animation
import os
import psystems as psys
import csv

simulation_number = os.listdir('../simulation_results')
simulation_number.sort()
simulation_number = simulation_number[-1]

print('Counting number of lines in file...')
nlines = 0
with open('../simulation_results/' + simulation_number + '/simulation_output.txt') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	for _ in readCSV:
		nlines += 1
print('Number of lines in file = ' + str(nlines))
useful_rows = []
with open('../simulation_results/' + simulation_number + '/simulation_output.txt') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	frames = []
	for k in range(NUMBER_OF_SNAPSHOTS):
		frames.append(int(float(k)/float(NUMBER_OF_SNAPSHOTS)*nlines))
	for k in range(nlines):
		current_row = next(readCSV)
		if k in frames:
			useful_rows.append(current_row)
	system = psys.crystal_and_particle(useful_rows)

print('Plotting...')
figs, frame_numbers = psys.plot_snapshots(system, 4)

print('Saving...')
if 'snapshots' not in os.listdir('../simulation_results/' + simulation_number):
	os.mkdir('../simulation_results/' + simulation_number + '/snapshots')
for idx,fig in enumerate(figs):
	fig.savefig(
		'../simulation_results/' + simulation_number + '/snapshots/frame_' + str(frames[idx]) + '.png',
		facecolor = (0,0,0)
	)

# ~ print('Reading data...')
# ~ system = psystems.crystal_and_particle('../simulation_results/' + simulation_number + '/simulation_output.txt')
# ~ print('Data has been loaded')
# ~ print('Plotting...')
# ~ figs, frame_numbers = psystems.plot_snapshots(system)
# ~ print('Saving images...')
# ~ if 'snapshots' not in os.listdir('../simulation_results/' + simulation_number):
	# ~ os.mkdir('../simulation_results/' + simulation_number + '/snapshots')
# ~ for idx,fig in enumerate(figs):
	# ~ fig.savefig(
		# ~ '../simulation_results/' + simulation_number + '/snapshots/frame_' + str(frame_numbers[idx]) + '.png',
		# ~ facecolor = (0,0,0)
	# ~ )
