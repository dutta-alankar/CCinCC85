#include "definitions.h"
#include "pluto.h"

int store_or_save_cloud_pos(double , double , int );
double* calc_scale(double , double );
double transform_velocity (const Data *, Grid *);
void ApplyFrameBoost (const Data *, Grid *, double );
void ApplyWindScaling (const Data *, Grid *, double *);

extern double   g_dist_lab;
extern double   g_anldt;
extern double   g_dist_start_boost;
extern double   g_boost_vel;
extern double   g_scale_save;
extern int      g_first_time_boost;
