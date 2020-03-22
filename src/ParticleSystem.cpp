#include "ParticleSystem.h"

using namespace std;

ParticleSystem::ParticleSystem(void) { // Constructs a particle system with no particles at all...
	time = 0;
}

ParticleSystem::~ParticleSystem(void) {
	size_t k;
	for (k=0; k<nodes_vec.size(); k++) {
		if ( (nodes_vec[k]).interactions == NULL ) // This means the particle has no interactions so theres nothing to delete.
			continue;
		delete (nodes_vec[k]).interactions;
	}
}

size_t ParticleSystem::AddParticle(Particle & p) { // Returns the number of the particle just added.
	SysNode node;
	(node.particle) = &p;
	nodes_vec.push_back(node);
	return nodes_vec.size();
}

size_t ParticleSystem::Size(void) { // Returns number of particles.
	return nodes_vec.size();
}

Particle & ParticleSystem::operator[](size_t i) {
	return *((nodes_vec[i]).particle);
}

Particle & ParticleSystem::GetParticle(size_t i) { // Returns a reference to the i-th particle.
	return *((nodes_vec[i]).particle);
}

void ParticleSystem::Print(std::ostream & stream) {
	Vec3D aux_vec;
	size_t k, l, n_interactions;
	for (k=0; k<nodes_vec.size(); k++) {
		stream << endl;
		stream << "Particle # " << k << endl;
		stream << *(nodes_vec[k].particle) << endl;
		stream << "Net force: " << (nodes_vec[k]).net_force << endl;
		if ((nodes_vec[k]).interactions != NULL) { // This means that the particle has interactions.
			stream << "Interacting with: " << endl;
			n_interactions = ((*((nodes_vec[k]).interactions)).size());
			for (l=0; l<n_interactions; l++) {
				if ( ((*((nodes_vec[k]).interactions))[l]).WithField() ) { // This means that the interaction is with a field.
					stream << "Field: «" << ((*((nodes_vec[k]).interactions))[l]).GetForceName() << "»";
				} else { // This means that the interaction is with a particle.
					stream << "Classical force: «" << ((*((nodes_vec[k]).interactions))[l]).GetForceName() << RST << "» with particle # " << ((*((nodes_vec[k]).interactions))[l]).GetParticleNumber();
				}
				aux_vec = ((*((nodes_vec[k]).interactions))[l]).GetValue();
				stream << " | Force value: " << aux_vec << endl;
			}
		} else { // No interactions.
			stream << "This particle has no interactions. " << endl;
		}
	}
}

void ParticleSystem::WriteToTXT(std::string filepath) {
	// Writes the time and position of each particle in a TXT file.
	std::ofstream ofile;
	ofile.open(filepath.c_str(), std::fstream::app);
	ofile << std::scientific; // Sets scientific notation.
	
	Vec3D aux_vec;
	size_t k;
	ofile << time << PRINTTXT_SEP_CHAR;
	for (k=0; k<nodes_vec.size()-1; k++) {
		aux_vec = (*((nodes_vec[k]).particle)).Position();
		ofile << aux_vec.GetX() << PRINTTXT_SEP_CHAR;
		ofile << aux_vec.GetY() << PRINTTXT_SEP_CHAR;
		ofile << aux_vec.GetZ() << PRINTTXT_SEP_CHAR;
	}
	aux_vec = (*((nodes_vec[k]).particle)).Position();
	ofile << aux_vec.GetX() << PRINTTXT_SEP_CHAR;
	ofile << aux_vec.GetY() << PRINTTXT_SEP_CHAR;
	ofile << aux_vec.GetZ();
	ofile << endl;
	ofile.close();
}

void ParticleSystem::WriteToBinary(std::string filepath) {
	// Writes the time and position of each particle in a binary file with float numbers.
	static bool first_call = true;
	std::ofstream ofile;
	ofile.open(filepath.c_str(), std::ios::out | std::ios::app | std::ios::binary);
	if (first_call == true) {
		float nparticles = nodes_vec.size();
		ofile.write(reinterpret_cast<const char*>(&nparticles), sizeof(float));
		first_call = false;
	}
	ofile.write(reinterpret_cast<const char*>(&time), sizeof(float));
	for (size_t k = 0; k < nodes_vec.size(); k++) {
		Vec3D aux = (*((nodes_vec[k]).particle)).Position();
		float x = aux.GetX(), y = aux.GetY(), z = aux.GetZ();
		ofile.write(reinterpret_cast<const char*>(&x), sizeof(float));
		ofile.write(reinterpret_cast<const char*>(&y), sizeof(float));
		ofile.write(reinterpret_cast<const char*>(&z), sizeof(float));
	}
	ofile.close();
}

