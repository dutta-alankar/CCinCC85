#include <stdbool.h>
#include "definitions.h"
extern double   g_dist_lab;
extern double   g_anldt;
extern double   g_boost_vel;

double transform_velocity (const Data *, Grid *);
void ApplyFrameBoost (const Data *, Grid *, double);
void ApplyWindScaling (const Data *, double , Grid *, double );
double calc_scale(double , double );
int store_or_save_cloud_pos(double , double , int );
