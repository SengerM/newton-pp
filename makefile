CC = g++
CFLAGS = -ansi -pedantic -Wall -std=c++11
LFLAGS = -lm

SOURCE_DIR = src

compile: main.o ParticleSystem.o Particle.o Vec3D.o Force.o Interaction.o my_forces.o
	$(CC) $(CFLAGS) -o newton++ *.o $(LFLAGS)

main.o: $(SOURCE_DIR)/main.cpp $(SOURCE_DIR)/main.h $(SOURCE_DIR)/simulation_config/simulation_macros.n++ $(SOURCE_DIR)/simulation_config/user_forces.n++ $(SOURCE_DIR)/simulation_config/user_macros.n++ $(SOURCE_DIR)/simulation_config/user_particles.n++ $(SOURCE_DIR)/simulation_config/user_system.n++ $(SOURCE_DIR)/simulation_config/user_functions.n++
	$(CC) $(CFLAGS) -c -o main.o $(SOURCE_DIR)/main.cpp $(LFLAGS)
ParticleSystem.o: $(SOURCE_DIR)/ParticleSystem.cpp $(SOURCE_DIR)/ParticleSystem.h $(SOURCE_DIR)/Particle.h $(SOURCE_DIR)/Interaction.h
	$(CC) $(CFLAGS) -c -o ParticleSystem.o $(SOURCE_DIR)/ParticleSystem.cpp $(LFLAGS)
Particle.o: $(SOURCE_DIR)/Particle.cpp $(SOURCE_DIR)/Particle.h $(SOURCE_DIR)/Vec3D.h $(SOURCE_DIR)/color.h
	$(CC) $(CFLAGS) -c -o Particle.o $(SOURCE_DIR)/Particle.cpp $(LFLAGS)
Vec3D.o: $(SOURCE_DIR)/Vec3D.cpp $(SOURCE_DIR)/Vec3D.h
	$(CC) $(CFLAGS) -c -o Vec3D.o $(SOURCE_DIR)/Vec3D.cpp $(LFLAGS)
Force.o: $(SOURCE_DIR)/Force.cpp $(SOURCE_DIR)/Force.h $(SOURCE_DIR)/Vec3D.h $(SOURCE_DIR)/Particle.h $(SOURCE_DIR)/color.h
	$(CC) $(CFLAGS) -c -o Force.o $(SOURCE_DIR)/Force.cpp $(LFLAGS)
Interaction.o: $(SOURCE_DIR)/Interaction.cpp $(SOURCE_DIR)/Interaction.h $(SOURCE_DIR)/Force.h
	$(CC) $(CFLAGS) -c -o Interaction.o $(SOURCE_DIR)/Interaction.cpp $(LFLAGS)
my_forces.o: $(SOURCE_DIR)/my_forces.cpp $(SOURCE_DIR)/my_forces.h
	$(CC) $(CFLAGS) -c -o my_forces.o $(SOURCE_DIR)/my_forces.cpp $(LFLAGS)

clean:
	rm *.o newton++
