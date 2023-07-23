#include "pluto.h"
#include "local_pluto.h"
#include "wind.h"

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
  double *x   = grid->x[IDIR];
  double *y   = grid->x[JDIR];
  double *z   = grid->x[KDIR];

  double ***temp            = GetUserVar("temperature");
  double ***ndens           = GetUserVar("ndens");
  double ***mach            = GetUserVar("mach");
  double ***celldV          = GetUserVar("cellvol");
  double ***delTbyTwind     = GetUserVar("delTbyTwind");
  double ***delRhoByRhoWind = GetUserVar("delRhoByRhoWind");

  double rIni        = g_inputParam[RINI]; // cloud position in units of Rcl
  double mach_ini    = g_inputParam[MACH];
  double chi         = g_inputParam[CHI];
  double rIniByrInj  = CC85pos(mach_ini);

  double rByrInj;
  double rho_wind, T_wind;

  #if COOLING==NO || COOLING==TABULATED || COOLING==TOWNSEND
  double dummy[4];
  double mu = MeanMolecularWeight((double*)d->Vc, dummy);
  #else
  double mu = MeanMolecularWeight((double*)d->Vc);
  #endif

  double Tcutoff = 1.0e+04;
  double Tmax    = 1.0e+08;
  double Tcl     = pow(UNIT_VELOCITY/mach_ini,2)*(mu*CONST_mp)/(g_gamma*CONST_kB*chi); //in K just Twind/chi

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

  rho_wind = 1.0*pow(g_dist_lab/g_inputParam[RINI], -2);
  T_wind = MIN(MAX(chi*Tcl*pow(g_dist_lab/g_inputParam[RINI], -2*(g_gamma-1)), Tcutoff), Tmax);

  TOT_LOOP(k,j,i) {
      double vx_lab = d->Vc[VX1][k][j][i] + g_boost_vel;
      temp[k][j][i]  = (d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i])*pow(UNIT_VELOCITY,2)*(CONST_mp*mu)/CONST_kB;
      ndens[k][j][i] = d->Vc[RHO][k][j][i]*UNIT_DENSITY/(CONST_mp*mu);
      mach[k][j][i]  = sqrt( DIM_EXPAND(vx_lab*vx_lab, + d->Vc[VX2][k][j][i]*d->Vc[VX2][k][j][i], + d->Vc[VX3][k][j][i]*d->Vc[VX3][k][j][i]) )/sqrt(g_gamma*(d->Vc[PRS][k][j][i]/d->Vc[RHO][k][j][i]));
      celldV[k][j][i] = grid->dV[k][j][i];

      double x_val = x[i] + (g_dist_lab-g_dist_start_boost);
      rByrInj  = (x_val/rIni)*rIniByrInj;
      delTbyTwind[k][j][i] = (temp[k][j][i] - T_wind)/T_wind;
      delRhoByRhoWind[k][j][i] = (d->Vc[RHO][k][j][i] - rho_wind)/rho_wind;
  } /* TOT_LOOP(k,j,i) */
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
  //SetOutputVar ("x1",    PARTICLES_FLT_OUTPUT, NO);
  //SetOutputVar ("vx1",   PARTICLES_FLT_OUTPUT, NO);
#endif

}
