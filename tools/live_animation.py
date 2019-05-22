from argparse import ArgumentParser
import os
import psystems as psys
import matplotlib.pyplot as plt
from zoomtools import ZoomPan

parser = ArgumentParser()
parser.add_argument('isimpath', help='directory containing the output data of newton++')

args = parser.parse_args()

system = psys.gas(args.isimpath + '/simulation_output.txt')
animation = psys.animate_system(system)

plt.show()
