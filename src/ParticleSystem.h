#ifndef _SYSTEMOFPARTICLES_H_
#define _SYSTEMOFPARTICLES_H_

#include <iostream>
#include <vector>
#include <fstream>
#include "Particle.h"
#include "Interaction.h"

#define PRINTTXT_SEP_CHAR "\t"

#define _PARALLEL_

struct SysNode { // This class specifies the nodes in wich there are stored the particles of the system.
	Particle * particle; // Pointer to the current particle.
	std::vector<Interaction> * interactions; // Pointer to a vector of interactions.
	Vec3D net_force; // Net force resulting from all the interactions.
	
	SysNode(void) { // Constructor
		particle = NULL; 
		interactions = NULL; 
		Vec3D net_force(0,0,0);
	}
};

class ParticleSystem {
private:
	double time;
	std::vector<SysNode> nodes_vec; // Vector of nodes that contain the particles and point to other nodes that contain interactions.
	Vec3D get_force_if(SysNode & node, Vec3D & position); // Get force if the particle contained in "node" were at «position».
public:
	ParticleSystem(void);
	~ParticleSystem(void);
	Particle & GetParticle(size_t i); // Returns a reference to the i-th particle.
	
	size_t AddParticle(Particle &); // Returns the number of the particle just added.
	void AddInteraction(Particle &, Particle &, Force &); // This is for classical forces.
	void AddInteraction(Particle &, Force &); // This is for fields.
	Particle & operator[](size_t i); // Returns a reference to the i-th particle.
	size_t Size(void); // Returns number of particles.
	void Print(std::ostream &);
	void WriteToTXT(std::string filepath); // Prints the time and position of each particle in a text file.
	void WriteToBinary(std::string filepath); // Writes the time and position of each particle in a binary file with double numbers.
	void CalcForces(void); // Calculates all the forces of the system with the current state of the particles and parameters (and time).
	void StepRK4(double h); // Evolves the system one step of time «h» using the method Runge-Kutta 4.
	void StepEuler(double h); // Evolves the system one step of time «h» using the Euler's method.
	double CalculateKineticEnergy(Vec3D frame_velocity); // Calculates the kinetic energy of the system and returns it.
	Vec3D CalculateCenterOfMassVelocity(void);
	Vec3D CalculateCenterOfMassPosition(void);
	
	double GetTime();
};


#endif
