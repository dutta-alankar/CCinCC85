#include "pluto.h"
#include "local_pluto.h"

/* *************************************************************** */
void ComputeUserVar (const Data *d, Grid *grid)
/*
 *
 *  PURPOSE
 *
 *    Define user-defined output variables
 *
 *
 *
 ***************************************************************** */
{
  int i,j,k;
  double ***temperature  = GetUserVar("temperature");
  double ***ndens  = GetUserVar("ndens");
  double ***mach   = GetUserVar("mach");
  double ***celldV = GetUserVar("cellvol");

  #if COOLING==NO || COOLING==TABULATED || COOLING==TOWNSEND
  double dummy[4];
  double mu = MeanMolecularWeight((double*)d->Vc, dummy);
  #else
  double mu = MeanMolecularWeight((double*)d->Vc);
  #endif

  TOT_LOOP(k,j,i) {
      temperature[k][j][i]  = (d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i])*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/CONST_kB;
      ndens[k][j][i] = d->Vc[RHO][k][j][i]*UNIT_DENSITY/(CONST_mp*mu);
      mach[k][j][i]  = sqrt( DIM_EXPAND(d->Vc[VX1][k][j][i]*d->Vc[VX1][k][j][i],
                                        + d->Vc[VX2][k][j][i]*d->Vc[VX2][k][j][i],
                                        + d->Vc[VX3][k][j][i]*d->Vc[VX3][k][j][i]) )/sqrt(g_gamma*(d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i]));
      celldV[k][j][i] = grid->dV[k][j][i];
  } /* DOM_LOOP(k,j,i) */
}
/* ************************************************************* */
void ChangeOutputVar ()
/*
 *
 *
 *************************************************************** */
{

/*
  Image *image;

  //SetOutputVar("bx1", FLT_OUTPUT, NO);
  SetOutputVar("rho", PNG_OUTPUT, YES);
  SetOutputVar("T", PNG_OUTPUT, YES);
  SetOutputVar("tr1", PNG_OUTPUT, YES);
  SetOutputVar("prs", PNG_OUTPUT, YES);
  //SetOutputVar("vortz", PNG_OUTPUT, YES);

  image = GetImage ("rho");
  image->slice_plane = X12_PLANE;
  image->slice_coord = 0.;
  //image->max = image->min = 0.0;
  image->logscale = 1;
  image->colormap = "red";

  image = GetImage ("prs");
  image->slice_plane = X12_PLANE;
  image->slice_coord = 0.;
  //image->max = image->min = 0.0;
  image->logscale = 1;
  image->colormap = "red";

  image = GetImage ("T");
  image->slice_plane = X12_PLANE;
  image->slice_coord = 0.;
  //image->max = image->min = 0.0;
  image->logscale = 1;
  image->colormap = "red";

  image = GetImage ("tr1");
  image->slice_plane = X12_PLANE;
  image->slice_coord = 0.;
  //image->max = image->min = 0.0;
  image->logscale = 1;
  image->colormap = "red";
  */

#ifdef PARTICLES
  //SetOutputVar ("energy",PARTICLES_FLT_OUTPUT, NO);
//  SetOutputVar ("x1",    PARTICLES_FLT_OUTPUT, NO);
  //SetOutputVar ("vx1",   PARTICLES_FLT_OUTPUT, NO);
#endif

}
