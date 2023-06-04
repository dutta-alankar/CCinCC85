/* ///////////////////////////////////////////////////////////////////// */
/*!
  \file
  \brief Contains basic functions for problem initialization.

  The init.c file collects most of the user-supplied functions useful
  for problem configuration.
  It is automatically searched for by the makefile.

  \author A. Dutta (alankardutta@iisc.ac.in)
  \date   March 5, 2022
*/
/* ///////////////////////////////////////////////////////////////////// */
#include "pluto.h"
#include <math.h>
#include <stdbool.h>
#include <unistd.h>
#include "wind.h"
//#include "gsl.h"

#define UNIT_MASS (UNIT_DENSITY*pow(UNIT_LENGTH,3))

/* ********************************************************************* */
void Init (double *v, double x1, double x2, double x3)
/*!
 * The Init() function can be used to assign initial conditions as
 * as a function of spatial position.
 *
 * \param [out] v   a pointer to a vector of primitive variables
 * \param [in] x1   coordinate point in the 1st dimension
 * \param [in] x2   coordinate point in the 2nd dimension
 * \param [in] x3   coordinate point in the 3rdt dimension
 *
 * The meaning of x1, x2 and x3 depends on the geometry:
 * \f[ \begin{array}{cccl}
 *    x_1  & x_2    & x_3  & \mathrm{Geometry}    \\ \noalign{\medskip}
 *     \hline
 *    x    &   y    &  z   & \mathrm{Cartesian}   \\ \noalign{\medskip}
 *    R    &   z    &  -   & \mathrm{cylindrical} \\ \noalign{\medskip}
 *    R    & \phi   &  z   & \mathrm{polar}       \\ \noalign{\medskip}
 *    r    & \theta & \phi & \mathrm{spherical}
 *    \end{array}
 *  \f]
 *
 * Variable names are accessed by means of an index v[nv], where
 * nv = RHO is density, nv = PRS is pressure, nv = (VX1, VX2, VX3) are
 * the three components of velocity, and so forth.
 *
 *********************************************************************** */
{
  #if PHYSICS == MHD || PHYSICS == RMHD
  v[BX1] = 0.0;
  v[BX2] = 0.0;
  v[BX3] = 0.0;

  v[AX1] = 0.0;
  v[AX2] = 0.0;
  v[AX3] = 0.0;
  #endif
}

