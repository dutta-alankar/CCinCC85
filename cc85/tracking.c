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
#include "wind.h"

void ApplyTracking (const Data *d, Grid *grid, Runtime *runtime, cmdLine *cmd_line)
{
  int i, j, k, nv, ip;
  double distance;
  int yr = 365*24*60*60;

  double rIni        = g_inputParam[RINI]; // cloud position in units of Rcl
  double thIni       = g_inputParam[THINI]*CONST_PI/180;
  double phiIni      = g_inputParam[PHIINI]*CONST_PI/180;
  double chi         = g_inputParam[CHI];
  double mach        = g_inputParam[MACH];
  double rIniByrInj  = CC85pos(mach);

  static double track_pos;
  double delta = 0.;
  
  // XXX: track_pos position of cloud at the last tracking step  
  if (g_stepNumber==0)
    track_pos = rIni;
  else
    delta = g_dist_lab-track_pos; /* g_dist_lab is updated at every step in main.c */
  g_tracking = delta;
  /*
  double dV, trc =0.;
  if (g_stepNumber == 0 || g_stepNumber == 100 || g_stepNumber == 200)  {
    // XXX: Initial tracer value
    DOM_LOOP(k,j,i) {
      dV = grid->dV[k][j][i]; // Cell volume
      trc += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
    }
    #ifdef PARALLEL
    double tmp;
    MPI_Allreduce (&trc, &tmp, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    trc = tmp;
    #endif
    printLog("Initial: step %d; Track_pos=%f Pos_now=%f, trc_min=%f, left_dom=%f\n", g_stepNumber, track_pos, g_dist_lab, g_trctrack, grid->xbeg_glob[IDIR]);
    printLog("Initial: step %d; t=%f; M_trc = %f\n", g_stepNumber, g_time, trc); 
  }
  */
  
  static int once = 0;
  if(cmd_line->h5restart == YES && once == 0){
    once = 1;
    int nrestart = cmd_line->nrestart;
    char fout[512], str[512];
    FILE* fbin;
    sprintf (fout,"%s/dbl.h5.out",runtime->output_dir);
    fbin = fopen (fout, "r");
    if (fbin == NULL){
      print ("! ApplyTracking(): cannot find dbl.h5.out\n");
      QUIT_PLUTO(1);
    }
    int nlines = 0;
    while (fgets(str, 512, fbin) != 0) nlines++;  /* -- count lines in dbl.h5.out -- */
    rewind(fbin);
    fclose(fbin);
    if (nrestart > nlines-1){
      print ("! ApplyTracking(): output #%d does not exist in file %s\n",
             nrestart, fout);
      QUIT_PLUTO(1);
    }
    nrestart = (nrestart >= 0 ? nrestart:(nlines+nrestart));
    if (nrestart < 0){
      print ("! ApplyTracking(): output #%d does not exist in file %s\n",
             nrestart, fout);
      QUIT_PLUTO(1);
    }
    FILE *fp;
    char fname[512];
    int dummy;
    double skip;
    sprintf (fname, "%s/restart-data.%04d.out", runtime->output_dir, nrestart);
    //print("Restart shift file: %s\n", fname);
    fp = fopen(fname, "r");
    dummy = fscanf(fp, "%lf", &skip);
    dummy = fscanf(fp, "%lf", &g_tracking);
    fclose(fp);
    delta = g_tracking;
    track_pos = g_dist_lab - delta;
  }
  
  if (g_stepNumber == 0) return;

  double *r   = grid->x[IDIR];
  double *th  = grid->x[JDIR];
  double *phi = grid->x[KDIR];

  double *dr   = grid->dx[IDIR];
  double *dth  = grid->dx[JDIR];
  double *dphi = grid->dx[KDIR];

  if ( fabs(g_trctrack - grid->xbeg_glob[IDIR]) < g_inputParam[BUFFER_TRACK] ) { // edge is BUFFER_TRACK * Rcl from boundary 
    track_pos = g_dist_lab;
    return;
  }
  /*
  printLog("step:%d; Track cond satisfied! Track_pos_before=%f Pos_now=%f, trc_min=%f, left_dom=%f\n", g_stepNumber, track_pos, g_dist_lab, g_trctrack, grid->xbeg_glob[IDIR]);
  trc = 0.;
  DOM_LOOP(k,j,i) {
    dV = grid->dV[k][j][i]; // Cell volume
    trc += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
  }
  #ifdef PARALLEL
  double tmp;
  MPI_Allreduce (&trc, &tmp, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
  trc = tmp;
  #endif
  printLog("Track cond satisfied but below shift thres!: step %d; t=%f; M_trc = %f\n", g_stepNumber, g_time, trc);
  // printLog("step:%d; Track cond satisfied!\n", g_stepNumber);
  */
  /* Assuming uniform grid */
  int shift_cells = 0;
  //if (delta >= 0)
  shift_cells =  (int)floor(delta/dr[IBEG]) ; // Cloud movement: pos: --> right & neg: <-- left
  //else
  //   shift_cells =  (int)ceil(delta/dr[IBEG]) ;
  int shift_thres = MIN(1,grid->nghost[IDIR]-g_ghost_true); //flooring creates a small overshoot error in fixing cloud position
  
  if (fabs(shift_cells)<shift_thres) return;
  #if VERBOSE != NO
  else
    printLog("step:%d time:%.3e; Applying cloud tracking: cells_shift=%d; shift_thres=%d\n",g_stepNumber, g_time, shift_cells, shift_thres);
  #endif
  /*
  // XXX: Tracking starts now but tracking steps not executed
  trc =0.;
  DOM_LOOP(k,j,i){
    dV = grid->dV[k][j][i]; // Cell volume
    trc += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
  }
  #ifdef PARALLEL
  MPI_Allreduce (&trc, &tmp, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
  trc = tmp;
  #endif
  printLog("Before Tracking: step %d; t=%f; M_trc = %f\n", g_stepNumber, g_time, trc); 
  */
  // printLog("step:%d; Applying cloud tracking: cells_shift=%d; shift_thres=%d\n",g_stepNumber, shift_cells, shift_thres);
  double shift_val = shift_cells*dr[IBEG]; //uniform grid assumption
  track_pos += shift_val; //this auto corrects the small overshoot in the next step as delta is neg in next step

  //printLog("Shift val = %lf\tTotal Shift val = %lf\n", shift_val, g_tot_shift_val);
  g_tot_shift_val = g_tot_shift_val + shift_val; 
  /*
  for (ip = 1; ip <= runtime->npatch[IDIR]+1; ip++) 
    printLog("Before Step %d: runtime->patch_left_node = %f, shift_val=%f\n", g_stepNumber, runtime->patch_left_node[IDIR][ip], shift_val);
  */

  for (ip = 1; ip <= runtime->npatch[IDIR]+1; ip++)  /* XXX: Shifting the node coordinates of the patch */
    runtime->patch_left_node[IDIR][ip] += shift_val;

  /*
  MPI_Barrier (MPI_COMM_WORLD);
  for (ip = 1; ip <= runtime->npatch[IDIR]+1; ip++) 
    printLog("After Step %d: runtime->patch_left_node = %f\n", g_stepNumber, runtime->patch_left_node[IDIR][ip]);
  
  for (ip = 1; ip <= runtime->npatch[JDIR]+1; ip++) 
    printLog("After Step %d: runtime->patch_left_node = %f\n", g_stepNumber, runtime->patch_left_node[JDIR][ip]);

  for (ip = 1; ip <= runtime->npatch[KDIR]+1; ip++) 
    printLog("After Step %d: runtime->patch_left_node = %f\n", g_stepNumber, runtime->patch_left_node[KDIR][ip]);
  */
  SetGrid(runtime, g_procs, grid);
  Where (-1, grid);     /* -- store grid inside the "Where"
                              function for subsequent calls -- */
  #if VERBOSE != NO
  printLog("step:%d; Done updating grid!\n",g_stepNumber);
  #endif

  /* ----------------------------------------------
     5.  Get the minimum cell length among all direction.
     ---------------------------------------------- */
  double scrh, dxmin[3], dxming[3];
  int idim;
  for (idim = 0; idim < 3; idim++) dxmin[idim] = 1.e30;

  for (i = IBEG; i <= IEND; i++) {
    for (j = JBEG; j <= JEND; j++) {
      for (k = KBEG; k <= KEND; k++) {
        scrh = Length_1(i, j, k, grid);
        dxmin[IDIR] = MIN (dxmin[IDIR], scrh);

        scrh = Length_2(i, j, k, grid);
        dxmin[JDIR] = MIN (dxmin[JDIR], scrh);

        scrh = Length_3(i, j, k, grid);
        dxmin[KDIR] = MIN (dxmin[KDIR], scrh);
      }
    }
  }

  #ifdef PARALLEL
  MPI_Allreduce (dxmin, dxming, 3, MPI_DOUBLE, MPI_MIN, MPI_COMM_WORLD);
  MPI_Barrier (MPI_COMM_WORLD);
  dxmin[IDIR] = dxming[IDIR];
  dxmin[JDIR] = dxming[JDIR];
  dxmin[KDIR] = dxming[KDIR];
  #endif

  grid->dl_min[IDIR] = dxmin[IDIR];
  grid->dl_min[JDIR] = dxmin[JDIR];
  grid->dl_min[KDIR] = dxmin[KDIR];

  /* ----------------------------------------------
     6a. Define geometrical coefficients for
         linear / PPM reconstruction.
     ---------------------------------------------- */

  PLM_CoefficientsSet (grid);   /* -- these may be needed by
                                      shock flattening algorithms */
  #if RECONSTRUCTION == PARABOLIC
  PPM_CoefficientsSet (grid);
  #endif

  /* ----------------------------------------------
     6b. Compute chunk size for the RING_AVERAGE
         technique.
     ---------------------------------------------- */
  #ifdef PARALLEL
  Boundary (d, ALL_DIR, grid);
  MPI_Barrier (MPI_COMM_WORLD);
  /*
  int par_dim[3] = {0, 0, 0};
  DIM_EXPAND(par_dim[0] = grid->nproc[IDIR] > 1;  ,
           par_dim[1] = grid->nproc[JDIR] > 1;  ,
           par_dim[2] = grid->nproc[KDIR] > 1;)           

  MPI_Barrier (MPI_COMM_WORLD);
  NVAR_LOOP(nv) AL_Exchange_dim ((char *)d->Vc[nv][0][0], par_dim, SZ);  
  MPI_Barrier (MPI_COMM_WORLD);
  */
  RBox dom_box;
  RBoxDefine (0, NX1_TOT-1, 0,  NX2_TOT-1, 0, NX3_TOT-1, CENTER, &dom_box);
  PrimToCons3D (d->Vc, d->Uc, &dom_box);
  /*
  TOT_LOOP(k,j,i) {
    RBox dom_box;
    RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box); // NX1_TOT
    PrimToCons3D(d->Vc, d->Uc, &dom_box);
  }
  */
  MPI_Barrier (MPI_COMM_WORLD);
  #endif
  
  #if RING_AVERAGE > 1
  RingAverageSize(grid);
  #endif
  MPI_Barrier (MPI_COMM_WORLD);
  TOT_LOOP(k,j,i) {
    distance = r[i];
    if (i<=(NX1_TOT-1-shift_cells)) {
      NVAR_LOOP(nv) {
        d->Vc[nv][k][j][i] = d->Vc[nv][k][j][i+shift_cells];
        d->Uc[k][j][i][nv] = d->Uc[k][j][i+shift_cells][nv];
        //d->Vs[nv][k][j][i] = d->Vs[nv][k][j][i+shift_cells];
      }
    }
    else { //wind property
      double rByrInj  = (distance/rIni)*rIniByrInj;

      d->Vc[RHO][k][j][i]   = CC85rho(rByrInj)/CC85rho(rIniByrInj);
      d->Vc[PRS][k][j][i]   = CC85prs(rByrInj)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2));
      d->Vc[iVR][k][j][i]   = CC85vel(rByrInj)/CC85vel(rIniByrInj);
      d->Vc[iVTH][k][j][i]  = 0.;
      d->Vc[iVPHI][k][j][i] = 0.;
      d->Vc[TRC][k][j][i]   = 0.;
      /* Update the conservative variables */
      RBox dom_box;
      RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box);
      PrimToCons3D(d->Vc, d->Uc, &dom_box);
    }
  }
  #if (SHOCK_FLATTENING == MULTID) || ENTROPY_SWITCH
  FlagShock (d, grid);
  #endif
  // XXX: Tracking steps executed
  /*
  trc = 0.;
  DOM_LOOP(k,j,i){
    dV = grid->dV[k][j][i]; // Cell volume
    trc += d->Vc[RHO][k][j][i]*d->Vc[TRC][k][j][i]*dV;
  }
  #ifdef PARALLEL
  MPI_Allreduce (&trc, &tmp, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
  trc = tmp;
  #endif
  printLog("After Tracking: step %d; t=%f; M_trc = %f\n", g_stepNumber, g_time, trc); 
  */
  #if PARTICLES != NO
  particleNode *curr, *next;
  Particle *p;
  int dir;
  curr = d->PHead;
  while (curr != NULL) {  /* Do not use macro looping here  */
    p    = &(curr->p);
    next = curr->next;
    //p->coord[0] -= (shift_cells*dx[IBEG]); //uniform grid assumption
    curr = next;
  }
  #endif
}
