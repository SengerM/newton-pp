import os

os.system('make compile')
os.system('./newton++')
os.system('python3 tools/video_from_data_particle_vs_crystal.py')
