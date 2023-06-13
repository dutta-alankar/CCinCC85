/* ----------- Auto generated from generateCatalystAdaptor.py -----------------
Created on Mon May  8 16:57:46 2023

@author: alankar                                                                */

#include <catalyst.h>
#include <stdio.h>
#include <math.h>
#include "pluto.h"

//-----------------------------------------------------------------------------
/**
 * Initialize Catalyst.
 */
//-----------------------------------------------------------------------------
void do_catalyst_initialization(int scripts, char** pipeline_script)
{
  conduit_node* catalyst_init_params = conduit_node_create();
  // pass scripts pass on command line.
  char buf[1024];
  int i;
  for (i=0; i<scripts; i++){
    snprintf(buf, 256, "catalyst/scripts/script%d", i);
    conduit_node_set_path_char8_str(catalyst_init_params, buf, pipeline_script[i]);
  }
  conduit_node_set_path_char8_str(catalyst_init_params, "catalyst_load/implementation", "paraview");
  conduit_node_set_path_char8_str(catalyst_init_params, "catalyst_load/search_paths/paraview", PARAVIEW_IMPL_DIR);
  enum catalyst_status err = catalyst_initialize(catalyst_init_params);
  conduit_node_destroy(catalyst_init_params);
  if (err != catalyst_status_ok)
  {
    printf("Failed to initialize Catalyst: %d\n", err);
  }
}

//-----------------------------------------------------------------------------
/**
 * Execute per cycle
 */
