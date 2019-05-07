import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

time = []
crystal = []
particle = []

with open('../simulation_results/2019_05_06_17_55_58/simulation_output.txt') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	for row in readCSV:
		time.append(row[0])
		crystal_now = []
		for k in range(int((len(row)-1-3)/3)):
			crystal_now.append([float(i) for i in row[1+3*k:1+3*k+3]])
		crystal.append(crystal_now)
		particle.append([float(i) for i in row[-3:]])

# ~ PLOT_TIME = 20
# ~ fig, ax = plt.subplots()
# ~ for idx, particle_coords in enumerate(crystal[PLOT_TIME]):
	# ~ ax.plot(
		# ~ [particle_coords[0]],
		# ~ [particle_coords[1]],
		# ~ marker = '.',
		# ~ color = [idx/len(crystal[PLOT_TIME]),0,0]
	# ~ )
# ~ ax.plot(
	# ~ [particle[PLOT_TIME][0]],
	# ~ [particle[PLOT_TIME][1]],
	# ~ marker = '.',
	# ~ color = [0,0,.6]
# ~ )
particles_x = [p[0] for p in crystal[0]]
particles_x.append(particle[0][0])
particles_y = [p[1] for p in crystal[0]]
particles_y.append(particle[0][1])
fig, ax = plt.subplots()
scat = ax.scatter(
	x = particles_x,
	y = particles_y,
	c = [(0,0,0)]*len(crystal[0]) + [(.7,0,0)]
)
ax.axis('equal')

def update(frame_number):
	particles_x = [p[0] for p in crystal[frame_number]]
	particles_x.append(particle[frame_number][0])
	particles_y = [p[1] for p in crystal[frame_number]]
	particles_y.append(particle[frame_number][1])
	scat.set_offsets([[particles_x[i], particles_y[i]] for i in range(len(particles_x))])
	

animation = FuncAnimation(fig, update, interval=1)
plt.show()
