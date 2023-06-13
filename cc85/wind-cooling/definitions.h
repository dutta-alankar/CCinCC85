#define  PHYSICS                        HD
#define  DIMENSIONS                     1
#define  COMPONENTS                     1
#define  GEOMETRY                       SPHERICAL
#define  BODY_FORCE                     NO
#define  FORCED_TURB                    NO
#define  COOLING                        TABULATED
#define  RECONSTRUCTION                 LINEAR
#define  TIME_STEPPING                  RK2
#define  DIMENSIONAL_SPLITTING          NO
#define  NTRACER                        0
#define  USER_DEF_PARAMETERS            6

/* -- physics dependent declarations -- */

#define  EOS                            IDEAL
#define  ENTROPY_SWITCH                 NO
#define  THERMAL_CONDUCTION             NO
#define  VISCOSITY                      NO
#define  ROTATING_FRAME                 NO
#define  PARTICLES                      NO
#define  INTERNAL_BOUNDARY              YES
#define  SHOW_TIMING                    NO
#define  SHOW_TIME_STEPS                YES
#define  TRACKING                       YES

/* -- user-defined parameters (labels) -- */

#define  RINI                           0
#define  THINI                          1
#define  PHIINI                         2
#define  CHI                            3
#define  MACH                           4
#define  ZMET                           5

/* [Beg] user-defined constants (do not change this line) */

#define  UNIT_DENSITY                   6.3682e-26
#define  UNIT_LENGTH                    2.7198e+20
#define  UNIT_VELOCITY                  5.4100e+07

/* [End] user-defined constants (do not change this line) */
#define  MULTIPLE_LOG_FILES             YES
#define  VERBOSE                        NO
#define  CUTOFF                         NO
