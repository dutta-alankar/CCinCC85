/* ///////////////////////////////////////////////////////////////////// */
/*!
 *   \file
 *     \brief cloud tracking by frame boost
 *
 *       \author Alankar Dutta
 *       \date   Jun 8, 2023
 *
 * ///////////////////////////////////////////////////////////////////// */
#include "pluto.h"
#include "local_pluto.h"

double ApplyFrameBoost (const Data *d, Grid *grid)
{
  int i, j, k;

  double trc=0., vx_cloud=0.;
  double dV;
  DOM_LOOP(k,j,i){
    dV = grid->dV[k][j][i]; // Cell volume
    trc         += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    vx_cloud    += d->Vc[RHO][k][j][i]*d->Vc[VX1][k][j][i]*d->Vc[TRC][k][j][i]*dV;
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

  TOT_LOOP(k,j,i){
    d->Vc[VX1][k][j][i]    -= vx_cloud;
    /* Update the conservative variables */
    RBox dom_box;
    RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box);
    PrimToCons3D(d->Vc, d->Uc, &dom_box);
  }
  return vx_cloud;
}
