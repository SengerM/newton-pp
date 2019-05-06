import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation

time = []
crystal = []
particle = []

with open('../simulation_results/2019_05_06_11_06_46/simulation_output.txt') as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	for row in readCSV:
		time.append(row[0])
		crystal_now = []
		for k in range(int((len(row)-1-3)/3)):
			crystal_now.append([float(i) for i in row[1+3*k:1+3*k+3]])
		crystal.append(crystal_now)
		particle.append([float(i) for i in row[-3:]])

fig, ax = plt.subplots()
# ~ for idx, particle_coords in enumerate(crystal[0]):
	# ~ ax.plot(
		# ~ [particle_coords[0]],
		# ~ [particle_coords[1]],
		# ~ marker = '.',
		# ~ color = [idx/len(crystal[0]),0,0]
	# ~ )
# ~ ax.plot(
	# ~ [particle[0][0]],
	# ~ [particle[0][1]],
	# ~ marker = '.',
	# ~ color = [0,0,.6]
# ~ )
ax.axis('equal')
plt.show()
