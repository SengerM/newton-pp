import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def boundrange(number, min=0, max=1):
	if number < min:
		return min
	if number > max:
		return max
	return number

class crystal_and_particle:
	"""
	This class is intended to store data of a crystal composed by N particles
	and an individual particle that hits the crystal.
	This is a "psystem" type class.
	"""
	def __init__(self, filename):
		self.time = []
		self.crystal = []
		self.particle = []
		with open(filename) as csvfile:
			readCSV = csv.reader(csvfile, delimiter='\t')
			for row in readCSV:
				self.time.append(row[0])
				crystal_now = []
				for k in range(int((len(row)-1-3)/3)):
					crystal_now.append([float(i) for i in row[1+3*k:1+3*k+3]])
				self.crystal.append(crystal_now)
				self.particle.append([float(i) for i in row[-3:]])
		# ~ data = np.genfromtxt(filename, delimiter='\t').transpose()
		# ~ self.time = data[0]
		# ~ self.particle = np.array([data[-3], data[-2], data[-1]]).transpose()
		# ~ self.crystal = [[data[3*k+1], data[3*k+2], data[3*k+3]] for k in range(int((len(data)-1-3)/3))]
		# ~ print(len(self.crystal[0]))
		
	def get_crystal_x(self, frame):
		return [p[0] for p in self.crystal[frame]]
	def get_crystal_y(self, frame):
		return [p[1] for p in self.crystal[frame]]
	def get_crystal_z(frame):
		return [p[2] for p in self.crystal[frame]]
	
	def get_particle_x(self, frame):
		return self.particle[frame][0]
	def get_particle_y(self, frame):
		return self.particle[frame][1]
	def get_particle_z(self, frame):
		return self.particle[frame][2]
	
	def get_crystal_color(self, frame):
		distance = [((self.get_crystal_x(frame)[i]-self.get_crystal_x(0)[i])**2 + (self.get_crystal_y(frame)[i]-self.get_crystal_y(0)[i])**2)**.5 for i in range(len(self.crystal[0]))]
		new_colors = [
			(
			boundrange(.3 + 2*distance[i]**.3), # Red
			boundrange(.3 + 5*distance[i]**.7), # Green
			boundrange(.8 - distance[i]**.5) # Blue
			)
			for i in range(len(self.crystal[0]))]
		return new_colors
	
	def get_particle_color(self, frame):
		return (1,0,0)
	
	def get_scatter_x(self, frame):
		return self.get_crystal_x(frame) + [self.get_particle_x(frame)]
	def get_scatter_y(self, frame):
		return self.get_crystal_y(frame) + [self.get_particle_y(frame)]
	def get_scatter_color(self, frame):
		return self.get_crystal_color(frame) + [self.get_particle_color(frame)]
	
	def nframes(self):
		return len(self.time)
		
class gas:
	"""
	This class is intended to store data of a gas composed by N particles.
	This is a "psystem" type class.
	"""
	def __init__(self, filename):
		self.time = []
		self.gas = []
		with open(filename) as csvfile:
			readCSV = csv.reader(csvfile, delimiter='\t')
			for row in readCSV:
				self.time.append(row[0])
				gas_now = []
				for k in range(int((len(row)-1)/3)):
					gas_now.append([float(i) for i in row[1+3*k:1+3*k+3]])
				self.gas.append(gas_now)
		
	def get_gas_x(self, frame):
		return [p[0] for p in self.gas[frame]]
	def get_gas_y(self, frame):
		return [p[1] for p in self.gas[frame]]
	def get_gas_z(frame):
		return [p[2] for p in self.gas[frame]]
	
	def get_gas_color(self, frame):
		return (1,1,1)
	
	def get_scatter_x(self, frame):
		return self.get_gas_x(frame)
	def get_scatter_y(self, frame):
		return self.get_gas_y(frame)
	def get_scatter_color(self, frame):
		return self.get_gas_color(frame)
	
	def nframes(self):
		return len(self.time)

def animate_system(psystem):
	"""
	This function receives a "psystem" type object and returns an animation.
	"""
	fig, ax = plt.subplots()
	scat = ax.scatter(
		x = psystem.get_scatter_x(0),
		y = psystem.get_scatter_y(0),
		c = psystem.get_scatter_color(0),
		s = 2
	)
	ax.axis('equal')
	ax.axis('off')
	fig.patch.set_facecolor('black')
	ax.set_xlim(-.5, .5)
	ax.set_ylim(-.5, .5)
	
	def update(frame_number):
		scat.set_offsets([[psystem.get_scatter_x(frame_number)[i], psystem.get_scatter_y(frame_number)[i]] for i in range(len(psystem.get_scatter_x(frame_number)))])
		scat.set_color(psystem.get_scatter_color(frame_number))
	
	animation = FuncAnimation(fig, update, interval=1, save_count=psystem.nframes())
	return animation, ax

def plot_snapshot(psystem, frame):
	fig, ax = plt.subplots()
	scat = ax.scatter(
		x = psystem.get_scatter_x(frame),
		y = psystem.get_scatter_y(frame),
		c = psystem.get_scatter_color(frame),
		s = 2
	)
	ax.axis('equal')
	ax.axis('off')
	fig.patch.set_facecolor('black')
	return fig, ax

def plot_snapshots(psystem, n_snapshots=4):
	"""
	This functions plots snapshots and return the figures.
	"""
	frame_numbers = []
	figs = []
	for k in range(n_snapshots):
		frame_number = int((psystem.nframes()-1)*float(k)/float(n_snapshots))
		frame_numbers.append(frame_number)
		fig, ax = plot_snapshot(psystem, frame_number)
		figs.append(fig)
	return figs, frame_numbers
