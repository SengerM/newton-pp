import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as mpl_animation

time = []
crystal = []
particle = []

SIMULATIONS = [
	'2019_05_06_17_55_58',
	'2019_05_07_18_33_26',
	'2019_05_07_18_36_29',
	'2019_05_07_18_59_35',
]

SIMULATION_TO_ANIMATE = 1

with open('../simulation_results/' + SIMULATIONS[SIMULATION_TO_ANIMATE] + '/simulation_output.txt') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	for row in readCSV:
		time.append(row[0])
		crystal_now = []
		for k in range(int((len(row)-1-3)/3)):
			crystal_now.append([float(i) for i in row[1+3*k:1+3*k+3]])
		crystal.append(crystal_now)
		particle.append([float(i) for i in row[-3:]])

particles_x = [p[0] for p in crystal[0]]
particles_x.append(particle[0][0])
particles_y = [p[1] for p in crystal[0]]
particles_y.append(particle[0][1])
fig, ax = plt.subplots()
scat = ax.scatter(
	x = particles_x,
	y = particles_y,
	c = [(.3,.3,.3)]*len(crystal[0]) + [(.7,0,0)],
	s = 5
)
ax.axis('equal')
ax.axis('off')
fig.patch.set_facecolor('black')

def cutinone(number):
	return number if number<1 else 1

def update(frame_number):
	particles_x = [p[0] for p in crystal[frame_number]]
	particles_x.append(particle[frame_number][0])
	particles_y = [p[1] for p in crystal[frame_number]]
	particles_y.append(particle[frame_number][1])
	scat.set_offsets([[particles_x[i], particles_y[i]] for i in range(len(particles_x))])
	distancia_en_crystal = [((particles_x[i]-crystal[0][i][0])**2 + (particles_y[i]-crystal[0][i][1])**2)**.3 for i in range(len(crystal[0]))]
	scat.set_color([(cutinone(.3+2*distancia_en_crystal[i]),cutinone(.3+2*distancia_en_crystal[i]),.3) for i in range(len(crystal[0]))] + [(.7,0,0)])
	

animation = FuncAnimation(fig, update, interval=1, save_count=len(time))
Writer = mpl_animation.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=1800)
animation.save(SIMULATIONS[SIMULATION_TO_ANIMATE] + '.mp4', writer=writer, savefig_kwargs={'facecolor':'black'})
# ~ plt.show()
