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

void ApplyFrameBoost (const Data *d, Grid *grid)
{
  int i, j, k;
  double *r   = grid->x[IDIR];
  double *th  = grid->x[JDIR];
  double *phi = grid->x[KDIR];

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

  double vr_cloud, vth_cloud, vphi_cloud;
  TOT_LOOP(k,j,i){
    vr_cloud   =   vx_cloud*sin(th[j])*cos(phi[k]);
    vth_cloud  =   vx_cloud*cos(th[j])*cos(phi[k]);
    vphi_cloud = - vx_cloud*sin(phi[k]);

    d->Vc[iVR][k][j][i]    -= vr_cloud;
    d->Vc[iVTH][k][j][i]   -= vth_cloud;
    d->Vc[iVPHI][k][j][i]  -= vphi_cloud;

    /* Update the conservative variables */
    RBox dom_box;
    RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box);
    PrimToCons3D(d->Vc, d->Uc, &dom_box);
  }
}
