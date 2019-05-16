from argparse import ArgumentParser
import os
import psystems as psys
import matplotlib.pyplot as plt

parser = ArgumentParser()
parser.add_argument('isimpath', help='directory containing the output data of newton++')
parser.add_argument('-n', '--nsnapshots', help='number of snapshots to plot', type=int, default=4)

args = parser.parse_args()

system = psys.crystal_and_particle(args.isimpath + '/simulation_output.txt')
print('Plotting...')
figs, frame_numbers = psys.plot_snapshots(system, n_snapshots=args.nsnapshots)
print('Saving images...')
if 'snapshots' not in os.listdir(args.isimpath):
	os.mkdir(args.isimpath + '/snapshots')
for idx,fig in enumerate(figs):
	fig.savefig(
		args.isimpath + '/snapshots/frame_' + str(frame_numbers[idx]) + '.png',
		facecolor = (0,0,0)
	)
