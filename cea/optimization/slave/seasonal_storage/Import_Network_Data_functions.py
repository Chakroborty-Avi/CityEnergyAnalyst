""" 

Import Network Data:
  
    This File reads all relevant thermal data for further analysis in the Slave Routine, 
    Namely : Thermal (J+) and Solar Data (J+) 
            
"""
import pandas as pd
import numpy as np
__author__ = "Sreepathi Bhargava Krishna"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Sreepathi Bhargava Krishna", "Thuy-an Ngugen", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"

def import_solar_data(fName, DAYS_IN_YEAR, HOURS_IN_DAY):
    """
    importing and preparing raw data for analysis of the district distribution

    :param fName: name of file where solar data is stored in
    :param DAYS_IN_YEAR: number of days in a year (usually 365)
    :param HOURS_IN_DAY: number of hours in a day (usually 24)
    :type fName: string
    :type DAYS_IN_YEAR: int
    :type HOURS_IN_DAY: int
    :return: Arrays containing all relevant data for further processing:
        mdot_sst_heat, mdot_sst_cool, T_sst_heat_return, T_sst_heat_supply, T_sst_cool_return,
        Q_DH_building, Q_DC_building, Q_DH_building_max, Q_DC_bulding_max, T_sst_heat_supply_ofmaxQh,
        T_sst_heat_return_ofmaxQh, T_sst_cool_return_ofmaxQc
    :rtype: list
    """

    if fName == "Pv.csv":
        solar_data = pd.read_csv(fName, nrows=24 * DAYS_IN_YEAR)
        PV_import_kWh = np.array(solar_data['PV_kWh'])
        Pv_PV_kWh = PV_import_kWh
        PV_PVT_kWh = np.zeros(24*DAYS_IN_YEAR)
        Solar_Area_m2 = np.zeros(24*DAYS_IN_YEAR)
        Solar_E_aux_kWh = np.zeros(24*DAYS_IN_YEAR)
        Solar_Q_th_kWh = np.zeros(24*DAYS_IN_YEAR)
        Solar_Tscs_th = np.zeros(24*DAYS_IN_YEAR)
        Solar_Tscr_th_K = np.zeros(24*DAYS_IN_YEAR)
        Solar_mcp_kWperC = np.zeros(24*DAYS_IN_YEAR)
        #print "PV"
    
    elif fName == "PVT_35.csv":
        solar_data = pd.read_csv(fName, nrows=24 * DAYS_IN_YEAR)
        Pv_PV_kWh = np.zeros(24*DAYS_IN_YEAR)
        PV_PVT_import_kWh = np.array(solar_data['PV_kWh'])
        PV_PVT_kWh = PV_PVT_import_kWh
        Solar_Area_Array = np.array(solar_data['Area'])
        Solar_Area_m2 = Solar_Area_Array[0]
        Solar_E_aux_kWh = np.array(solar_data['Eaux_kWh'])
        Solar_Q_th_kWh = np.array(solar_data['Qsc_KWh']) + 0.0
        Solar_Tscs_th = np.zeros(24*DAYS_IN_YEAR)
        Solar_Tscr_th_K = np.array(solar_data['Tscr']) + 273.0
        Solar_mcp_kWperC = np.array(solar_data['mcp_kW/C'])
        #print "PVT 35"
        
        # Replace by 0 if negative values
        Tscs = np.array( pd.read_csv( fName, usecols=["Tscs"], nrows=1 ) ) [0][0]
        
        for i in range(DAYS_IN_YEAR * HOURS_IN_DAY):
            if Solar_Q_th_kWh[i] < 0:
                Solar_Q_th_kWh[i] = 0
                Solar_E_aux_kWh[i] = 0
                Solar_Tscr_th_K[0] = Tscs + 273
                Solar_mcp_kWperC[i] = 0
    
    else:
        solar_data = pd.read_csv(fName, nrows=24 * DAYS_IN_YEAR)
        Solar_Area_Array = np.array(solar_data['Area'])
        Solar_Area_m2 = Solar_Area_Array[0]
        Solar_E_aux_kWh = np.array(solar_data['Eaux_kW'])
        Solar_Q_th_kWh = np.array(solar_data['Qsc_Kw']) + 0.0
        Solar_Tscr_th_K = np.array(solar_data['Tscr']) + 273.0
        Solar_Tscs_th = np.zeros(24 * DAYS_IN_YEAR)

        Solar_mcp_kWperC = np.array(solar_data['mcp_kW/C'])
        Pv_PV_kWh = np.zeros(24 * DAYS_IN_YEAR)
        PV_PVT_kWh = np.zeros(24 * DAYS_IN_YEAR)

        # Replace by 0 if negative values
        Tscs = np.array( pd.read_csv( fName, usecols=["Tscs"], nrows=1 ) ) [0][0]
        
        for i in range(DAYS_IN_YEAR * HOURS_IN_DAY):
            if Solar_Q_th_kWh[i] < 0:
                Solar_Q_th_kWh[i] = 0
                Solar_E_aux_kWh[i] = 0
                Solar_Tscr_th_K[0] = Tscs + 273
                Solar_mcp_kWperC[i] = 0

    PV_kWh = PV_PVT_kWh + Pv_PV_kWh

    return Solar_Area_m2, Solar_E_aux_kWh, Solar_Q_th_kWh, Solar_Tscs_th, Solar_mcp_kWperC, PV_kWh, Solar_Tscr_th_K