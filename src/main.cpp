#include "main.h"

#include "simulation_config/user_functions.n++"

int main(int argc, char** argv) {
	size_t i, j, I; // General purpose counters.
	ofstream ofile; // Output file stream.
	string gpstr; // General purpose string.
	string path_str;
	string timeString;
	// ------------------------------------------------- //

	// Begin --------------------------------------------------------
	#ifdef _VERBOSE_
	system("clear");
	cerr << INIT_MSG << endl;
	#endif
	if (argc > 2) {
		cerr << "wrong arguments" << endl;
		return 1;
	} else if (argc == 2)
		timeString = argv[1];
	else
		timeString = now();
	// --------------------------------------------------------------
	#ifdef _VERBOSE_
	cerr << BOLD << "Simulation number: " << RST << timeString << endl;
	cerr << BOLD << "Simulation time: " << RST << SIMULATION_TIME << endl;
	cerr << BOLD << "Time step: " << RST << TIME_STEP << endl;
	cerr << BOLD << "Number of data points to be exported: " << RST << N_EXPORT_POINTS << endl;
	cerr << "-------------------" << endl;
	#endif
	
	path_str = string("");
	path_str.append(OUTPUT_DIRECTORY);
	path_str.append("/");
	path_str.append(timeString);
	
	gpstr = string("");
	gpstr.append("mkdir ");
	gpstr.append(path_str);
	system(gpstr.c_str()); // Creates a new directory in wich to store all the information.
	
	#include "simulation_config/user_macros.n++"
	// Particles ----------------------------------------
	#ifdef _VERBOSE_
	cerr << "Creating and configuring particles... " << endl;
	#endif
	#include "simulation_config/user_particles.n++"
	// ----------------------------------------------------
	// FORCES ----------------------------------------- //
	#ifdef _VERBOSE_
	cerr << "Creating and configuring forces... " << endl;
	#endif
	#include "simulation_config/user_forces.n++" // In this file is where the user has to define the forces.
	// ------------------------------------------------ //
	// System of particles ----------------------------- //
	#ifdef _VERBOSE_
	cerr << "Creating and configuring system of particles..." << endl;
	#endif
	#include "simulation_config/user_system.n++"
	sys.CalcForces(); // Calculates the forces to their initial value.
	// ----------------------------------------------------
	// Print initial conditions and configuration information text file -----
	gpstr = path_str;
	gpstr.append("/");
	gpstr.append(INITIAL_CONDITIONS_DATA_TEXT_FILE);
	ofile.open(gpstr.c_str()); // Opens the file for saving the simulation data.
	ofile << "Initial conditions for simulation number " << timeString << endl;
	sys.Print(ofile);
	ofile << endl << "--------------------------------------------------------------------" << endl;
	ofile << "Values for the macros are:" << endl;
	ofile << "N_EXPORT_POINTS" << '\t' << N_EXPORT_POINTS << endl;
	ofile << "SIMULATION_TIME" << '\t' << SIMULATION_TIME << endl;
	ofile << "TIME_TO_START_SAVING_DATA" << '\t' << TIME_TO_START_SAVING_DATA << endl;
	ofile << "TIME_STEP" << '\t' << TIME_STEP << endl;
	ofile.close();
	// ------------------------------------------------------------------------
	
	#ifdef _VERBOSE_
	//~ cerr << KGRN << "Initial conditions are: --------" << RST << endl;
	//~ sys.Print(cerr);
	cerr << KGRN << "--------------------------------" << RST << endl;
	#endif
	// ---------------------------------------------------------
	
	// Calculation ---------------------------------------------
	#ifdef _VERBOSE_
	cerr << "Preparing calculation..." << endl;
	#endif
	gpstr = path_str;
	gpstr.append("/");
	gpstr.append(OUTPUT_DATA_TEXT_FILE);
	
	cerr << "Calculating... ";
	cerr << "00 %";
	I = SIMULATION_TIME/TIME_STEP; // Final value of the counter "i".
	for (i=0; i<I; i++) {
		sys.StepEuler(TIME_STEP);
		if (i > TIME_TO_START_SAVING_DATA/TIME_STEP && (i%size_t((I-TIME_TO_START_SAVING_DATA/TIME_STEP)/N_EXPORT_POINTS) == 0) ) {
			sys.WriteToBinary(path_str + "/data.bin");

			std::ofstream ofile;
			ofile.open(path_str + "/energy.txt", std::fstream::app);
			ofile << std::scientific; // Sets scientific notation.
			ofile << sys.GetTime() << "\t" << sys.CalculateKineticEnergy(sys.CalculateCenterOfMassVelocity()) << "\n";
			ofile.close();
			
			cerr << ", t = " << sys.GetTime() << ", E = " << sys.CalculateKineticEnergy(sys.CalculateCenterOfMassVelocity()) << "\n";
		}
		if (((i*100)/I)%PERCENTAGE_PRINT_STEP == 0) {
			print_percentage(i,I);
		}
		#include "simulation_config/loop_action.n++"
	}
	print_percentage(i,I);
	cerr << endl;
	
	// -------------------------------------------------- //
	#ifdef _VERBOSE_
	cerr << LAST_MSG << endl;
	#endif
	
}

std::string now(void) { // Function that returns a C++ string object containing the date and time in the format "%Y_%m_%d_%H_%M_%S".
	time_t current_time;
	struct tm * time_info;
	char timeString_c_like[200];
	
	time(&current_time);
	time_info = localtime(&current_time);
	strftime(timeString_c_like, sizeof(timeString_c_like), "%Y_%m_%d_%H_%M_%S", time_info);
	return string(timeString_c_like);
}


void print_percentage(size_t i, size_t I) {
	cerr << '\b' << '\b' << '\b' << '\b';
	cerr << setfill('0') << setw(2) << (i*100)/I << " %";
}

void asd(int i) { // For debugging purposes.
	cerr << WARNING_MSG << "I'm here " << i << endl;
}
