import csv

def particle_vs_crystal(filename):
	time = []
	crystal = []
	particle = []
	with open(filename) as csvfile:
		readCSV = csv.reader(csvfile, delimiter='\t')
		for row in readCSV:
			time.append(row[0])
			crystal_now = []
			for k in range(int((len(row)-1-3)/3)):
				crystal_now.append([float(i) for i in row[1+3*k:1+3*k+3]])
			crystal.append(crystal_now)
			particle.append([float(i) for i in row[-3:]])
	return time, particle, crystal
