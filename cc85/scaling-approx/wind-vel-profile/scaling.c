/* ///////////////////////////////////////////////////////////////////// */
/*!
 *   \file
 *     \brief cloud tracking by shifting cells using tracer weighted position
 *
 *       \author Alankar Dutta
 *       \date   Jun 29, 2022
 *
 * ///////////////////////////////////////////////////////////////////// */
#include "pluto.h"
#include "local_pluto.h"
#include "wind.h"

void ApplyWindScaling (const Data *d, Grid *grid, double *all_scales)
/*!
 * Integrate cooling and reaction source terms.
 *
 * \param [in,out]  d      pointer to Data structure
 * \param [in]     grid    pointer to an array of Grid structures
 * \param [in]     double* scale factors
 *
 *********************************************************************** */
{
  double scale     = all_scales[0];
  double vx_factor = all_scales[1];

  int i, j, k;
  int iend = grid->lend[IDIR] + grid->nghost[IDIR];
  int jend = grid->lend[JDIR] + grid->nghost[JDIR];
  int kend = grid->lend[KDIR] + grid->nghost[KDIR];

  double cc85_exp[5] = {-2., -2.0*g_gamma, 0., -1., -1.};

  double rIni        = g_inputParam[RINI]; // Enter cloud position in Rcl
  double chi         = g_inputParam[CHI];
  double mach        = g_inputParam[MACH];

  double oth_mu[4];
  double mu   = MeanMolecularWeight((double*)d->Vc, oth_mu);

  double Tcl         = pow(UNIT_VELOCITY/mach,2)*(mu*CONST_mp)/(g_gamma*CONST_kB*chi); //in K just Twind/chi

  double gasTemperature;
  double Tcutoff = Tcl;
  double Tmax    = 1.e8;
  double nmin    = 1e-6;
  double rhomin  = (nmin*((CONST_mp*mu)/UNIT_DENSITY));

  JTOT_LOOP(j) {
    grid->x[JDIR][j]  *= pow(scale, 1.0);
    grid->xr[JDIR][j] *= pow(scale, 1.0);
    grid->xl[JDIR][j] *= pow(scale, 1.0);
    grid->dx[JDIR][j] *= pow(scale, 1.0);
  }
  KTOT_LOOP(k) {
    grid->x[KDIR][k]  *= pow(scale, 1.0);
    grid->xr[KDIR][k] *= pow(scale, 1.0);
    grid->xl[KDIR][k] *= pow(scale, 1.0);
    grid->dx[KDIR][k] *= pow(scale, 1.0);
  }
  SetGeometry(grid);

  TOT_LOOP(k,j,i){
    #if CONST_WIND_VEL == NO
    #if WIND_TEST == NO
    d->Vc[VX1][k][j][i]   += (vx_factor*(1.-d->Vc[TRC][k][j][i]));
    #else
    d->Vc[VX1][k][j][i]   += vx_factor;
    #endif
    #endif
    d->Vc[RHO][k][j][i]  *= pow(scale, cc85_exp[0]);
    d->Vc[PRS][k][j][i]  *= pow(scale, cc85_exp[1]);

    d->Vc[VX1][k][j][i]  *= pow(scale, cc85_exp[2]);
    d->Vc[VX2][k][j][i]  *= pow(scale, cc85_exp[3]);
    d->Vc[VX3][k][j][i]  *= pow(scale, cc85_exp[4]);

    d->Vc[TRC][k][j][i]  *= 1.;

    /* Update the conservative variables */
    RBox dom_box;
    RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box);
    PrimToCons3D(d->Vc, d->Uc, &dom_box);
  } // TOT_LOOP(k,j,i)

  TOT_LOOP(k,j,i) { // -- Loop over all cells --
    int convert_to_cons = 0;
    gasTemperature = ((d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i])*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/CONST_kB);
    if (gasTemperature<Tcutoff) {
      d->Vc[PRS][k][j][i] = (d->Vc[RHO][k][j][i]*Tcutoff)/(pow(UNIT_VELOCITY,2)*((CONST_mp*mu)/CONST_kB) );
      convert_to_cons = 1;
    }
    if (gasTemperature>Tmax ) {
      if (d->Vc[PRS][k][j][i] > 0) d->Vc[RHO][k][j][i] = (d->Vc[PRS][k][j][i]/Tmax)*(mu*CONST_mp/CONST_kB)*pow(UNIT_VELOCITY,2);
      convert_to_cons = 1;
    }
    RBox dom_box;
    if (convert_to_cons) {
      RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box);
      PrimToCons3D(d->Vc, d->Uc, &dom_box);
    }
  } // TOT_LOOP(k,j,i)
}

