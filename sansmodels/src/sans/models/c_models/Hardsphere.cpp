/**
	This software was developed by the University of Tennessee as part of the
	Distributed Data Analysis of Neutron Scattering Experiments (DANSE)
	project funded by the US National Science Foundation.

	If you use DANSE applications to do scientific research that leads to
	publication, we ask that you acknowledge the use of the software with the
	following sentence:

	"This work benefited from DANSE software developed under NSF award DMR-0520547."

	copyright 2008, University of Tennessee
 */

/**
 * Scattering model classes
 * The classes use the IGOR library found in
 *   sansmodels/src/libigor
 *
 *	TODO: refactor so that we pull in the old sansmodels.c_extensions
 */

#include <math.h>
#include "models.hh"
#include "parameters.hh"
#include <stdio.h>
using namespace std;

extern "C" {
	#include "libStructureFactor.h"
	#include "Hardsphere.h"
}

HardsphereStructure :: HardsphereStructure() {
	radius      = Parameter(50.0, true);
	radius.set_min(0.0);
	volfraction = Parameter(0.20, true);
	volfraction.set_min(0.0);
}

/**
 * Function to evaluate 1D scattering function
 * The NIST IGOR library is used for the actual calculation.
 * @param q: q-value
 * @return: function value
 */
double HardsphereStructure :: operator()(double q) {
	double dp[2];

	// Fill parameter array for IGOR library
	// Add the background after averaging
	dp[0] = radius();
	dp[1] = volfraction();

	// Get the dispersion points for the radius
	vector<WeightPoint> weights_rad;
	radius.get_weights(weights_rad);

	// Perform the computation, with all weight points
	double sum = 0.0;
	double norm = 0.0;

	// Loop over radius weight points
	for(int i=0; i<weights_rad.size(); i++) {
		dp[0] = weights_rad[i].value;

		sum += weights_rad[i].weight
				* HardSphereStruct(dp, q);
		norm += weights_rad[i].weight;
	}
	return sum/norm ;
}

/**
 * Function to evaluate 2D scattering function
 * @param q_x: value of Q along x
 * @param q_y: value of Q along y
 * @return: function value
 */
double HardsphereStructure :: operator()(double qx, double qy) {
	HardsphereParameters dp;
	// Fill parameter array
	dp.radius      = radius();
	dp.volfraction = volfraction();

	// Get the dispersion points for the radius
	vector<WeightPoint> weights_rad;
	radius.get_weights(weights_rad);

	// Perform the computation, with all weight points
	double sum = 0.0;
	double norm = 0.0;

	// Loop over radius weight points
	for(int i=0; i<weights_rad.size(); i++) {
		dp.radius = weights_rad[i].value;

					double _ptvalue = weights_rad[i].weight
						* Hardsphere_analytical_2DXY(&dp, qx, qy);
					sum += _ptvalue;

					norm += weights_rad[i].weight;
	}
	// Averaging in theta needs an extra normalization
	// factor to account for the sin(theta) term in the
	// integration (see documentation).
	return sum/norm;
}

/**
 * Function to evaluate 2D scattering function
 * @param pars: parameters of the cylinder
 * @param q: q-value
 * @param phi: angle phi
 * @return: function value
 */
double HardsphereStructure :: evaluate_rphi(double q, double phi) {
	double qx = q*cos(phi);
	double qy = q*sin(phi);
	return (*this).operator()(qx, qy);
}