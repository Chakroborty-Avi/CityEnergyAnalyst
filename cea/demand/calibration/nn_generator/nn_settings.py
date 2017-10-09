nn_delay=1
nn_passes=20
target_parameters = ['Qhsf_kWh', 'T_int_C'] #we will later add:'Qcsf_kWh', 'Qwwf_kWh', 'Ef_kWh',
random_variables = ['win_wall','Cm_Af','n50',
                    'U_roof','a_roof','U_wall','a_wall','U_base','U_win','G_win','rf_sh',
                    'Ths_set_C','Tcs_set_C','Ths_setb_C','Tcs_setb_C','Ve_lps',
                    'Qs_Wp','X_ghp','Ea_Wm2','El_Wm2','Vww_lpd','Vw_lpd',
                    'dThs_C','dTcs_C','ECONOMIZER','WIN_VENT','MECH_VENT','HEAT_REC','NIGHT_FLSH','dT_Qhs','dT_Qcs']
number_samples=10
boolean_vars = ['ECONOMIZER','WIN_VENT','MECH_VENT','HEAT_REC','NIGHT_FLSH']
