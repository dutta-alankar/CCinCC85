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
#include "wind.h"
#include <math.h>
#include <stdbool.h>
#include <unistd.h>
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
  g_gamma = 5/3.;
  double oth_mu[4];
  int yr = 365*24*60*60;
  double mu   = MeanMolecularWeight((double*)d->Vc, oth_mu);

  double Tcutoff = 1.e4;
  double Tmax    = 1.e8;
  double nmin    = 1e-6;

  g_smallDensity  = (nmin*((CONST_mp*mu)/UNIT_DENSITY));
  g_smallPressure = (nmin*Tcutoff*CONST_kB)/(UNIT_DENSITY*pow(UNIT_VELOCITY,2));

  /* Write the data files needed for the simulation if it is non-existent, corrupted or empty */
  FILE *fp;
  /* create the CC85 steady profile for the given set of parameters in python */
  int overwrite = 0;
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
    print("CC85 wind data absent!\n");
    QUIT_PLUTO(1);
  }

  #if COOLING != NO
  /* create cooling table if not found using Cloudy */
  char CoolingDataFile[256];
  sprintf(CoolingDataFile, "./cooltable.dat");
  if(!access(CoolingDataFile, F_OK ) && !access(CoolingDataFile, R_OK )){
    fp = fopen(CoolingDataFile, "r");
    fseek (fp, 0, SEEK_END);
    int contentSize = ftell(fp);
  }
  if(access(CoolingDataFile, F_OK ) || access(CoolingDataFile, R_OK )){
    print("cooling data absent!\n");
    QUIT_PLUTO(1);
  }
  #endif

  #ifdef PARALLEL
  MPI_Barrier (MPI_COMM_WORLD);
  #endif

  double rIni        = g_inputParam[RINI]; // Enter cloud position in Rcl
  double chi         = g_inputParam[CHI];
  double mach        = g_inputParam[MACH];

  double rIniByrInj  = CC85pos(mach); // Position wrt wind

  g_dist_lab   = rIni; // Seed cloud position in pc wrt wind center
  g_dist_start_boost = g_dist_lab;

  int i, j, k;
  double *x = grid->x[IDIR];
  double *y = grid->x[JDIR];
  double *z = grid->x[KDIR];

  double xIni = rIni;
  double yIni = 0.;
  double zIni = 0.;
  TOT_LOOP(k,j,i){
    double R = sqrt( (x[i]-xIni)*(x[i]-xIni) + (y[j]-yIni)*(y[j]-yIni) + (z[k]-zIni)*(z[k]-zIni) );
    double rByrInj  = (x[i]/rIni)*rIniByrInj; // Plane parallel assumption

    d->Vc[RHO][k][j][i]   = 1.;
    d->Vc[PRS][k][j][i]   = 1./(g_gamma*mach*mach);
    d->Vc[VX1][k][j][i]   = 1.; //CC85vel(rByrInj)/CC85vel(rIniByrInj);
    d->Vc[VX2][k][j][i]   = 0.;
    d->Vc[VX3][k][j][i]   = 0.;
    d->Vc[TRC][k][j][i]   = 0.;
    if (R <= 1.0) {
      #if WIND_TEST == NO
      d->Vc[RHO][k][j][i]   = chi;
      d->Vc[VX1][k][j][i]   =  0.;
      #endif
      d->Vc[TRC][k][j][i]   =  1.;
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
  static double rIni, chi, mach, tcc, factor, Tcl, mu, rho_cl;
  static int first = 0;
  static long int nstep = -1;
  double temperature_cut[] = {1.2, 2.0, 3.0, 5.0, 10.0}; // temperature cutoff criteria
  double rho_cut[] = {1.2, 2.0, 3.0, 5.0, 10.0};

  double *x  = grid->x[IDIR];
  double *y  = grid->x[JDIR];
  double *z  = grid->x[KDIR];

  double *xl = grid->xl[IDIR];
  double *xr = grid->xr[IDIR];

  double tanl;

  if (first==0) {
    first = 1;
    double oth_mu[4];
    mu   = MeanMolecularWeight((double*)d->Vc, oth_mu);

    rIni        = g_inputParam[RINI]; // cloud position in units of Rcl
    chi         = g_inputParam[CHI];
    mach        = g_inputParam[MACH];

    tcc      = sqrt(chi);
    factor   = sqrt(chi)/3;
    Tcl      = pow(UNIT_VELOCITY/mach,2)*(mu*CONST_mp)/(g_gamma*CONST_kB*chi); //in K just Twind/chi
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

  double Tcutoff = (Tcl>1.e4)?Tcl:1.e4;
  double Tmax    = 1.e8;

  if (g_stepNumber<=nstep && g_time<=(tanl+0.5*g_anldt)) return;

  double      trc   = 0.,      trc_all    = 0.;
  double mass_dense = 0., mass_dense_all  = 0.;
  double vx_cloud = 0., vy_cloud = 0., vz_cloud = 0.;
  double vx_cloud_all = 0., vy_cloud_all = 0., vz_cloud_all = 0.;

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

  double dV, rByrInj, rho_wind, T_wind, T_gas;
  int cold_indx;
  int cloud_indx;

  int spread_indx = (int)(sizeof(rho_cut) / sizeof(rho_cut[0])) - 1;
  double cloud_min = 2*grid->xend_glob[IDIR], cloud_max = 0.5*grid->xbeg_glob[IDIR];
  double cloud_spread;

  rho_wind = 1.0*pow(g_dist_lab/g_inputParam[RINI], -2);
  T_wind = MIN(MAX(chi*Tcl*pow(g_dist_lab/g_inputParam[RINI], -2*(g_gamma-1)), Tcutoff), Tmax);

  DOM_LOOP(k,j,i){
    dV = grid->dV[k][j][i]; // Cell volume
    trc         += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    vx_cloud    += d->Vc[RHO][k][j][i]*d->Vc[VX1][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    vy_cloud    += d->Vc[RHO][k][j][i]*d->Vc[VX2][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    vz_cloud    += d->Vc[RHO][k][j][i]*d->Vc[VX3][k][j][i]*d->Vc[TRC][k][j][i]*dV;

    if(d->Vc[RHO][k][j][i] >= (rho_cl/factor))
      mass_dense += d->Vc[RHO][k][j][i]*dV;
    // double temp_cut = 1.2e5;

    T_gas = (d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i])*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/CONST_kB;
    for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
        if (d->Vc[RHO][k][j][i] >= (rho_wind*rho_cut[cloud_indx])) {
          if( T_gas <= (factor*Tcl) ) {
            mass_cloud[cloud_indx] += d->Vc[RHO][k][j][i]*dV;
            if (cloud_indx == spread_indx) {
              if (xl[i] < cloud_min) cloud_min = xl[i];
              if (xr[i] > cloud_max) cloud_max = xr[i];
            }
          }
        }
    }
    if( T_gas <= (factor*Tcl) ){
      for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++){
          if( T_gas <= (T_wind/temperature_cut[cold_indx]) )
            mass_cold[cold_indx] += d->Vc[RHO][k][j][i]*dV;
      }
    }
  }

  #ifdef PARALLEL
  double pos_value;
  MPI_Allreduce (&cloud_min, &pos_value, 1, MPI_DOUBLE, MPI_MIN, MPI_COMM_WORLD);
  cloud_min = pos_value;
  MPI_Allreduce (&cloud_max, &pos_value, 1, MPI_DOUBLE, MPI_MAX, MPI_COMM_WORLD);
  cloud_max = pos_value;

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
  sendArray[transfer++] = vx_cloud; sendArray[transfer++] = vy_cloud; sendArray[transfer++] = vz_cloud;
  MPI_Allreduce (sendArray, recvArray, transfer_size, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD); // TODO: Replace this with Allreduce to improve on communication overhead
  transfer = 0;
  trc_all = recvArray[transfer++]; mass_dense_all = recvArray[transfer++];
  for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
    mass_cold_all[cold_indx] = recvArray[transfer++];
  }
  for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
    mass_cloud_all[cloud_indx] = recvArray[transfer++];
  }
  vx_cloud_all = recvArray[transfer++]; vy_cloud_all = recvArray[transfer++]; vz_cloud_all = recvArray[transfer++];

  #else
  trc_all    = trc;
  mass_dense_all = mass_dense;

  for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
    mass_cold_all[cold_indx] = mass_cold[cold_indx];
  }
  for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
    mass_cloud_all[cloud_indx] = mass_cloud[cloud_indx];
  }
  vx_cloud_all    = vx_cloud;
  vy_cloud_all    = vy_cloud;
  vz_cloud_all    = vz_cloud;
  #endif
  cloud_spread = fabs(cloud_max-cloud_min);

  vx_cloud_all = vx_cloud_all/trc_all;
  vy_cloud_all = vy_cloud_all/trc_all;
  vz_cloud_all = vz_cloud_all/trc_all;
  trc_all     = trc_all/trc0_all; // trc0_all is M_cloud, ini
  mass_dense_all = mass_dense_all/trc0_all;
  for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
    mass_cold_all[cold_indx] = mass_cold_all[cold_indx]/trc0_all;
  }
  for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
    mass_cloud_all[cloud_indx] = mass_cloud_all[cloud_indx]/trc0_all;
  }

  vx_cloud_all += g_boost_vel;
  double v_cloud = sqrt(vx_cloud_all*vx_cloud_all + vy_cloud_all*vy_cloud_all + vz_cloud_all*vz_cloud_all);

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
      fprintf (fp,"# %s\t=\t%.5e\n", "vwind_asymp (code)", UNIT_VELOCITY );
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
      fprintf (fp, "(%d)dt (code)\t\t", ++cont);
      #if WIND_TEST != NO
      fprintf (fp, "(%d)rho (code)\t\t", ++cont);
      fprintf (fp, "(%d)prs (code)\t\t", ++cont);
      fprintf (fp, "(%d)vel (code)\t\t", ++cont);
      #endif
      fprintf (fp, "(%d)cloud spread (code)\t\t", ++cont);
      fprintf (fp, "\n");
      fclose(fp);
    }
    /* Append numeric data */
    fp = fopen(fname,"a");
    fprintf (fp, "%12.6e\t\t%12.6e\t\t%12.6e\t\t%12.6e\t\t%12.6e\t\t\t",
             g_time, g_dist_lab, v_cloud, trc_all, mass_dense_all); // g_tmp
    for (cold_indx=0; cold_indx<(int)(sizeof(temperature_cut) / sizeof(temperature_cut[0])); cold_indx++) {
      fprintf (fp, "%12.6e\t\t\t", mass_cold_all[cold_indx]);
    }
    for (cloud_indx=0; cloud_indx<(int)(sizeof(rho_cut) / sizeof(rho_cut[0])); cloud_indx++) {
      fprintf (fp, "%12.6e\t\t\t", mass_cloud_all[cloud_indx]);
    }
    fprintf (fp, "%12.6e\t\t", g_dt);
    #if WIND_TEST != NO
    double tmp;
    DOM_LOOP(k, j, i) tmp = d->Vc[RHO][k][j][i];
    fprintf (fp, "%12.6e\t\t", tmp);
    DOM_LOOP(k, j, i) tmp = d->Vc[PRS][k][j][i];
    fprintf (fp, "%12.6e\t\t", tmp);
    DOM_LOOP(k, j, i) tmp = d->Vc[VX1][k][j][i];
    fprintf (fp, "%12.6e\t\t", tmp+g_boost_vel);
    #endif
    fprintf (fp, "%12.6e\t\t", cloud_spread);
    fprintf (fp, "\n");
    fclose(fp);

    /* Write restart file */
    // printLog("Step %d: Writing Analysis restart!\n", g_stepNumber);
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

  double oth_mu[4];
  double  mu   = MeanMolecularWeight((double*)d->Vc, oth_mu);

  double *x   = grid->x[IDIR];

  double *dx   = grid->dx[IDIR];

  double rIni        = g_inputParam[RINI]; // Enter cloud position in Rcl
  double chi         = g_inputParam[CHI];
  double mach        = g_inputParam[MACH];

  double rIniByrInj  = CC85pos(mach);
  double Tcl         = pow(UNIT_VELOCITY/mach,2)*(mu*CONST_mp)/(g_gamma*CONST_kB*chi); //in K

  #if SCALING != NO
  double scale = g_dist_lab/rIni;
  double cc85_exp[5] = {-2., -2.0*g_gamma, 0., -1., -1.};
  #endif

  /* set steady wid profile at the boundary */
  /*
  if (side == X1_BEG) {
    /* -- select the boundary side -- *//*
    BOX_LOOP(box,k,j,i) { /* -- Loop over boundary zones -- *//*
      double rByrInj  = (g_dist_lab/rIni)*rIniByrInj;
      double vel      = CC85vel(rByrInj)/CC85vel(rIniByrInj)

      d->Vc[RHO][k][j][i]   = 1.;
      d->Vc[PRS][k][j][i]   = 1./(g_gamma*mach*mach);
      d->Vc[VX1][k][j][i]   = vel;
      d->Vc[VX2][k][j][i]   = 0.;
      d->Vc[VX3][k][j][i]   = 0.;
      d->Vc[TRC][k][j][i]   = 0.;
      #if SCALING != NO
      d->Vc[RHO][k][j][i]   *= pow(scale, cc85_exp[0]);
      d->Vc[PRS][k][j][i]   *= pow(scale, cc85_exp[1]);
      d->Vc[VX1][k][j][i]   *= pow(scale, cc85_exp[2]);
      d->Vc[VX2][k][j][i]   *= pow(scale, cc85_exp[3]);
      d->Vc[VX3][k][j][i]   *= pow(scale, cc85_exp[4]);
      #endif
      #if TRACKING != NO
      d->Vc[VX1][k][j][i]   -= g_boost_vel;
      #endif
    }
  }
*/
  /* set temperature floor */
  if (side == 0) { // -- select active cells --
    RBox dom_box;
    double gasTemperature;
    double Tcutoff = Tcl;
    double Tmax    = 1.e8;
    double nmin    = 1e-6;

    //int Np = 5;
    double oth_mu[4];
    double mu   = MeanMolecularWeight((double*)d->Vc, oth_mu);
    double rhomin  = (nmin*((CONST_mp*mu)/UNIT_DENSITY));

    TOT_LOOP(k,j,i) { // -- Loop over all cells --
      int convert_to_cons = 0;
      gasTemperature = ((d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i])*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/CONST_kB);
      if (gasTemperature<Tcutoff){
        d->Vc[PRS][k][j][i] = (d->Vc[RHO][k][j][i]*Tcutoff)/(pow(UNIT_VELOCITY,2)*((CONST_mp*mu)/CONST_kB) );
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
