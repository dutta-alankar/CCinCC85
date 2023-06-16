#include "pluto.h"
#include "local_pluto.h"
#include "wind.h"

double *rbyR, *rhotld, *prstld, *veltld, *machCC85;
int nwindtab;

void create_CC85_data(){
  static int create_data = 1;
  /* create the CC85 steady profile for the given set of parameters in python */
  if (prank==0 && create_data){
    char command[500];
    int len = sprintf(command,"%s ./CC85.py %e %e %e %e %e %e %s", PYTHON_LOC,
                 1.0, 1.6e43,
                 1.0,  7.0,
                 200.0,  g_gamma, "False");
    printLog("> Executing: %s\n",command);
    int dummy = system(command);
    create_data = 0;
  }
  #ifdef PARALLEL
  MPI_Barrier (MPI_COMM_WORLD);
  #endif
}

void read_CC85_data(char *filename){
  /* -------------------------------------------
        Read tabulated CC85 steady wind profile
   ------------------------------------------- */

  if (rbyR == NULL){ //This line ensures reading is done only once per run
    //printLog (" > Reading table %s from disk...\n", filename);

    FILE *fCC85 = fopen(filename,"r");
    if (fCC85 == NULL){
      printLog ("! read_CC85_data: %s could not be found.\n", filename);
      QUIT_PLUTO(1);
    }
    rbyR     = ARRAY_1D(200000, double);
    rhotld   = ARRAY_1D(200000, double);
    prstld   = ARRAY_1D(200000, double);
    veltld   = ARRAY_1D(200000, double);
    machCC85 = ARRAY_1D(200000, double);

    int dummy = fscanf(fCC85, "%*[^\n]\n"); //skip the header
    nwindtab = 0;
    while (fscanf(fCC85, "%lf %lf %lf %lf\n", rbyR + nwindtab, rhotld + nwindtab, prstld + nwindtab, veltld + nwindtab)!=EOF) {
      machCC85[nwindtab] = veltld[nwindtab]/sqrt(g_gamma*prstld[nwindtab]/rhotld[nwindtab]);
      nwindtab++;
    }
  }
}

double CC85rho(double rad_norm) {
  return interp1D_wind(rbyR, rhotld, rad_norm, "CC85rho");
}

double CC85prs(double rad_norm) {
  return interp1D_wind(rbyR, prstld, rad_norm, "CC85prs");
}

double CC85vel(double rad_norm) {
  return interp1D_wind(rbyR, veltld, rad_norm, "CC85vel");
}

double CC85pos(double mach) {
  return interp1D_wind(machCC85, rbyR, mach, "CC85pos");
}

double interp1D_wind(double* x_data, double* y_data, double x_request, char* msg) {

 /* ----------------------------------------------
  *         Table lookup by binary search used for interpolating y as a function of x.
  *        x is assumed to be arranged in ascending order
  *  ---------------------------------------------- */
  //nwindtab number of entries maybe (int)(sizeof(x_data)/sizeof(x_data[0])) will work
  int klo = 0;
  int khi = nwindtab - 1;
  int kmid;
  double xmid, dx, scrh;

  if (x_request > x_data[khi] || x_request < x_data[klo]){
    print ("Called from %s\n",msg);
    print (" ! Requested value out of range: %12.6e\n",x_request);
    QUIT_PLUTO(1);
  }

  while (klo != (khi - 1)){
    kmid = (klo + khi)/2;
    xmid = x_data[kmid];
    if (x_request <= xmid){
      khi = kmid;
    }else if (x_request > xmid){
      klo = kmid;
    }
  }

/* -----------------------------------------------
 *     Compute r.h.s
 * ----------------------------------------------- */
  dx       = x_data[khi] - x_data[klo];
  scrh     = y_data[klo]*(x_data[khi] - x_request)/dx + y_data[khi]*(x_request - x_data[klo])/dx;

  return scrh;
}
