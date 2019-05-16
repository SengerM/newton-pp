import os
import tools.psystems as psys
import matplotlib.pyplot as plt

if 'build' not in os.listdir():
	os.mkdir('build')
if 'simulation_results' not in os.listdir():
	os.mkdir('simulation_results')

os.system('make compile')
os.system('./newton++')

simulation_number = os.listdir('simulation_results')[-1]

print('Reading data...')
system = psys.crystal_and_particle('simulation_results/' + simulation_number + '/simulation_output.txt')
print('Data has been loaded')
print('Creating animation...')
animation = psys.animate_system(system)

plt.show()
