void write_info (char* filename) {
  if (prank!=0) return;
  FILE *fp;
  sprintf (filename, "%s/%s", RuntimeGet()->output_dir, filename);
  fp = fopen(filename,"w"); /* from beginning */
  fprintf (fp,"id: growth_test\n");
  fprintf (fp,"paths:\n- {root}/%s\n", RuntimeGet()->output_dir);
  fprintf (fp,"simulation attributes:\n");
  #if COOLING != NO
  fprintf (fp,"\thas_cooling: yes\n");
  #else
  fprintf (fp,"\thas_cooling: no\n");
  #endif
  #if GEOMETRY == SPHERICAL
  fprintf (fp,"\tgeometry: spherical\n");
  #elif GEOMETRY == CARTESIAN
  fprintf (fp,"\tgeometry: cartesian\n");
  #elif GEOMETRY == POLAR
  fprintf (fp,"\tgeometry: polar\n");
  #else
  printLog("Unsupported Geometry!\n");
  QUIT_PLUTO(1);
  #endif
  fprintf (fp,"\tdimensioality: %d\n", DIMENSIONS);

  fprintf (fp,"parameters:\n");
  fprintf (fp,"\tchi: %.3f\n", g_inputParam[CHI]);
  fprintf (fp,"\tMach_ini: %.3f\n", g_inputParam[MACH]);
  fprintf (fp,"\tcoolmBytcc: %.3f\n", 0.8);
  fprintf (fp,"\tRinibyRcl: %.3f\n", g_inputParam[RINI]);
  fprintf (fp,"\tTcl: %.2e\n", 40000.0);
  fprintf (fp,"\tPinibykB: %.3e\n", 2020000.0);

  fprintf (fp,"wind properties:\n");
  fprintf (fp,"\tEdot : %.3e\n", 3.003538777293662e+41);
  fprintf (fp,"\tMdot : %.3e\n", 2.001792023447753);
  fprintf (fp,"\tRinj : %.3f\n", 200.02349561612164);
  fprintf (fp,"\tRini : %.3f\n", 214.15203720016763);
  fprintf (fp,"\tRcl  : %.3f\n", 0.7575668845784254);

  fprintf (fp,"code units:\n");
  fprintf (fp,"\tunit_dens: %e\n", UNIT_DENSITY);
  fprintf (fp,"\tunit_len: %e\n",  UNIT_LENGTH);
  fprintf (fp,"\tunit_vel: %e\n",  UNIT_VELOCITY);

  fprintf (fp,"additional info:\n");
  fprintf (fp,"\tRclbydcell: 8\n");
  fprintf (fp,"\tRcl_buffer: 2\n");
  fprintf (fp,"\tncells: [4802, 160, 160]\n");

  fclose(fp);
}
