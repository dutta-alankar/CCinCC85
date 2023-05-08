#include <stdbool.h>
#include "definitions.h"
extern int      g_ghost_true;
extern double   g_dist_lab;
extern double   g_tot_shift_val;
extern double   g_tracking;
extern double   g_anldt;
extern double   g_trctrack;
extern int      g_restart;

#if TRACKING!=NO
void ApplyTracking (const Data *, Grid *, Runtime *, cmdLine *);
#endif
