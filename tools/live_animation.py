from argparse import ArgumentParser
import os
import psystems as psys
import matplotlib.pyplot as plt

parser = ArgumentParser()
parser.add_argument('isimpath', help='directory containing the output data of newton++')

args = parser.parse_args()

print('Reading data...')
system = psys.crystal_and_particle(args.isimpath + '/simulation_output.txt')
print('Data has been loaded')
print('Creating animation...')
animation = psys.animate_system(system)

plt.show()
