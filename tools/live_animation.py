import os
import psystems as psys
import matplotlib.pyplot as plt

simulation_number = '2019_05_08_11_25_44'#os.listdir('simulation_results')[-1]

print('Reading data...')
system = psys.crystal_and_particle('../simulation_results/' + simulation_number + '/simulation_output.txt')
print('Data has been loaded')
print('Creating animation...')
animation = psys.animate_system(system)

plt.show()
