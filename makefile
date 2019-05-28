CC = g++
CFLAGS = -ansi -pedantic -Wall -std=c++11
LFLAGS = -lm -fopenmp

BUILD_DIR = build
SRC_DIR = src

newton++: $(BUILD_DIR)/main.o $(BUILD_DIR)/ParticleSystem.o $(BUILD_DIR)/Particle.o $(BUILD_DIR)/Vec3D.o $(BUILD_DIR)/Force.o $(BUILD_DIR)/Interaction.o $(BUILD_DIR)/my_forces.o
	$(CC) $(CFLAGS) -o newton++ $(BUILD_DIR)/*.o $(LFLAGS)

$(BUILD_DIR)/main.o: $(SRC_DIR)/main.cpp $(SRC_DIR)/main.h $(SRC_DIR)/simulation_config/simulation_macros.n++ $(SRC_DIR)/simulation_config/user_forces.n++ $(SRC_DIR)/simulation_config/user_macros.n++ $(SRC_DIR)/simulation_config/user_particles.n++ $(SRC_DIR)/simulation_config/user_system.n++ $(SRC_DIR)/simulation_config/user_functions.n++ $(SRC_DIR)/simulation_config/loop_action.n++
	$(CC) $(CFLAGS) -c -o $(BUILD_DIR)/main.o $(SRC_DIR)/main.cpp $(LFLAGS)
$(BUILD_DIR)/ParticleSystem.o: $(SRC_DIR)/ParticleSystem.cpp $(SRC_DIR)/ParticleSystem.h $(SRC_DIR)/Particle.h $(SRC_DIR)/Interaction.h
	$(CC) $(CFLAGS) -c -o $(BUILD_DIR)/ParticleSystem.o $(SRC_DIR)/ParticleSystem.cpp $(LFLAGS)
$(BUILD_DIR)/Particle.o: $(SRC_DIR)/Particle.cpp $(SRC_DIR)/Particle.h $(SRC_DIR)/Vec3D.h $(SRC_DIR)/color.h
	$(CC) $(CFLAGS) -c -o $(BUILD_DIR)/Particle.o $(SRC_DIR)/Particle.cpp $(LFLAGS)
$(BUILD_DIR)/Vec3D.o: $(SRC_DIR)/Vec3D.cpp $(SRC_DIR)/Vec3D.h
	$(CC) $(CFLAGS) -c -o $(BUILD_DIR)/Vec3D.o $(SRC_DIR)/Vec3D.cpp $(LFLAGS)
$(BUILD_DIR)/Force.o: $(SRC_DIR)/Force.cpp $(SRC_DIR)/Force.h $(SRC_DIR)/Vec3D.h $(SRC_DIR)/Particle.h $(SRC_DIR)/color.h
	$(CC) $(CFLAGS) -c -o $(BUILD_DIR)/Force.o $(SRC_DIR)/Force.cpp $(LFLAGS)
$(BUILD_DIR)/Interaction.o: $(SRC_DIR)/Interaction.cpp $(SRC_DIR)/Interaction.h $(SRC_DIR)/Force.h
	$(CC) $(CFLAGS) -c -o $(BUILD_DIR)/Interaction.o $(SRC_DIR)/Interaction.cpp $(LFLAGS)
$(BUILD_DIR)/my_forces.o: $(SRC_DIR)/my_forces.cpp $(SRC_DIR)/my_forces.h
	$(CC) $(CFLAGS) -c -o $(BUILD_DIR)/my_forces.o $(SRC_DIR)/my_forces.cpp $(LFLAGS)

clean:
	rm $(BUILD_DIR)/*.o newton++