/* ********************************************************************* */
void InitDomain (Data *d, Grid *grid)
/*!
 * Assign initial condition by looping over the computational domain.
 * Called after the usual Init() function to assign initial conditions
 * on primitive variables.
 * Value assigned here will overwrite those prescribed during Init().
 *
 *
 *********************************************************************** */
{
  FILE *fp;
  int overwrite;
  double oth_mu[4];
  int yr = 365*24*60*60;
  double mu   = MeanMolecularWeight((double*)d->Vc, oth_mu);

  double Tcutoff = 1.e4;
  double Tmax    = 1.e8;
  double nmin    = 1e-6;

  g_gamma          = 5/3.;
  g_smallDensity   = (nmin*((CONST_mp*mu)/UNIT_DENSITY));
  g_smallPressure  = (nmin*Tcutoff*CONST_kB)/(UNIT_DENSITY*pow(UNIT_VELOCITY,2));
  g_minCoolingTemp = 1.e4;

  /* Write the data files needed for the simulation if it is non-existent, corrupted or empty */

  /* create the CC85 steady profile for the given set of parameters in python */
  overwrite = 0;
  char CC85DataFile[256];
  sprintf(CC85DataFile, "./CC85_steady-prof_gamma_%.3f.txt", g_gamma);
  if(!access(CC85DataFile, F_OK ) && !access(CC85DataFile, R_OK )){
    fp = fopen(CC85DataFile, "r");
    fseek (fp, 0, SEEK_END);
    int contentSize = ftell(fp);
    overwrite = (contentSize==0)?1:0;
  }
  if(!access(CC85DataFile, F_OK ) && !access(CC85DataFile, R_OK ) && !overwrite)
    read_CC85_data(CC85DataFile);
  else{
    printLog("> Creating CC85 data:\n");
    if (prank==0) create_CC85_data();
    #ifdef PARALLEL
    MPI_Barrier (MPI_COMM_WORLD);
    #endif
    read_CC85_data(CC85DataFile);
  }

  /* create cooling table if not found using Cloudy */
  overwrite = 0;
  char CoolingDataFile[256];
  sprintf(CoolingDataFile, "./cooltable.dat");
  if(!access(CoolingDataFile, F_OK ) && !access(CoolingDataFile, R_OK )){
    fp = fopen(CoolingDataFile, "r");
    fseek (fp, 0, SEEK_END);
    int contentSize = ftell(fp);
    overwrite = (contentSize==0)?1:0;
  }
  if(access(CoolingDataFile, F_OK ) || access(CoolingDataFile, R_OK ) || overwrite){
    if (prank==0){
      int len, dummy;
      char command[500];
      #ifdef PARALLEL
      len = sprintf(command,"cd %s && %s %.3f %.3e %s",
                    "./cloudy-cooling" ,"./hazy_coolingcurve",
                    g_inputParam[ZMET],1e-3,"False");
      #else
      len = sprintf(command,"cd %s && %s %.3f %.3e %s",
                    "./cloudy-cooling" ,"./hazy_coolingcurve",
                    g_inputParam[ZMET],1e-3,"True");
      #endif
      printLog("> Executing: %s\n",command);
      dummy = system(command);
      len = sprintf(command,"cp %s/%s %s",
                    "./cloudy-cooling","hazy_coolingcurve.txt",
                    "./cooltable.dat");
      dummy = system(command);
    }
  }

  #ifdef PARALLEL
  MPI_Barrier (MPI_COMM_WORLD);
  #endif

  /* Initialization starts here */

  double rIni        = g_inputParam[RINI]; // cloud position in units of Rcl
  double thIni       = g_inputParam[THINI]*CONST_PI/180;
  double phiIni      = g_inputParam[PHIINI]*CONST_PI/180;
  double mach        = g_inputParam[MACH];
  double rIniByrInj  = CC85pos(mach);

  printLog("> RiniByRinj = %.5e\n", rIniByrInj);

  int i, j, k;
  double *r   = grid->x[IDIR];
  double *th  = grid->x[JDIR];
  double *phi = grid->x[KDIR];

  TOT_LOOP(k,j,i){
    double x = r[i]*sin(th[j])*cos(phi[k]);
    double y = r[i]*sin(th[j])*sin(phi[k]);
    double z = r[i]*cos(th[j]);

    double distance = r[i];
    double rByrInj  = (distance/rIni)*rIniByrInj;

    d->Vc[RHO][k][j][i]   = CC85rho(rByrInj)/CC85rho(rIniByrInj);
    d->Vc[PRS][k][j][i]   = CC85prs(rByrInj)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2));
    d->Vc[iVR][k][j][i]   = CC85vel(rByrInj)/CC85vel(rIniByrInj);
    d->Vc[iVTH][k][j][i]  = 0.;
    d->Vc[iVPHI][k][j][i] = 0.;
  } /* TOT_LOOP(k,j,i)  */
}

/* ********************************************************************* */
void Analysis (const Data *d, Grid *grid)
/*!
 *  Perform runtime data analysis.
 *
 * \param [in] d the PLUTO Data structure
 * \param [in] grid   pointer to array of Grid structures
 *
 *********************************************************************** */
{

}

#if PHYSICS == MHD
/* ********************************************************************* */
void BackgroundField (double x1, double x2, double x3, double *B0)
/*!
 * Define the component of a static, curl-free background
 * magnetic field.
 *
 * \param [in] x1  position in the 1st coordinate direction \f$x_1\f$
 * \param [in] x2  position in the 2nd coordinate direction \f$x_2\f$
 * \param [in] x3  position in the 3rd coordinate direction \f$x_3\f$
 * \param [out] B0 array containing the vector componens of the background
 *                 magnetic field
 *********************************************************************** */
{
   B0[0] = 0.0;
   B0[1] = 0.0;
   B0[2] = 0.0;
}
#endif