//-----------------------------------------------------------------------------
void do_catalyst_execute(int cycle, double time, Grid* grid, Data* d)
{
  /*   Conversion to Conduit (catalyst) compatible data arrangement   */

  unsigned int i, j, k;
  static unsigned int initialized = 0;
  unsigned int counter = 0;

  static double *xp, *yp, *zp;
  static uint64_t *CellConn;
  const uint64_t numCells = grid->np_tot[IDIR]*grid->np_tot[JDIR]*grid->np_tot[KDIR];
  const uint64_t numPoints[3] = {grid->np_tot[IDIR]+1, grid->np_tot[JDIR]+1, grid->np_tot[KDIR]+1};

  //double ***temperature  = GetUserVar("temperature");
  //ComputeUserVar (d, grid);

  if (initialized==0){
    xp = (double *)malloc((grid->np_tot[IDIR]+1) * (grid->np_tot[JDIR]+1) * (grid->np_tot[KDIR]+1) * sizeof(double));
    yp = (double *)malloc((grid->np_tot[IDIR]+1) * (grid->np_tot[JDIR]+1) * (grid->np_tot[KDIR]+1) * sizeof(double));
    zp = (double *)malloc((grid->np_tot[IDIR]+1) * (grid->np_tot[JDIR]+1) * (grid->np_tot[KDIR]+1) * sizeof(double));
    CellConn   = (uint64_t*)malloc(8 * numCells * sizeof(int64_t));

    for(k=0; k<grid->np_tot[KDIR]; k++)
    {
      for(j=0; j<grid->np_tot[JDIR]; j++)
      {
        for(i=0; i<grid->np_tot[IDIR]; i++)
        {
          //cell_count = k * grid->np_tot[IDIR] * grid->np_tot[JDIR] + j * grid->np_tot[IDIR] + i;
          CellConn[counter++] =     k * numPoints[JDIR]*numPoints[IDIR] +     j * numPoints[IDIR] + i;

          CellConn[counter++] = (k+1) * numPoints[JDIR]*numPoints[IDIR] +     j * numPoints[IDIR] + i;

          CellConn[counter++] = (k+1) * numPoints[JDIR]*numPoints[IDIR] + (j+1) * numPoints[IDIR] + i;

          CellConn[counter++] =     k * numPoints[JDIR]*numPoints[IDIR] + (j+1) * numPoints[IDIR] + i;;

          CellConn[counter++] =     k * numPoints[JDIR]*numPoints[IDIR] +     j * numPoints[IDIR] + i+1;

          CellConn[counter++] = (k+1) * numPoints[JDIR]*numPoints[IDIR] +     j * numPoints[IDIR] + i+1;

          CellConn[counter++] = (k+1) * numPoints[JDIR]*numPoints[IDIR] + (j+1) * numPoints[IDIR] + i+1;

          CellConn[counter++] =     k * numPoints[JDIR]*numPoints[IDIR] + (j+1) * numPoints[IDIR] + i+1;
        }
      }
    }
  }

  counter = 0;
  double x1, x2, x3;
  for (k = 0; k<=grid->np_tot[KDIR]; k++){
    for (j = 0; j<=grid->np_tot[JDIR]; j++){
      for (i = 0; i<=grid->np_tot[IDIR]; i++){
        x1 = (i!=grid->np_tot[IDIR])?grid->xl[IDIR][i]:grid->xr[IDIR][i-1];
        x2 = (j!=grid->np_tot[JDIR])?grid->xl[JDIR][j]:grid->xr[JDIR][j-1];
        x3 = (k!=grid->np_tot[KDIR])?grid->xl[KDIR][k]:grid->xr[KDIR][k-1];

	#if GEOMETRY==CARTESIAN || GEOMETRY == CYLINDRICAL
	DIM_EXPAND(
        xp[counter]   = x1;,
        yp[counter]   = x2;,
        zp[counter]   = x3;
        )
	#elif GEOMETRY==SPHERICAL
	  #if DIMENSIONS <= 2
	DIM_EXPAND(
	xp[counter] = x1*sin(x2);,
	yp[counter] = x1*cos(x2);,
	zp[counter] = 0.;
	)
	  #else
	DIM_EXPAND(
        xp[counter]   = x1*sin(x2)*cos(x3);,
        yp[counter]   = x1*sin(x2)*sin(x3);,
        zp[counter]   = x1*cos(x2);
        )
          #endif
        #elif GEOMETRY==POLAR
	DIM_EXPAND(
        xp[counter]   = x1*cos(x2);,
        yp[counter]   = x1*sin(x2);,
        zp[counter]   = x3;
        )
        #else
        printLog ("! CatalystAdaptor: Unknown geometry\n");
        QUIT_PLUTO(1);
	#endif
	counter++;
      }
    }
  }
  counter = 0;

  /*   setup conduit for catalyst   */
  conduit_node* catalyst_exec_params = conduit_node_create();
  conduit_node_set_path_int64(catalyst_exec_params, "catalyst/state/timestep", cycle);
  conduit_node_set_path_int64(catalyst_exec_params, "catalyst/state/cycle", cycle);
  conduit_node_set_path_float64(catalyst_exec_params, "catalyst/state/time", time);

  conduit_node_set_path_char8_str(catalyst_exec_params, "catalyst/channels/grid/type", "mesh");
  conduit_node* mesh = conduit_node_create();

  // add coordsets
  conduit_node_set_path_char8_str(mesh, "coordsets/coords/type", "explicit");

  conduit_node_set_path_external_float64_ptr(mesh, "coordsets/coords/values/X", xp, numPoints[IDIR]*numPoints[JDIR]*numPoints[KDIR]);
  conduit_node_set_path_external_float64_ptr(mesh, "coordsets/coords/values/Y", yp, numPoints[IDIR]*numPoints[JDIR]*numPoints[KDIR]);
  conduit_node_set_path_external_float64_ptr(mesh, "coordsets/coords/values/Z", zp, numPoints[IDIR]*numPoints[JDIR]*numPoints[KDIR]);

  // add topologies
  conduit_node_set_path_char8_str(mesh, "topologies/mesh/type", "unstructured");
  conduit_node_set_path_char8_str(mesh, "topologies/mesh/coordset", "coords");
  conduit_node_set_path_char8_str(mesh, "topologies/mesh/elements/shape", "hex");
  conduit_node_set_path_external_int64_ptr(mesh, "topologies/mesh/elements/connectivity", CellConn, numCells * 8);

  // add density (cell-field)
  conduit_node_set_path_char8_str(mesh, "fields/density/association", "element");
  conduit_node_set_path_char8_str(mesh, "fields/density/topology", "mesh");
  conduit_node_set_path_char8_str(mesh, "fields/density/volume_dependent", "false");
  conduit_node_set_path_external_float64_ptr(mesh, "fields/density/values", /*density */(double *)(**d->Vc[RHO]), numCells );

  // add pressure (cell-field)
  conduit_node_set_path_char8_str(mesh, "fields/pressure/association", "element");
  conduit_node_set_path_char8_str(mesh, "fields/pressure/topology", "mesh");
  conduit_node_set_path_char8_str(mesh, "fields/pressure/volume_dependent", "false");
  conduit_node_set_path_external_float64_ptr(mesh, "fields/pressure/values", /*pressure */(double *)(**d->Vc[PRS]), numCells );

  // add vr (cell-field)
  conduit_node_set_path_char8_str(mesh, "fields/vr/association", "element");
  conduit_node_set_path_char8_str(mesh, "fields/vr/topology", "mesh");
  conduit_node_set_path_char8_str(mesh, "fields/vr/volume_dependent", "false");
  conduit_node_set_path_external_float64_ptr(mesh, "fields/vr/values", /*vr */(double *)(**d->Vc[iVR]), numCells );

  // add vth (cell-field)
  conduit_node_set_path_char8_str(mesh, "fields/vth/association", "element");
  conduit_node_set_path_char8_str(mesh, "fields/vth/topology", "mesh");
  conduit_node_set_path_char8_str(mesh, "fields/vth/volume_dependent", "false");
  conduit_node_set_path_external_float64_ptr(mesh, "fields/vth/values", /*vth */(double *)(**d->Vc[iVTH]), numCells );

  // add vphi (cell-field)
  conduit_node_set_path_char8_str(mesh, "fields/vphi/association", "element");
  conduit_node_set_path_char8_str(mesh, "fields/vphi/topology", "mesh");
  conduit_node_set_path_char8_str(mesh, "fields/vphi/volume_dependent", "false");
  conduit_node_set_path_external_float64_ptr(mesh, "fields/vphi/values", /*vphi */(double *)(**d->Vc[iVPHI]), numCells );

  // add tr1 (cell-field)
  conduit_node_set_path_char8_str(mesh, "fields/tr1/association", "element");
  conduit_node_set_path_char8_str(mesh, "fields/tr1/topology", "mesh");
  conduit_node_set_path_char8_str(mesh, "fields/tr1/volume_dependent", "false");
  conduit_node_set_path_external_float64_ptr(mesh, "fields/tr1/values", /*tr1 */(double *)(**d->Vc[TRC]), numCells );

  ComputeUserVar (d, grid);

  // add temperature (cell-field)
  double ***temperature  = GetUserVar("temperature");
  conduit_node_set_path_char8_str(mesh, "fields/temperature/association", "element");
  conduit_node_set_path_char8_str(mesh, "fields/temperature/topology", "mesh");
  conduit_node_set_path_char8_str(mesh, "fields/temperature/volume_dependent", "false");
  conduit_node_set_path_external_float64_ptr(mesh, "fields/temperature/values", /*temperature */(double *)(**temperature), numCells );

  // add ndens (cell-field)
  double ***ndens  = GetUserVar("ndens");
  conduit_node_set_path_char8_str(mesh, "fields/ndens/association", "element");
  conduit_node_set_path_char8_str(mesh, "fields/ndens/topology", "mesh");
  conduit_node_set_path_char8_str(mesh, "fields/ndens/volume_dependent", "false");
  conduit_node_set_path_external_float64_ptr(mesh, "fields/ndens/values", /*ndens */(double *)(**ndens), numCells );

  // add mach (cell-field)
  double ***mach  = GetUserVar("mach");
  conduit_node_set_path_char8_str(mesh, "fields/mach/association", "element");
  conduit_node_set_path_char8_str(mesh, "fields/mach/topology", "mesh");
  conduit_node_set_path_char8_str(mesh, "fields/mach/volume_dependent", "false");
  conduit_node_set_path_external_float64_ptr(mesh, "fields/mach/values", /*mach */(double *)(**mach), numCells );

  // add the mesh info (conduit mesh) to catalyst_exec_params
  conduit_node_set_path_external_node(catalyst_exec_params, "catalyst/channels/grid/data", mesh);

  #ifdef CATALYST_DEBUG
  // print for debugging purposes, if needed
  conduit_node_print(catalyst_exec_params);

  // print information with details about memory allocation
  conduit_node* info = conduit_node_create();
  conduit_node_info(catalyst_exec_params, info);
  conduit_node_print(info);
  conduit_node_destroy(info);
  #endif

  initialized = 1;
  enum catalyst_status err = catalyst_execute(catalyst_exec_params);
  if (err != catalyst_status_ok)
  {
    printf("Failed to execute Catalyst: %d\n", err);
  }
  conduit_node_destroy(catalyst_exec_params);
  conduit_node_destroy(mesh);
}

//-----------------------------------------------------------------------------
/**
 * Finalize Catalyst.
 */
//-----------------------------------------------------------------------------
void do_catalyst_finalization()
{
  conduit_node* catalyst_fini_params = conduit_node_create();
  enum catalyst_status err = catalyst_finalize(catalyst_fini_params);
  if (err != catalyst_status_ok)
  {
    printf("Failed to execute Catalyst: %d\n", err);
  }
  conduit_node_destroy(catalyst_fini_params);
}