void ParticleSystem::AddInteraction(Particle & a, Particle & b, Force & force) { // Adds to particle «a» an interaction with particle «b» defined by «force».
	if (force.IsField()) {
		cerr << WARNING_MSG << "Trying to add interaction «" << force.GetName() << "» wich is of type «field» to two particles. It must be added to only one particle. Nothing is done." << endl;
		return;
	}
	// Search for the position of each particle in the vector.
	size_t k, pos_a, pos_b;
	bool a_founded=false, b_founded=false;
	for (k=0; k<nodes_vec.size(); k++) {
		if ((nodes_vec[k]).particle == &a) {
			a_founded = true;
			pos_a = k;
		}
		if ((nodes_vec[k]).particle == &b) {
			b_founded = true;
			pos_b = k;
		}
		if (a_founded && b_founded)
			break;
	}
	if (!a_founded) { // The main particle is not in the system!
		cerr << WARNING_MSG << "Trying to add interaction «" << force.GetName() << "» to particle «" << a.Name() << "» but «" << a.Name() << "» is not part of the system of particles. Nothing is done." << endl;
		return;
	} else if (!b_founded) {
		cerr << WARNING_MSG << "Trying to add interaction «" << force.GetName() << "» to particle # " << pos_a << " named «" << a.Name() << "» with «" << b.Name() << "» but the second one is not part of the system of particles. This interaction will be discarded." << endl;
		return;
	}
	if (pos_a == pos_b)
		cerr << WARNING_MSG << "Adding interaction «" << force.GetName() << "» to particle # " << pos_a << " named «" << a.Name() << "» with itself." << endl;
	// -----------------
	
	if ((nodes_vec[pos_a]).interactions == NULL) { // This means that no interactions have been added yet.
		(nodes_vec[pos_a]).interactions = new vector<Interaction>;
	}
	
	Interaction current_interaction(force, pos_b);
	(*((nodes_vec[pos_a]).interactions)).push_back(current_interaction);
}

void ParticleSystem::AddInteraction(Particle & a, Force & force) { // This is for fields.
	if (!force.IsField()) {
		cerr << WARNING_MSG << "Trying to add interaction «" << force.GetName() << "» wich is NOT of type «field» (is a classical force between two particles) to only one particle. Nothing is done." << endl;
		return;
	}
	
	// Search for the position of the particle.
	size_t k, pos_a;
	bool a_founded=false;
	for (k=0; k<nodes_vec.size(); k++) {
		if ((nodes_vec[k]).particle == &a) {
			a_founded = true;
			pos_a = k;
			break;
		}
	}
	if (!a_founded) { // The main particle is not in the system!
		cerr << WARNING_MSG << "Trying to add interaction «" << force.GetName() << "» to particle «" << a.Name() << "» but «" << a.Name() << "» is not part of the system of particles. Nothing is done." << endl;
		return;
	}
	// -----------------
	if ((nodes_vec[pos_a]).interactions == NULL) { // This means that no interactions have been added yet.
		(nodes_vec[pos_a]).interactions = new vector<Interaction>;
	}
	
	Interaction current_interaction(force, 0);
	(*((nodes_vec[pos_a]).interactions)).push_back(current_interaction);
}

void ParticleSystem::CalcForces(void) { // Calculates all the forces of the system with the current state of the particles and parameters (and time).
	#ifdef _PARALLEL_
	#pragma omp parallel for
	#endif
	for (size_t k=0; k<nodes_vec.size(); k++) {
		Vec3D aux_vec;
		Force *force;
		Interaction *current_interaction;
		Particle current_particle, interacting_particle;
		if ((nodes_vec[k]).interactions == NULL) { // This means the particle has no interactions.
			continue;
		}
		current_particle = *((nodes_vec[k]).particle);
		size_t n_interactions = ((*((nodes_vec[k]).interactions)).size());
		(nodes_vec[k]).net_force = Vec3D(0,0,0); // Clear the net force.
		for (size_t l=0; l<n_interactions; l++) {
			current_interaction = &((*((nodes_vec[k]).interactions))[l]);
			force = &(current_interaction->GetForce());
			if (force->IsField()) {
				aux_vec = (*force)(current_particle);
				current_interaction->SetValue(aux_vec);
			} else { // Is a classical force between two particles.
				interacting_particle = *((nodes_vec[ ((*((nodes_vec[k]).interactions))[l]).GetParticleNumber() ]).particle);
				aux_vec = (*force)(current_particle, interacting_particle);
				current_interaction->SetValue(aux_vec);
			}
			(nodes_vec[k]).net_force = (nodes_vec[k]).net_force + current_interaction->GetValue();
		}
	}
}

