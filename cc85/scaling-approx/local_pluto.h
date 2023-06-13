#include <stdbool.h>
#include "definitions.h"
extern double   g_dist_lab;
extern double   g_anldt;

#if TRACKING!=NO
double ApplyFrameBoost (const Data *, Grid *);
#endif
void ApplyWindScaling (const Data *, double , timeStep *, Grid *, double );
double calc_scale(double , double );
int store_or_save_cloud_pos(double , double , int );
