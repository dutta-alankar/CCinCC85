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
#include "local_pluto.h"
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
  double chi         = g_inputParam[CHI];
  double mach        = g_inputParam[MACH];
  double rIniByrInj  = CC85pos(mach);

  printLog("> RiniByRinj = %.5e\n", rIniByrInj);
  g_dist_lab  = rIni; //Seed cloud position in units of Rcl wrt wind center

  int i, j, k;
  double *r   = grid->x[IDIR];
  double *th  = grid->x[JDIR];
  double *phi = grid->x[KDIR];

  double xIni = rIni*sin(thIni)*cos(phiIni);
  double yIni = rIni*sin(thIni)*sin(phiIni);
  double zIni = rIni*cos(thIni);
  TOT_LOOP(k,j,i){
    double x = r[i]*sin(th[j])*cos(phi[k]);
    double y = r[i]*sin(th[j])*sin(phi[k]);
    double z = r[i]*cos(th[j]);

    //sqrt(r[i]*r[i] + rIni*rIni - 2*r[i]*rIni*( sin(th[j])*sin(thIni)*cos(phi[k]-phiIni) + cos(th[j])*cos(thIni) ));
    double R = sqrt( (x-xIni)*(x-xIni) + (y-yIni)*(y-yIni) + (z-zIni)*(z-zIni) );
    double distance = r[i];
    double rByrInj  = (distance/rIni)*rIniByrInj;

    d->Vc[RHO][k][j][i]   = CC85rho(rByrInj)/CC85rho(rIniByrInj);
    d->Vc[PRS][k][j][i]   = CC85prs(rByrInj)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2));
    d->Vc[iVR][k][j][i]   = CC85vel(rByrInj)/CC85vel(rIniByrInj);
    d->Vc[iVTH][k][j][i]  = 0.;
    d->Vc[iVPHI][k][j][i] = 0.;
    d->Vc[TRC][k][j][i]   = 0.;
    if (R <= 1.0) {
      d->Vc[RHO][k][j][i]  = chi*d->Vc[RHO][k][j][i]; // TST : Don't change density
      d->Vc[iVR][k][j][i]  = 0.;
      d->Vc[TRC][k][j][i]  = 1.;
    }
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
  int k, j, i, nv;
  int yr = 365*24*60*60;
  static double trc0 = 0.;
  static double trc0_all = 0.;
  static double rIni, thIni, phiIni, chi, mach, rIniByrInj, tcc, factor, Tcl, mu, rho_cl;
  static int first = 0;
  static long int nstep = -1;
  double temperature_cut[] = {1.2, 2.0, 3.0, 5.0, 10.0};
  double rho_cut[] = {1.2, 2.0, 3.0, 5.0, 10.0};

  double *r  = grid->x[IDIR];
  double tanl;

  if (first==0) {
    first = 1;
    double oth_mu[4];
    mu   = MeanMolecularWeight((double*)d->Vc, oth_mu);

    rIni        = g_inputParam[RINI]; // cloud position in units of Rcl
    thIni       = g_inputParam[THINI]*CONST_PI/180;
    phiIni      = g_inputParam[PHIINI]*CONST_PI/180;
    chi         = g_inputParam[CHI];
    mach        = g_inputParam[MACH];
    rIniByrInj  = CC85pos(mach);

    tcc      = sqrt(chi);
    factor   = sqrt(chi)/3;
    Tcl      = (CC85prs(rIniByrInj)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2)))*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/(CONST_kB*chi); // in K
    rho_cl   = chi;
  }
  if (g_stepNumber==0){
    double dV;
    DOM_LOOP(k,j,i){
      dV = grid->dV[k][j][i]; // Cell volume in Spherical
      trc0  += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    }
    #ifdef PARALLEL
    int transfer_size = 1;
    int transfer = 0;
    double sendArray[transfer_size], recvArray[transfer_size];
    sendArray[transfer++] = trc0;
    MPI_Allreduce (sendArray, recvArray, transfer_size, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    transfer = 0;
    trc0_all = recvArray[transfer++];
    #else
    trc0_all    = trc0;
    #endif
  }
  if (g_stepNumber==0 && trc0_all == 0) {
    printLog("> Analysis(): Check initialization! Likely some error as no cloud tracer has been detected!\n");
    QUIT_PLUTO(1);
  }

  if (trc0_all==0) { // Means we have restarted!
    g_restart = 1;
    FILE *fp;
    char fname[512];
    int dummy;
    sprintf (fname, "%s/restart-analysis.out",RuntimeGet()->output_dir);
    fp = fopen(fname,"r");
    dummy = fscanf(fp, "%lf", &trc0_all);
    dummy = fscanf(fp, "%ld", &nstep);
    dummy = fscanf(fp, "%lf", &tanl);
    fclose(fp);
    //printLog("This is step %ld!\n", g_stepNumber);
    //printLog("Analysis should resume from step %d:\n", nstep);
    //printLog("Initial Tracer read as %e\n", trc0_all);
  }

  double rByrInjTmin = ((rIni+1)/rIni) * rIniByrInj; // rightmost edge of the cloud is the coldest due to adiabatic expansion
  double prsCodeTmin = CC85prs(rByrInjTmin)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2));
  double rhoCodeTmin = CC85rho(rByrInjTmin)/CC85rho(rIniByrInj)*chi;
  double Tcutoff     = (prsCodeTmin/rhoCodeTmin)*pow(UNIT_VELOCITY,2)*((CONST_mp*mu)/CONST_kB); //in K
  Tcutoff = (Tcutoff>1.e4)?Tcutoff:1.e4;
  double Tmax    = 1.e8;

  if (g_stepNumber<=nstep && g_time<=(tanl+0.5*g_anldt)) return;
  g_restart = 0;

  double      trc   = 0.,      trc_all    = 0.;
  double mass_dense = 0., mass_dense_all  = 0.;
  double vr_cloud = 0., vt_cloud = 0., vp_cloud = 0.;
  double vr_cloud_all = 0., vt_cloud_all = 0., vp_cloud_all = 0.;

  double mass_cold[(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0]))];
  double mass_cold_all[(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0]))];

  double mass_cloud[(int)(sizeof(rho_cut) / sizeof(rho_cut[0]))];
  double mass_cloud_all[(int)(sizeof(rho_cut) / sizeof(rho_cut[0]))];

  for (i=0; i<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); i++){
    mass_cold[i] = 0.;
    mass_cold_all[i] = 0.;
  }

  for (i=0; i<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); i++){
    mass_cloud[i] = 0.;
    mass_cloud_all[i] = 0.;
  }

  double dV, distance, rByrInj, rho_wind, prs_wind, T_wind, T_gas;
  int cold_indx;
  int cloud_indx;
  DOM_LOOP(k,j,i){
    dV = grid->dV[k][j][i]; // Cell volume
    trc         += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    vr_cloud    += d->Vc[RHO][k][j][i]*d->Vc[iVR][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    vt_cloud    += d->Vc[RHO][k][j][i]*d->Vc[iVTH][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    vp_cloud    += d->Vc[RHO][k][j][i]*d->Vc[iVPHI][k][j][i]*d->Vc[TRC][k][j][i]*dV;

    if(d->Vc[RHO][k][j][i] >= (rho_cl/factor))
      mass_dense += d->Vc[RHO][k][j][i]*dV;
    // double temp_cut = 1.2e5;
    distance = r[i];
    rByrInj  = (distance/rIni)*rIniByrInj;
    rho_wind = CC85rho(rByrInj)/CC85rho(rIniByrInj);
    prs_wind = CC85prs(rByrInj)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2));
    T_wind = MIN(MAX((prs_wind/rho_wind)*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/CONST_kB, Tcutoff), Tmax);

    T_gas = (d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i])*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/CONST_kB;
    for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++){
        if (d->Vc[RHO][k][j][i] >= (rho_wind*rho_cut[cloud_indx])){
          if( T_gas <= (factor*Tcl) )
            mass_cloud[cloud_indx] += d->Vc[RHO][k][j][i]*dV;
        }
    }
    if( T_gas <= (factor*Tcl) ){ // temp_cut){
      for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++){
          if( T_gas <= (T_wind/temperature_cut[cold_indx]) )
            mass_cold[cold_indx] += d->Vc[RHO][k][j][i]*dV;
      }
      /* if (d->Vc[RHO][k][j][i]>(rho_cl/sqrt(chi))) mass_cold += d->Vc[RHO][k][j][i]*dV; */
      /* if (d->Vc[RHO][k][j][i] >= (rho_cl/factor)) mass_cold += d->Vc[RHO][k][j][i]*dV; */
    }
  }

  #ifdef PARALLEL
  int transfer_size = 5 + (int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])) + (int)(sizeof(rho_cut) / sizeof(rho_cut[0]));
  int transfer = 0;
  double sendArray[transfer_size], recvArray[transfer_size];
  sendArray[transfer++] = trc; sendArray[transfer++] = mass_dense;
  for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
    sendArray[transfer++] = mass_cold[cold_indx];
  }
  for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
    sendArray[transfer++] = mass_cloud[cloud_indx];
  }
  sendArray[transfer++] = vr_cloud; sendArray[transfer++] = vt_cloud; sendArray[transfer++] = vp_cloud;
  MPI_Allreduce (sendArray, recvArray, transfer_size, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD); // TODO: Replace this with Allreduce to improve on communication overhead
  transfer = 0;
  trc_all = recvArray[transfer++]; mass_dense_all = recvArray[transfer++];
  for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
    mass_cold_all[cold_indx] = recvArray[transfer++];
  }
  for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
    mass_cloud_all[cloud_indx] = recvArray[transfer++];
  }
  vr_cloud_all = recvArray[transfer++]; vt_cloud_all = recvArray[transfer++]; vp_cloud_all = recvArray[transfer++];

  #else
  trc_all    = trc;
  mass_dense_all = mass_dense;

  for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
    mass_cold_all[cold_indx] = mass_cold[cold_indx];
  }
  for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
    mass_cloud_all[cloud_indx] = mass_cloud[cloud_indx];
  }
  vr_cloud_all    = vr_cloud;
  vt_cloud_all    = vt_cloud;
  vp_cloud_all    = vp_cloud;
  #endif
  vr_cloud_all = vr_cloud_all/trc_all;
  vt_cloud_all = vt_cloud_all/trc_all;
  vp_cloud_all = vp_cloud_all/trc_all;
  trc_all     = trc_all/trc0_all; // trc0_all is M_cloud, ini
  mass_dense_all = mass_dense_all/trc0_all;
  for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
    mass_cold_all[cold_indx] = mass_cold_all[cold_indx]/trc0_all;
  }
  for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
    mass_cloud_all[cloud_indx] = mass_cloud_all[cloud_indx]/trc0_all;
  }
  g_trctrack = trc_all;

  double v_cloud = sqrt(vr_cloud_all*vr_cloud_all + vt_cloud_all*vt_cloud_all + vp_cloud_all*vp_cloud_all);

  /* ---- Write ascii file "analysis.dat" to disk ---- */
  if (prank == 0){
    char fname[512];
    char buffer1[128], buffer2[128];
    sprintf(buffer1, "M(rho>rho_cl/%.1f)/M0", factor);
    sprintf(buffer2, "M(T<%.1f*T_cl)/M0", factor);
    char *cold_header[(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0]))];
    char *cloud_header[(int)(sizeof(rho_cut) / sizeof(rho_cut[0]))];

    for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
      char *dummy1 = (char *)malloc(256*sizeof(char));
      char *dummy2 = (char *)malloc(256*sizeof(char));
      cold_header[cold_indx] = (char *)malloc(256*sizeof(char));
      strcpy(dummy1, buffer2);
      sprintf(dummy2, " [T(r)<T_w(r)/%.1f]", temperature_cut[cold_indx]);
      strcat(dummy1, dummy2);
      strcpy(cold_header[cold_indx], dummy1);
    }

    for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
      cloud_header[cloud_indx] = (char *)malloc(256*sizeof(char));
      sprintf(cloud_header[cloud_indx], "M (rho(r)>=%.1f rho_w(r))/M0", rho_cut[cloud_indx]);
    }

    FILE *fp;
    sprintf (fname, "%s/analysis.dat",RuntimeGet()->output_dir);
    if (g_stepNumber == 0){ /* Open for writing only when we are starting */
      fp = fopen(fname,"w"); /* from beginning */
      fprintf (fp,"# %s\t=\t%.5e\n", "tcc (code)", tcc);
      fprintf (fp,"# %s\t=\t%.5e\n", "vwind_asymp (code)", (CC85vel(5.0)/CC85vel(rIniByrInj)) );
      // Header
      fprintf (fp,"# (1)%s\t\t(2)%s\t(3)%s\t\t(4)%s\t\t(5)%s\t\t",
               "time (code)", "g_dist_lab (code)", "v_cloud (code)", "trc/trc0", buffer1); //, buffer2, "dt (code)");
      int cont = 5;
      for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
        fprintf(fp,"(%d)%s\t\t", ++cont, cold_header[cold_indx]);
      }
      for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
        fprintf(fp,"(%d)%s\t\t", ++cont, cloud_header[cloud_indx]);
      }
      fprintf (fp, "(%d)dt (code)\n", ++cont);
      fclose(fp);
    }
    /* Append numeric data */
    fp = fopen(fname,"a");
    fprintf (fp, "%12.6e\t\t%12.6e\t\t%12.6e\t\t%12.6e\t\t%12.6e\t\t\t",
             g_time, g_dist_lab, v_cloud, trc_all, mass_dense_all);
    for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
      fprintf (fp, "%12.6e\t\t\t", mass_cold_all[cold_indx]);
    }
    for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
      fprintf (fp, "%12.6e\t\t\t", mass_cloud_all[cloud_indx]);
    }
    fprintf (fp, "%12.6e\n", g_dt);
    fclose(fp);

    /* Write restart file */
    //printLog("Step %d: Writing Analysis restart!\n", g_stepNumber);
    FILE *frestart;
    sprintf (fname, "%s/restart-analysis.out", RuntimeGet()->output_dir);
    frestart = fopen(fname,"w");
    fprintf (frestart,"%lf\n", trc0_all);
    fprintf(frestart,"%ld\n", g_stepNumber);
    fprintf(frestart,"%lf\n", g_time);
    fclose(frestart);
  }
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
  if (side == X1_BEG || side == X2_BEG || side == X3_BEG || side == X1_END || side == X2_END || side == X3_END){ /* -- select the boundary side -- */
    BOX_LOOP(box,k,j,i){ /* -- Loop over boundary zones -- */
      double distance = r[i];
      double rByrInj  = (distance/rIni)*rIniByrInj;

      d->Vc[RHO][k][j][i]   = CC85rho(rByrInj)/CC85rho(rIniByrInj);
      d->Vc[PRS][k][j][i]   = CC85prs(rByrInj)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2));
      d->Vc[iVR][k][j][i]   = CC85vel(rByrInj)/CC85vel(rIniByrInj);
      d->Vc[iVTH][k][j][i]  = 0.;
      d->Vc[iVPHI][k][j][i] = 0.;
      d->Vc[TRC][k][j][i]   = 0.;
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
