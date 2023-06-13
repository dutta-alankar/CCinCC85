/* ///////////////////////////////////////////////////////////////////// */
/*!
 *   \file
 *     \brief cloud tracking by shifting cells using tracer weighted position
 *
 *       \author Alankar Dutta
 *       \date   Mar 10, 2022
 *
 * ///////////////////////////////////////////////////////////////////// */
#include "pluto.h"
#include "local_pluto.h"

int store_or_save_cloud_pos(double position, double velocity, int save){
  static double cloud_pos = -1.0;
  static double cloud_vel = -1.0;
  if (g_stepNumber==0) {
    cloud_pos = g_inputParam[RINI];
    cloud_vel = 0.;
    g_dist_lab = cloud_pos;
    return 0;
  }
  if (save == 0 && g_stepNumber>0){
     cloud_pos = position;
     cloud_vel = velocity;
     g_dist_lab = cloud_pos;
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
    fclose(fp);
    return 0; // success
  }
  return -1; // error
}

double calc_scale(const Data *d, double dt, timeStep *Dts, Grid *grid)
/*!
 * Integrate cooling and reaction source terms.
 *
 * \param [in,out]  d     pointer to Data structure
 * \param [in]     dt     the time step to be taken
 * \param [out]    Dts    pointer to the Time_Step structure
 * \param [in]     grid   pointer to an array of Grid structures
 *
 * return scale_factor [double]
 *********************************************************************** */
{
  int i, j, k;
  double *r   = grid->x[IDIR];
  double *th  = grid->x[JDIR];
  double *phi = grid->x[KDIR];

  double scale = 0.;
  static int once = 0;
  static double cloud_vel  = -1.0;
  static double cloud_pos = -1.0;
  if (g_stepNumber==0) {
    cloud_pos = g_inputParam[RINI];
    cloud_vel = 0.;
  }
  if (cloud_pos==-1.0 && once==0) { // means we have restarted
    FILE *fp;
    char fname[512];
    int dummy;
    sprintf (fname, "%s/restart-cloud-props.out", RuntimeGet()->output_dir);
    fp = fopen(fname,"r");
    dummy = fscanf(fp, "%f\n", &cloud_pos);
    dummy = fscanf(fp, "%f\n", &cloud_vel);
    fclose(fp);
    once = 1;
  }

  double trc=0., vx_cloud=0.;
  double dV, vx_val;
  DOM_LOOP(k,j,i){
    dV = grid->dV[k][j][i]; // Cell volume
    trc         += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    vx_val = d->Vc[iVR][k][j][i]*sin(th[j])*cos(phi[k]) + d->Vc[iVPHI][k][j][i]*cos(th[j])*cos(phi[k]) - d->Vc[iVTH][k][j][i]*sin(phi[k]);
    vx_cloud    += d->Vc[RHO][k][j][i]*vx_val*d->Vc[TRC][k][j][i]*dV;
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

  cloud_pos += ( (cloud_vel + (cloud_vel + vx_cloud))*0.5*dt );
  cloud_vel += vx_cloud;
  store_or_save_cloud_pos(cloud_pos, cloud_vel, 0);

  scale = cloud_pos/g_inputParam[RINI];
  return scale;
}

void ApplyWindScaling (const Data *d, double dt, timeStep *Dts, Grid *grid, double scale)
/*!
 * Integrate cooling and reaction source terms.
 *
 * \param [in,out]  d     pointer to Data structure
 * \param [in]     dt     the time step to be taken
 * \param [out]    Dts    pointer to the Time_Step structure
 * \param [in]     grid   pointer to an array of Grid structures
 * \param [in]     double scale factor
 *
 *********************************************************************** */
{
  int i, j, k, nv;
  double *r   = grid->x[IDIR];
  double *th  = grid->x[JDIR];
  double *phi = grid->x[KDIR];

  // exp_P = Gamma * ed_exp_rho
  double cc85_exp[5] = {-2., -2.0*g_gamma, 0., -1., -1.};
  double vel_x, vel_y, vel_z;

  TOT_LOOP(k,j,i){
    vel_x = d->Vc[iVR][k][j][i]*sin(th[j])*cos(phi[k]) + d->Vc[iVTH][k][j][i]*cos(th[j])*cos(phi[k]) - d->Vc[iVPHI][k][j][i]*cos(phi[k]);
    vel_y = d->Vc[iVR][k][j][i]*sin(th[j])*sin(phi[k]) + d->Vc[iVTH][k][j][i]*cos(th[j])*sin(phi[k]) + d->Vc[iVPHI][k][j][i]*cos(phi[k]);
    vel_z = d->Vc[iVR][k][j][i]*sin(th[j])*sin(phi[k]) + d->Vc[iVTH][k][j][i]*cos(th[j])*sin(phi[k]) + d->Vc[iVPHI][k][j][i]*cos(phi[k]);
    vel_x     *= pow(scale, cc85_exp[2]);
    vel_y     *= pow(scale, cc85_exp[3]);
    vel_z     *= pow(scale, cc85_exp[4]);

    d->Vc[RHO][k][j][i]     *= pow(scale, cc85_exp[0]);
    d->Vc[PRS][k][j][i]     *= pow(scale, cc85_exp[1]);

    d->Vc[iVR][k][j][i]   =   vel_x*sin(th[j])*cos(phi[k]) + vel_y*sin(th[j])*sin(phi[k]) + vel_z*cos(th[j]);
    d->Vc[iVTH][k][j][i]  =   vel_x*cos(th[j])*cos(phi[k]) + vel_y*cos(th[j])*sin(phi[k]) - vel_z*sin(th[j]);
    d->Vc[iVPHI][k][j][i] = - vel_x*sin(phi[k]) + vel_y*cos(phi[k]);

    d->Vc[TRC][k][j][i]     *= 1.;

    /* Update the conservative variables */
    RBox dom_box;
    RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box);
    PrimToCons3D(d->Vc, d->Uc, &dom_box);
  }
}
