/* ///////////////////////////////////////////////////////////////////// */
/*!
 *   \file
 *     \brief cloud tracking by frame boost
 *
 *       \author Alankar Dutta
 *       \date   Jun 22, 2023
 *
 * ///////////////////////////////////////////////////////////////////// */
#include "pluto.h"
#include "local_pluto.h"

void ApplyFrameBoost (const Data *d, Grid *grid, double dt) {
  int i, j, k;
  static int boost_on = 0;

  double start = BOOST_START;

  double trc=0., vx_cloud=0.;
  double dV;
  DOM_LOOP(k,j,i){
    dV = grid->dV[k][j][i]; // Cell volume
    trc         += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    vx_cloud    += d->Vc[RHO][k][j][i]*d->Vc[VX1][k][j][i]*d->Vc[TRC][k][j][i]*dV; // TODO: Try tracking with left edge of cloud
  }
  #ifdef PARALLEL
  int transfer_size = 2;
  int transfer = 0;
  double sendArray[transfer_size], recvArray[transfer_size];
  sendArray[transfer++] = trc; sendArray[transfer++] = vx_cloud;

  MPI_Allreduce (sendArray, recvArray, transfer_size, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
  transfer = 0;
  trc = recvArray[transfer++]; vx_cloud = recvArray[transfer++];
  #endif
  vx_cloud = vx_cloud/trc;

  #if TRACKING != NO
  double chi = g_inputParam[CHI];
  double tcc = sqrt(chi);
  if (g_time >= start*tcc) {
    boost_on = 1;
    TOT_LOOP(k,j,i) {
      d->Vc[VX1][k][j][i] -= vx_cloud;
      /* Update the conservative variables */
      RBox dom_box;
      RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box);
      PrimToCons3D(d->Vc, d->Uc, &dom_box);
    }
  }
  #endif

  int status = calc_cloud_pos(vx_cloud, dt, start, 0);
  if (boost_on == 0)
    g_dist_start_boost = g_dist_lab;
  return;
}

int calc_cloud_pos(double velocity, double dt, double start, int save) {
  static double cloud_pos = -1.0;
  static double cloud_vel = -1.0;
  static int once = 0;
  static int first_time_boost = 1;

  double chi = g_inputParam[CHI];
  double tcc = sqrt(chi);

  if (g_stepNumber==0) {
    once = 1;
    cloud_pos = g_inputParam[RINI];
    cloud_vel = 0.;
    g_dist_lab = cloud_pos;
    if (save == 0)
      return 0;
  }
  if (save == 0 && g_stepNumber>0){
     #if TRACKING != NO
     if (g_time >= start*tcc) {
       if (first_time_boost == 1) {
         cloud_pos += ( (cloud_vel + velocity)*0.5*dt );
         cloud_vel = velocity;
         first_time_boost = 0;
       }
       else {
         cloud_pos += ( (cloud_vel + (cloud_vel + velocity))*0.5*dt );
         cloud_vel += velocity;
       }
       g_boost_vel = cloud_vel;
     }
     else {
       cloud_pos += ( (cloud_vel + velocity)*0.5*dt );
       cloud_vel = velocity;
     }
     #else
     cloud_pos += ( (cloud_vel + velocity)*0.5*dt );
     cloud_vel = velocity;
     #endif
     g_dist_lab = cloud_pos;
     once = 1;
     return 0; // success
  }
  if (save == 1 && once==1){
    FILE *fp;
    char fname[512];
    int dummy;
    sprintf (fname, "%s/restart-cloud-props.out", RuntimeGet()->output_dir);
    fp = fopen(fname,"w");
    fprintf(fp, "%f\n", cloud_pos);
    fprintf(fp, "%f\n", cloud_vel);
    fclose(fp);
    return 0; // success
  }
  if (once==0) { // means we have restarted
    FILE *fp;
    char fname[512];
    int dummy;
    sprintf (fname, "%s/restart-cloud-props.out", RuntimeGet()->output_dir);
    fp = fopen(fname,"r");
    dummy = fscanf(fp, "%f\n", &cloud_pos);
    dummy = fscanf(fp, "%f\n", &cloud_vel);
    fclose(fp);
    g_dist_lab = cloud_pos;
    once = 1;
    if (g_time >= start*tcc)
      first_time_boost = 0;
    return 0;
  }
  return -1; // error
}
