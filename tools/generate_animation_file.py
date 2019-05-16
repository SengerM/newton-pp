from argparse import ArgumentParser
import os
import psystems as psys
import matplotlib.pyplot as plt

parser = ArgumentParser()
parser.add_argument('isimpath', help='directory containing the output data of newton++')

args = parser.parse_args()

system = psys.crystal_and_particle(args.isimpath + '/simulation_output.txt')
animation = psys.animate_system(system)

animation.save(
	args.isimpath + '/animation.mp4', 
	fps = 30,
	savefig_kwargs = {'facecolor':'black'},
)
