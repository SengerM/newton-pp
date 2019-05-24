from argparse import ArgumentParser
import os
import psystems as psys
import matplotlib.pyplot as plt

parser = ArgumentParser()
parser.add_argument('isimpath', help='directory containing the output data of newton++')

args = parser.parse_args()

system = psys.gas(args.isimpath + '/data.bin')
animation = psys.animate_system(system)

animation.save(
	args.isimpath + '/animation.mp4', 
	fps = 50,
	savefig_kwargs = {'facecolor':'black'},
)
