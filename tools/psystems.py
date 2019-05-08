import csv

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
		return (.8,0,0)
	
	def get_scatter_x(self, frame):
		return self.get_crystal_x(frame) + [self.get_particle_x(frame)]
	def get_scatter_y(self, frame):
		return self.get_crystal_y(frame) + [self.get_particle_y(frame)]
	def get_scatter_color(self, frame):
		return self.get_crystal_color(frame) + [self.get_particle_color(frame)]
	
	def nframes(self):
		return len(self.time)