/* ********************************************************************* */
void UserDefBoundary (const Data *d, RBox *box, int side, Grid *grid)
/*!
 *  Assign user-defined boundary conditions.
 *
 * \param [in,out] d  pointer to the PLUTO data structure containing
 *                    cell-centered primitive quantities (d->Vc) and
 *                    staggered magnetic fields (d->Vs, when used) to
 *                    be filled.
 * \param [in] box    pointer to a RBox structure containing the lower
 *                    and upper indices of the ghost zone-centers/nodes
 *                    or edges at which data values should be assigned.
 * \param [in] side   specifies the boundary side where ghost zones need
 *                    to be filled. It can assume the following
 *                    pre-definite values: X1_BEG, X1_END,
 *                                         X2_BEG, X2_END,
 *                                         X3_BEG, X3_END.
 *                    The special value side == 0 is used to control
 *                    a region inside the computational domain.
 * \param [in] grid  pointer to an array of Grid structures.
 *
 *********************************************************************** */
{
  int i, j, k;
  int yr = 365*24*60*60;

  double *r   = grid->x[IDIR];
  double *th  = grid->x[JDIR];
  double *phi = grid->x[KDIR];

  double *dr   = grid->dx[IDIR];
  double *dth  = grid->dx[JDIR];
  double *dphi = grid->dx[KDIR];

  double rIni        = g_inputParam[RINI]; // cloud position in units of Rcl
  double thIni       = g_inputParam[THINI]*CONST_PI/180;
  double phiIni      = g_inputParam[PHIINI]*CONST_PI/180;
  double chi         = g_inputParam[CHI];
  double mach        = g_inputParam[MACH];
  double rIniByrInj  = CC85pos(mach);

  double oth_mu[4];
  double mu   = MeanMolecularWeight((double*)d->Vc, oth_mu);
  double rByrInjTmin = ((rIni+1)/rIni) * rIniByrInj; // rightmost edge of the cloud is the coldest due to adiabatic expansion
  double prsCodeTmin = CC85prs(rByrInjTmin)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2));
  double rhoCodeTmin = CC85rho(rByrInjTmin)/CC85rho(rIniByrInj)*chi;
  double Tcutoff     = (prsCodeTmin/rhoCodeTmin)*pow(UNIT_VELOCITY,2)*((CONST_mp*mu)/CONST_kB); //in K

  Tcutoff = (Tcutoff>1.e4)?Tcutoff:1.e4;

  /* set steady wid profile at the boundary */
  if (side == X1_BEG || side == X1_END){ /* -- select the boundary side -- */
    BOX_LOOP(box,k,j,i){ /* -- Loop over boundary zones -- */
      double distance = r[i];
      double rByrInj  = (distance/rIni)*rIniByrInj;

      d->Vc[RHO][k][j][i]   = CC85rho(rByrInj)/CC85rho(rIniByrInj);
      d->Vc[PRS][k][j][i]   = CC85prs(rByrInj)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2));
      d->Vc[iVR][k][j][i]   = CC85vel(rByrInj)/CC85vel(rIniByrInj);
      d->Vc[iVTH][k][j][i]  = 0.;
      d->Vc[iVPHI][k][j][i] = 0.;
    }
  }

  /* set temperature floor */
  if (side == 0){ // -- select active cells --
    RBox dom_box;
    double gasTemperature;
    double Tmax    = 1.e8;
    double nmin    = 1e-6;

    double oth_mu[4];
    double mu   = MeanMolecularWeight((double*)d->Vc, oth_mu);
    double rhomin  = (nmin*((CONST_mp*mu)/UNIT_DENSITY));

    TOT_LOOP(k,j,i){ // -- Loop over all cells --
      int convert_to_cons = 0;
      gasTemperature = ((d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i])*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/CONST_kB);
      if (gasTemperature<Tcutoff){
        d->Vc[PRS][k][j][i] = (d->Vc[RHO][k][j][i]*Tcutoff)/(pow(UNIT_VELOCITY,2)*((CONST_mp*mu)/CONST_kB));
        convert_to_cons = 1;
      }
      if (gasTemperature>Tmax ){
        if (d->Vc[PRS][k][j][i] > 0) d->Vc[RHO][k][j][i] = (d->Vc[PRS][k][j][i]/Tmax)*(mu*CONST_mp/CONST_kB)*pow(UNIT_VELOCITY,2);
        convert_to_cons = 1;
      }
      if (convert_to_cons){
        RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box);
        PrimToCons3D(d->Vc, d->Uc, &dom_box);
      }
    } // TOT_LOOP(k,j,i)
  }
}

#if BODY_FORCE != NO
/* ********************************************************************* */
void BodyForceVector(double *v, double *g, double x1, double x2, double x3)
/*!
 * Prescribe the acceleration vector as a function of the coordinates
 * and the vector of primitive variables *v.
 *
 * \param [in] v  pointer to a cell-centered vector of primitive
 *                variables
 * \param [out] g acceleration vector
 * \param [in] x1  position in the 1st coordinate direction \f$x_1\f$
 * \param [in] x2  position in the 2nd coordinate direction \f$x_2\f$
 * \param [in] x3  position in the 3rd coordinate direction \f$x_3\f$
 *
 *********************************************************************** */
{
  g[IDIR] = 0.0;
  g[JDIR] = 0.0;
  g[KDIR] = 0.0;

}
/* ********************************************************************* */
double BodyForcePotential(double x1, double x2, double x3)
/*!
 * Return the gravitational potential as function of the coordinates.
 *
 * \param [in] x1  position in the 1st coordinate direction \f$x_1\f$
 * \param [in] x2  position in the 2nd coordinate direction \f$x_2\f$
 * \param [in] x3  position in the 3rd coordinate direction \f$x_3\f$
 *
 * \return The body force potential \f$ \Phi(x_1,x_2,x_3) \f$.
 *
 *********************************************************************** */
{
  return 0.0;
}
#endif
