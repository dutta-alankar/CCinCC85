/* ///////////////////////////////////////////////////////////////////// */
/*!
  \file
  \brief Include source terms using operator splitting.

  The SplitSource() function handles source terms in a separate
  step using operator splitting.
  It is called from Integrate() between standard hydro advances.
  At present these source terms are one or more of the following:

  - optically thin radiative losses (cooling)
  - Diffusion operators:
    - resistivity
    - Thermal conduction
    - Viscosity
  - additional user-defined terms may also be included here.

  \authors A. Mignone (mignone@ph.unito.it)
  \date    Oct 26, 2016
*/
/* ///////////////////////////////////////////////////////////////////// */
#include "pluto.h"
#include "local_pluto.h"

/* ********************************************************************* */
void SplitSource (const Data *d, double dt, timeStep *Dts, Grid *grid)
/*!
 *  Take one step on operator-split source terms.
 *
 *  \param [in,out] d   pointer to PLUTO Data structure containing
 *                      the solution array updated from the most
 *                      recent call
 *  \param[in]      dt  the time step used to integrate the source
 *                      terms
 *  \param[in]     Dts  pointer to the time step structure
 *  \param[in]    grid  pointer to an array of grid structures
 *
 *********************************************************************** */
{
  double vx_cloud = transform_velocity(d, grid);

  #if SCALING != NO
  double *all_scales = calc_scale(vx_cloud, dt);
  ApplyWindScaling(d, grid, all_scales);
  #endif

  #if TRACKING != NO
  ApplyFrameBoost (d, grid, vx_cloud);
  #else
  g_boost_vel = 0.;
  #endif

/*  ---------------------------------------------
             Cooling/Heating losses
    ---------------------------------------------  */

#if COOLING != NO
  #if COOLING == POWER_LAW  /* -- solve exactly -- */
  PowerLawCooling (d->Vc, dt, Dts, grid);
  #elif COOLING == KROME /* -- Interfaced krome solvers -- */
  KromeCooling (d, dt, Dts, grid);
  #else
  CoolingSource (d, dt, Dts, grid);
  #endif
#endif

/* ----------------------------------------------
    Parabolic terms using STS:

    - resistivity
    - thermal conduction
    - viscosity
   ---------------------------------------------- */

#if (PARABOLIC_FLUX & SUPER_TIME_STEPPING)
  STS (d, dt, Dts, grid);
#endif

#if (PARABOLIC_FLUX & RK_LEGENDRE)
  RKL (d, dt, Dts, grid);
#endif

}
