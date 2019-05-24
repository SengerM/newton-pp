import threading
import os
import matplotlib.pyplot as plt
import datetime
from time import sleep

from tools.psystems import gas
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
	sleep(10e-6) # This ensures that there will not exist two equal timestamps.
	return timestamp

simulation_timestamp = get_timestamp()

def plot_preview(newton_thread, sim_number):
	while newton_thread.isAlive():
		while sim_number not in os.listdir('simulation_results'):
			sleep(1)
		while 'simulation_output.txt' not in os.listdir('simulation_results/' + sim_number):
			sleep(1)
		system = gas('simulation_results/' + simulation_timestamp + '/simulation_output.txt')
		fig, ax = plot_snapshot(system, len(system.time)-1)
		fig.savefig(
			'simulation_results/' + simulation_timestamp + '/preview.png', 
			facecolor = 'black',
		)
		plt.close(fig)
		sleep(5)

newton_thread = threading.Thread(
	target = lambda: os.system('./newton++ ' + simulation_timestamp), 
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
	sleep(1)

os.system('python3 tools/generate_animation_file.py ' + 'simulation_results/' + simulation_timestamp)

print('Finished!')
