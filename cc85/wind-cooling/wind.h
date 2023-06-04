extern double *rbyR, *rhotld, *prstld, *veltld, *machCC85;
extern int nwindtab;
double interp1D_wind(double* , double* , double , char* );
void create_CC85_data();
void read_CC85_data(char* );
double CC85rho(double );
double CC85prs(double );
double CC85vel(double );
double CC85pos(double );
