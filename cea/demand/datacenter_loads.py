# -*- coding: utf-8 -*-
"""
datacenter loads
"""
from __future__ import division
import numpy as np
import pandas as pd
from cea.technologies import heatpumps
from cea.constants import HOURS_IN_YEAR

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

def has_data_load(bpr):
    """
    Checks if building has a data center load

    :param bpr: BuildingPropertiesRow
    :type bpr: cea.demand.building_properties.BuildingPropertiesRow
    :return: True or False
    :rtype: bool
        """

    if bpr.internal_loads['Ed_Wm2'] > 0:
        return True
    else:
        return False


def calc_Edata(bpr, tsd, schedules):

    tsd['Edata'] = schedules['Ed'] * bpr.internal_loads['Ed_Wm2']

    return tsd

def calc_Qcdata_sys(bpr, tsd):
    # calculate cooling loads for data center
    tsd['Qcdata'] = 0.9 * tsd['Edata']

    # calculate distribution losses for data center cooling analogously to space cooling distribution losses
    Y = bpr.building_systems['Y'][0]
    Lv = bpr.building_systems['Lv']
    Qcdata_d_ls = ((tsd['Tcdata_sys_sup'] + tsd['Tcdata_sys_re']) / 2 - tsd['T_ext']) * (
            tsd['Qcdata'] / np.nanmin(tsd['Qcdata'])) * (Lv * Y)
    # calculate system loads for data center
    tsd['Qcdata_sys'] = tsd['Qcdata'] + Qcdata_d_ls

    def function(Qcdata_sys):
        if Qcdata_sys > 0:
            Tcdataf_re_0 = 15
            Tcdataf_sup_0 = 7
            mcpref = Qcdata_sys / (Tcdataf_re_0 - Tcdataf_sup_0)
        else:
            Tcdataf_re_0 = 0
            Tcdataf_sup_0 = 0
            mcpref = 0
        return mcpref, Tcdataf_re_0, Tcdataf_sup_0

    tsd['mcpcdata_sys'], tsd['Tcdata_sys_re'], tsd['Tcdata_sys_sup'] = np.vectorize(function)(tsd['Qcdata_sys'])

    return tsd

def calc_Qcdataf(locator, bpr, tsd):
    """
    it calculates final loads
    """
    # GET SYSTEMS EFFICIENCIES
    data_systems = pd.read_excel(locator.get_life_cycle_inventory_supply_systems(), "COOLING").set_index('code')
    type_system = bpr.supply['type_cs']
    energy_source = data_systems.loc[type_system, "source_cs"]

    if energy_source == "GRID":
        if bpr.supply['type_cs'] in {'T2', 'T3'}:
            if bpr.supply['type_cs'] == 'T2':
                t_source = (tsd['T_ext'] + 273)
            if bpr.supply['type_cs'] == 'T3':
                t_source = (tsd['T_ext_wetbulb'] + 273)

            # heat pump energy
            tsd['E_cdata'] = np.vectorize(heatpumps.HP_air_air)(tsd['mcpcdata_sys'], (tsd['Tcdata_sys_sup'] + 273),
                                                                (tsd['Tcdata_sys_re'] + 273), t_source)
            # final to district is zero
            tsd['DC_cdata'] = np.zeros(HOURS_IN_YEAR)
    elif energy_source == "DC":
        tsd['DC_cdata'] = tsd['Qcdata_sys']
        tsd['E_cdata'] = np.zeros(HOURS_IN_YEAR)
    else:
        tsd['E_cdata'] = np.zeros(HOURS_IN_YEAR)
        tsd['DC_cdata'] = np.zeros(HOURS_IN_YEAR)
    return tsd

