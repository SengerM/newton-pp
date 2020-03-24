import threading
import os
import matplotlib.pyplot as plt
import datetime
import time
import numpy as np

from tools import psystems as psys
from tools.psystems import plot_snapshot

def get_timestamp():
	"""
	Returns a numeric string with a timestamp. It also halts the execution 
	of the program during 10 micro seconds to ensure that all returned
	timestamps to be different and unique.
	
	Returns
	-------
	str
		String containing the timestamp. Format isYYYYMMDDHHMMSSmmmmmm.
	
	Example
	-------	
	>>> get_timestamp()
	'20181013234913378084'
	>>> [get_timestamp(), get_timestamp()]
	['20181013235501158401', '20181013235501158583']
	"""
	timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
	time.sleep(10e-6) # This ensures that there will not exist two equal timestamps.
	return timestamp

simulation_timestamp = get_timestamp()

def plot_preview(newton_thread, sim_number):
	while newton_thread.isAlive():
		while sim_number not in os.listdir('simulation_results'):
			time.sleep(1)
		while 'data.bin' not in os.listdir('simulation_results/' + sim_number):
			time.sleep(1)
		time.sleep(5)
		
		system = psys.gas('simulation_results/' + simulation_timestamp + '/data.bin')
		fig, ax = plot_snapshot(system, len(system.time)-1)
		fig.savefig(
			'simulation_results/' + simulation_timestamp + '/preview.png', 
			facecolor = 'black',
		)
		plt.close(fig)
		
		data = np.genfromtxt('simulation_results/' + simulation_timestamp + '/energy.txt').transpose()
		fig, ax = plt.subplots()
		ax.plot(data[0], data[1])
		ax.set_xlabel('Time')
		ax.set_ylabel('Energy')
		ax.set_yscale('log')
		fig.savefig('simulation_results/' + simulation_timestamp + '/energy.png')
		plt.close(fig)

def run_newton_pp():
	start = time.time()
	os.system('./newton++ ' + simulation_timestamp)
	end = time.time()
	print('newton++ execution time was ' + str(end-start) + ' seconds')

newton_thread = threading.Thread(
	target = run_newton_pp, 
	name = 'newton++'
)
plotting_thread = threading.Thread(
	target = plot_preview,
	name = 'preview thread',
	args = (newton_thread, simulation_timestamp,)
)

if 'build' not in os.listdir():
	os.mkdir('build')
if 'simulation_results' not in os.listdir():
	os.mkdir('simulation_results')

os.system('rm newton++')
os.system('make newton++')

newton_thread.start()
plotting_thread.start()

while newton_thread.isAlive() or plotting_thread.isAlive():
	time.sleep(1)

os.system('python3 tools/generate_animation_file.py ' + 'simulation_results/' + simulation_timestamp)

print('Finished!')
