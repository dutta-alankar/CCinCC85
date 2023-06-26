#include "definitions.h"
#include "pluto.h"

int calc_cloud_pos(double , double , double , int );
void ApplyFrameBoost (const Data *, Grid *, double);

extern double   g_dist_lab;
extern double   g_anldt;
extern int      g_restart;
extern double   g_dist_start_boost;
extern double   g_boost_vel;
