import os
import matplotlib.pyplot as plt

if 'build' not in os.listdir():
	os.mkdir('build')
if 'simulation_results' not in os.listdir():
	os.mkdir('simulation_results')

os.system('make clean')
os.system('make compile')
os.system('./newton++')

sims = os.listdir('simulation_results')
sims.sort()
os.system('python3 tools/generate_animation_file.py ' + 'simulation_results/' + sims[-1])
