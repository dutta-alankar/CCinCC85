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
  int i, j, k, nv;
  int yr = 365*24*60*60;

  double rIni        = g_inputParam[RINI]; // cloud position in units of Rcl
  double thIni       = g_inputParam[THINI]*CONST_PI/180;
  double phiIni      = g_inputParam[PHIINI]*CONST_PI/180;
  double chi         = g_inputParam[CHI];
  double mach        = g_inputParam[MACH];
  double rIniByrInj  = CC85pos(mach);

  static double cloud_pos;
  double delta = 0.;

  if (g_stepNumber==0)
    cloud_pos = g_dist_lab;
  else
    delta = g_dist_lab-cloud_pos; /* g_dist_lab is updated at every step in main.c */
  g_tracking = delta;

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
    cloud_pos = g_dist_lab - delta;
  }

  double *r   = grid->x[IDIR];
  double *th  = grid->x[JDIR];
  double *phi = grid->x[KDIR];

  double *dr   = grid->dx[IDIR];
  double *dth  = grid->dx[JDIR];
  double *dphi = grid->dx[KDIR];

  if ( (g_time<5.0*sqrt(chi) || ( (g_time>10.0*sqrt(chi)) && (g_time<12.0*sqrt(chi)) )) ){
    cloud_pos = g_dist_lab;
    return;
  }
  int OffInterval = (int)round(3.0*sqrt(chi));
  if ( (g_time>12.0*sqrt(chi)) ){
    int val = ( ((int)round(g_time-12.0*sqrt(chi)))%OffInterval )%2;
    if (val==1){
      cloud_pos = g_dist_lab;
      return;
    }
  }
  /* Assuming uniform grid */
  int shift_cells = 0;
  if (delta >= 0)
    shift_cells =  (int)floor(delta/dr[IBEG]) ; // Cloud movement: pos: --> right & neg: <-- left
  else
     shift_cells =  (int)ceil(delta/dr[IBEG]) ;
  int shift_thres = MIN(1,grid->nghost[0]-g_ghost_true); //flooring creates a small overshoot error in fixing cloud position
  /*
  static int switch_tracking = 1;
  if (g_trctrack/dr[IBEG]<=50) {
    switch_tracking = 0;
  }
  else {
    if (switch_tracking == 0){
      switch_tracking = 1;
      cloud_pos = g_dist_lab;
      return;
    }
  }

  if (switch_tracking==0) return;
  */
  if (fabs(shift_cells)<shift_thres) return;
  #if VERBOSE != NO
  else
    printLog("step:%d; Applying cloud tracking: cells_shift=%d; shift_thres=%d\n",g_stepNumber, shift_cells, shift_thres);
  #endif

  double shift_val = shift_cells*dr[IBEG]; //uniform grid assumption
  cloud_pos += shift_val; //this auto corrects the small overshoot in the next step

  //printLog("Shift val = %lf\tTotal Shift val = %lf\n", shift_val, g_tot_shift_val);
  g_tot_shift_val = g_tot_shift_val + shift_val;

  grid->xbeg[IDIR] += shift_val;
  grid->xend[IDIR] += shift_val;
  grid->xbeg_glob[IDIR] += shift_val;
  grid->xend_glob[IDIR] += shift_val;
  g_domBeg[IDIR] += shift_val;
  g_domEnd[IDIR] += shift_val;

  ITOT_LOOP(i) {
    grid->x[IDIR][i] += shift_val;
    //grid->x_glob[IDIR][i] += shift_val;
    grid->xr[IDIR][i] += shift_val;
    //grid->xr_glob[IDIR][i] += shift_val;
    grid->xl[IDIR][i] += shift_val;
    //grid->xl_glob[IDIR][i] += shift_val;
    //grid->xgc[IDIR][i] += shift_val;
    //grid->rt[i] += shift_val;
  }
  SetGeometry(grid);

  #if VERBOSE != NO
  printLog("step:%d; Done updating grid!\n",g_stepNumber);
  #endif

  TOT_LOOP(k,j,i){
    if(shift_cells>0){ //cloud moving to right

      if (i<=(NX1_TOT-1-shift_cells)) {
        NVAR_LOOP(nv) {
          d->Vc[nv][k][j][i] = d->Vc[nv][k][j][i+shift_cells];
          //d->Uc[nv][k][j][i] = d->Uc[nv][k][j][i+shift_cells];
          //d->Vs[nv][k][j][i] = d->Vs[nv][k][j][i+shift_cells];
        }
        //d->Vc[RHO][k][j][i] = d->Vc[RHO][k][j][i+shift_cells];
        //d->Vc[PRS][k][j][i] = d->Vc[PRS][k][j][i+shift_cells];
        //d->Vc[iVR][k][j][i] = d->Vc[iVR][k][j][i+shift_cells];
        //d->Vc[TRC][k][j][i] = d->Vc[TRC][k][j][i+shift_cells];
      }
      else { //wind property
        double distance = r[i];
        double rByrInj  = (distance/rIni)*rIniByrInj;

        d->Vc[RHO][k][j][i]   = CC85rho(rByrInj)/CC85rho(rIniByrInj);
        d->Vc[PRS][k][j][i]   = CC85prs(rByrInj)/(CC85rho(rIniByrInj)*pow(CC85vel(rIniByrInj),2));
        d->Vc[iVR][k][j][i]   = CC85vel(rByrInj)/CC85vel(rIniByrInj);
        d->Vc[iVTH][k][j][i]  = 0.;
        d->Vc[iVPHI][k][j][i] = 0.;
        d->Vc[TRC][k][j][i]   = 0.;
      }
    }
    /* Update the conservative variables */
    RBox dom_box;
    RBoxDefine (i, i, j, j, k, k, CENTER, &dom_box);
    PrimToCons3D(d->Vc, d->Uc, &dom_box);
  }


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
