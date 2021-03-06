import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import sys

current_path = sys.path[0]
if current_path.split('/')[-1] != 'tools':
	sys.path.insert(0, current_path+'/tools/')
	from . import zoomtools
else:
	import zoomtools

def boundrange(number, min=0, max=1):
	if number < min:
		return min
	if number > max:
		return max
	return number

class nppreader:
	def __init__(self, file):
		self.file = file
		self.time = None
		self.particles = None
	
	def read_binary(self, filename):
		data = np.fromfile(filename, dtype = '<f4')
		nparticles = int(data[0])
		data = data[1:]
		time = []
		particles = []
		for frame in range(int(len(data)/(3*nparticles+1))):
			time.append(data[frame*(3*nparticles+1)])
			particles.append([None]*nparticles)
			for l in range(nparticles):
				particles[frame][l] = data[frame*(3*nparticles+1)+1+l*3 : frame*(3*nparticles+1)+1+l*3+3+1]
		return time, particles

	def read_csv(self, filename):
		time = []
		particles = []
		with open(filename) as csvfile:
			readCSV = csv.reader(csvfile, delimiter='\t')
			for row in readCSV:
				time.append(row[0])
				particlesnow = []
				for k in range(int((len(row)-1)/3)):
					particlesnow.append([float(i) for i in row[1+3*k:1+3*k+3]])
				particles.append(particlesnow)
		return time, particles
	
	def read(self):
		if self.file[-3:] == 'csv':
			self.time, self.particles = self.read_csv(self.file)
		elif self.file[-3:] == 'bin':
			self.time, self.particles = self.read_binary(self.file)
		else:
			raise ValueError('Dont know how to read a file of type "' + filename[-4:] + '"')
	
	def get_time(self):
		if self.time == None:
			self.read()
		return self.time
	
	def get_particles(self):
		if self.time == None:
			self.read()
		return self.particles
	

class crystal_and_particle:
	"""
	This class is intended to store data of a crystal composed by N particles
	and an individual particle that hits the crystal.
	This is a "psystem" type class.
	"""
	def __init__(self, filename):
		reader = nppreader(filename)
		self.time = reader.get_time()
		self.crystal = [all_particles[:-1] for all_particles in reader.get_particles()]
		self.particle = [all_particles[-1] for all_particles in reader.get_particles()]
		
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
		reader = nppreader(filename)
		self.time = reader.get_time()
		self.gas = reader.get_particles()
		
	def get_gas_x(self, frame):
		return [p[0] for p in self.gas[frame]]
	def get_gas_y(self, frame):
		return [p[1] for p in self.gas[frame]]
	def get_gas_z(frame):
		return [p[2] for p in self.gas[frame]]
	
	def get_gas_color(self, frame):
		return 'w'
	
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
	# ~ ax.set_xlim(-.5, .5)
	# ~ ax.set_ylim(-.5, .5)
	
	zp = zoomtools.ZoomPan()
	figZoom = zp.zoom_factory(ax, base_scale = 1.5)
	figPan = zp.pan_factory(ax)
	
	def update(frame_number):
		scat.set_offsets([[psystem.get_scatter_x(frame_number)[i], psystem.get_scatter_y(frame_number)[i]] for i in range(len(psystem.get_scatter_x(frame_number)))])
		scat.set_color(psystem.get_scatter_color(frame_number))
	
	animation = FuncAnimation(fig, update, interval=1, save_count=psystem.nframes())
	return animation

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