void ParticleSystem::StepRK4(double dt) { // Evolves the system one step of time «h» using the method Runge-Kutta 4.
	//~ cerr << WARNING_MSG << "«void ParticleSystem::StepRK4(double h)» not yet implemented." << endl;
	this->CalcForces(); // Update the forces of the system. 
	
	size_t 	k;
	double 	m; // mass.
	Vec3D 	r, // position.
			r2, // modified position to calculate the RK4 coefficient k2.
			r3, // modified position to calculate the RK4 coefficient k3.
			r4, // modified position to calculate the RK4 coefficient k4.
			v, // velocity.
			F, // force.
			k11, k12, // RK4
			k21, k22, // RK4
			k31, k32, // RK4
			k41, k42; // RK4
	Particle current_particle;
	
	for (k=0; k<nodes_vec.size(); k++) {
		current_particle = *((nodes_vec[k]).particle);
		r = current_particle.Position(); // Current position of the k'th particle.
		v = current_particle.Velocity(); // Current speed of the k'th particle.
		F = ((nodes_vec[k]).net_force); // Current force acting on the k'th particle.
		m = current_particle.Mass(); // Mass of the k'th particle.
		
		k11 = v;
		k12 = F/m;
		
		r2 = r + k11*(dt/2);
		k21 = v + k12*(dt/2);
		k22 = get_force_if(nodes_vec[k], r2)/m;
		
		r3 = r + k21*(dt/2);
		k31 = v + k22*(dt/2);
		k32 = get_force_if(nodes_vec[k], r3)/m;
		
		r4 = r + k31*(dt/2);
		k41 = v + k32*dt;
		k42 = get_force_if(nodes_vec[k], r4)/m;
		
		(*((nodes_vec[k]).particle)).Position() = r + (k11 + k21*2 + k31*2 + k41)*(dt/6); // New position of the k'th particle.
		(*((nodes_vec[k]).particle)).Velocity() = v + (k12 + k22*2 + k32*2 + k42)*(dt/6); // New velocity of the k'th particle.
	}
	time += dt;
}

Vec3D ParticleSystem::get_force_if(SysNode & node, Vec3D & position) { // Get force if the particle contained in "node" were at «position».
	// CHECK BECAUSE SOMETHING IS WRONG IMPLEMENTED. The system has a center of mass motion even after it was removed at the begining (compare with "stepEuler" that is properly working).
	if (node.interactions == NULL) // This means the particle has no interactions.
		return Vec3D(0,0,0);
		
	Particle current_particle = *(node.particle);
	Particle *interacting_particle;
	Vec3D force_value; // This is the value to be returned.
	Force *force;
	size_t i;
	size_t n_interactions = (*(node.interactions)).size();
	Interaction *current_interaction;
	
	current_particle.Position() = position; // Modify the position of the particle.
	for (i=0; i<n_interactions; i++) {
		current_interaction = &((*(node.interactions))[i]);
		force = &(current_interaction->GetForce());
		if (force->IsField()) {
			force_value = force_value + (*force)(current_particle);
		} else { // Is a classical force between two particles.
			interacting_particle = ((nodes_vec[ ((*(node.interactions))[i]).GetParticleNumber() ]).particle);
			force_value = force_value + (*force)(current_particle, *interacting_particle);
		}
	}
	return force_value;
}

void ParticleSystem::StepEuler(double h) { // Evolves the system one step of time «h» using the Euler's method.
	this->CalcForces(); // Update the forces of the system. 
	
	size_t 	k,
			N_particles = this->nodes_vec.size();
	double 	m; // mass.
	Vec3D 	r, // position.
			v, // velocity.
			F; // force.
	
	std::vector<Vec3D> 	new_positions(N_particles),
						new_velocities(N_particles);
	#ifdef _PARALLEL_
	#pragma omp parallel for
	#endif
	for (k=0; k<N_particles; k++) {
		double 	m; // mass.
		Vec3D 	r, // position.
				v, // velocity.
				F; // force.
		r = (*((nodes_vec[k]).particle)).Position(); // Current position of the k'th particle.
		v = (*((nodes_vec[k]).particle)).Velocity(); // Current speed of the k'th particle.
		F = ((nodes_vec[k]).net_force); // Current force acting on the k'th particle.
		m = (*((nodes_vec[k]).particle)).Mass(); // Mass of the k'th particle.
		new_positions[k] = r + (v + F*(h/(2*m)))*h; // New position of the k'th particle.
		new_velocities[k] = v + F/m*h; // New velocity of the k'th particle.
	}
	#ifdef _PARALLEL_
	#pragma omp parallel for
	#endif
	for (k=0; k<N_particles; k++) {
		(*((nodes_vec[k]).particle)).Position() = new_positions[k]; // New position of the k'th particle.
		(*((nodes_vec[k]).particle)).Velocity() = new_velocities[k]; // New velocity of the k'th particle.
	}
	time += h;
}

double ParticleSystem::GetTime(void) {
	return time;
}

double ParticleSystem::CalculateKineticEnergy(Vec3D frame_velocity = Vec3D()) {
	double energy = 0;
	for (size_t i = 0; i < this->nodes_vec.size(); i++) {
		double mass = (*((nodes_vec[i]).particle)).Mass();
		double speed = ( (*((nodes_vec[i]).particle)).Velocity() - frame_velocity ).Abs();
		energy += mass/2*speed*speed;
	}
	return energy;
}

Vec3D ParticleSystem::CalculateCenterOfMassVelocity(void) {
	Vec3D center_of_mass_velocity;
	double total_mass = 0;
	for (size_t i = 0; i < this->nodes_vec.size(); i++) {
		double mass = (*((nodes_vec[i]).particle)).Mass();
		Vec3D velocity = (*((nodes_vec[i]).particle)).Velocity();
		center_of_mass_velocity = center_of_mass_velocity + velocity*mass;
		total_mass += mass;
	}
	center_of_mass_velocity = center_of_mass_velocity/total_mass;
	return center_of_mass_velocity;
}