int store_or_save_cloud_pos(double position, double velocity, int save) {
  static double cloud_pos = -1.0;
  static double cloud_vel = -1.0;
  if (g_stepNumber==0) {
    cloud_pos = g_inputParam[RINI];
    #if WIND_TEST == NO
    cloud_vel = 0.;
    #else
    cloud_vel = 1.0;
    #endif
    return 0;
  }
  if (save == 0 && g_stepNumber>0){
     cloud_pos = position;
     cloud_vel = velocity;
     return 0; // success
  }
  if (save == 1){
    FILE *fp;
    char fname[512];
    int dummy;
    sprintf (fname, "%s/restart-cloud-props.out", RuntimeGet()->output_dir);
    fp = fopen(fname,"w");
    fprintf(fp, "%f\n", cloud_pos);
    fprintf(fp, "%f\n", cloud_vel);
    fprintf(fp, "%d\n", g_first_time_boost);
    fclose(fp);
    return 0; // success
  }
  return -1; // error
}

double* calc_scale(double vx_cloud, double dt)
{
  double start = BOOST_START*sqrt(g_inputParam[CHI]);
  double scale = 0.;
  static int once = 0;
  static double cloud_vel = -1.0;
  static double cloud_pos = -1.0;
  if (g_stepNumber==0) {
    cloud_vel = vx_cloud;
    #if WIND_TEST == NO
    cloud_pos = g_inputParam[RINI] + vx_cloud*0.5*dt;
    #else
    cloud_pos = g_inputParam[RINI] + (1.0 + vx_cloud)*0.5*dt;
    #endif
    #if TRACKING != NO
    g_first_time_boost = (start==0.)?0:1;
    if (start=0.) g_dist_start_boost = cloud_pos;
    #endif
  }
  if (cloud_pos==-1.0 && once==0) { // means we have restarted
    FILE *fp;
    char fname[512];
    int dummy;
    sprintf (fname, "%s/restart-cloud-props.out", RuntimeGet()->output_dir);
    fp = fopen(fname,"r");
    dummy = fscanf(fp, "%f\n", &cloud_pos);
    dummy = fscanf(fp, "%f\n", &cloud_vel);
    dummy = fscanf(fp, "%d\n", &g_first_time_boost);
    #if TRACKING != NO
    if ( g_time>=start ) g_boost_vel = cloud_vel;
    else
    #endif
      g_boost_vel = 0.;
    fclose(fp);
    once = 1;
  }

  double cloud_pos_old = (g_stepNumber>0)?cloud_pos:g_inputParam[RINI];
  #if TRACKING != NO
  if (g_time>=start && g_stepNumber>0) {
    if (g_first_time_boost==1) {
      cloud_pos += ( (cloud_vel + vx_cloud)*0.5*dt );
      cloud_vel = vx_cloud;
      g_first_time_boost = 0;
      g_dist_start_boost = g_dist_lab;
    }
    else {
      cloud_pos += ( (cloud_vel + (cloud_vel + vx_cloud))*0.5*dt );
      cloud_vel += vx_cloud;
    }
  }
  else {
    cloud_pos += ( (cloud_vel + vx_cloud)*0.5*dt );
    cloud_vel = vx_cloud;
    g_dist_start_boost = g_dist_lab;
  }
  #else
  cloud_pos += ( (cloud_vel + vx_cloud)*0.5*dt );
  cloud_vel = vx_cloud;
  #endif
  g_dist_lab = cloud_pos;
  #if TRACKING == NO
  g_dist_start_boost = g_dist_lab;
  #endif
  int status = store_or_save_cloud_pos(cloud_pos, cloud_vel, 0);
  if (status != 0) {
    printLog("Problem in store_or_save_cloud_pos!\n");
    QUIT_PLUTO(1);
  }
  scale = cloud_pos/cloud_pos_old;

  static double all_scales[2];
  double rIni        = g_inputParam[RINI]; // Enter cloud position in Rcl
  double mach        = g_inputParam[MACH];
  double rIniByrInj  = CC85pos(mach);

  double rByrInj_now  = (cloud_pos/rIni)*rIniByrInj;
  double rByrInj_old  = (cloud_pos_old/rIni)*rIniByrInj;
  // printLog("Debug: %.2e %.2e\n", rByrInj_old, rByrInj_now);
  double vx_factor    = (CC85vel(rByrInj_now)-CC85vel(rByrInj_old));
  // g_tmp = rByrInj_now-rByrInj_old;
  //g_tmp = CC85vel(rByrInj_now)-CC85vel(rByrInj_old);

  all_scales[0] = scale;
  all_scales[1] = vx_factor;

  return all_scales;
}
