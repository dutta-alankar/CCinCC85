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
  double ***temp   = GetUserVar("temperature");
  double ***ndens  = GetUserVar("ndens");
  double ***mach   = GetUserVar("mach");
  double ***celldV = GetUserVar("cellvol");
  /*
  double ***rtld  = GetUserVar("rtld");
  double ***ptld  = GetUserVar("ptld");
  double ***rhotld  = GetUserVar("rhotld");
  double ***vtld  = GetUserVar("vtld");
  */
  int yr = 365*24*60*60;
  // double Edot  = g_inputParam[ALPHA]*g_inputParam[EDINJ]/(UNIT_DENSITY*pow(UNIT_LENGTH,2)*pow(UNIT_VELOCITY,3)); // Enter energy injection rate in erg/s
  // double Mdot  = g_inputParam[BETA]*g_inputParam[MDINJ]*(CONST_Msun/yr)/(UNIT_DENSITY*pow(UNIT_LENGTH,2)*UNIT_VELOCITY);  // Enter mass injection rate in Msun/yr
  // double RInj  = g_inputParam[RINJ]*CONST_pc/UNIT_LENGTH; //Injection radius in pc
  /*
  double rho_norm = pow(Mdot,  3/2.)*pow(Edot, -1/2.)*pow(RInj, -2);
  double prs_norm = pow(Mdot,  1/2.)*pow(Edot,  1/2.)*pow(RInj, -2);
  double vel_norm = pow(Mdot, -1/2.)*pow(Edot,  1/2.);
  */
  #if COOLING==NO || COOLING==TABULATED || COOLING==TOWNSEND
  double dummy[4];
  double mu = MeanMolecularWeight((double*)d->Vc, dummy);
  #else
  double mu = MeanMolecularWeight((double*)d->Vc);
  #endif
  /*
  double *r   = grid->x[IDIR];
  double *th  = grid->x[JDIR];
  double *phi = grid->x[KDIR];
  */
  TOT_LOOP(k,j,i) {
      temp[k][j][i]  = (d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i])*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/CONST_kB;
      ndens[k][j][i] = d->Vc[RHO][k][j][i]*UNIT_DENSITY/(CONST_mp*mu);
      mach[k][j][i]  = sqrt( DIM_EXPAND(d->Vc[iVR][k][j][i]*d->Vc[iVR][k][j][i], + d->Vc[iVTH][k][j][i]*d->Vc[iVTH][k][j][i], + d->Vc[iVPHI][k][j][i]*d->Vc[iVPHI][k][j][i]) )/sqrt(g_gamma*(d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i]));
      celldV[k][j][i] = grid->dV[k][j][i];
      /*
      double distance = r[i];

      rtld[k][j][i]   = distance/RInj;
      rhotld[k][j][i] = d->Vc[RHO][k][j][i]/rho_norm;
      ptld[k][j][i]   = d->Vc[PRS][k][j][i]/prs_norm;
      vtld[k][j][i]   = sqrt( DIM_EXPAND(d->Vc[iVR][k][j][i]*d->Vc[iVR][k][j][i], + d->Vc[iVTH][k][j][i]*d->Vc[iVTH][k][j][i], + d->Vc[iVPHI][k][j][i]*d->Vc[iVPHI][k][j][i]) )/vel_norm;
      */
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