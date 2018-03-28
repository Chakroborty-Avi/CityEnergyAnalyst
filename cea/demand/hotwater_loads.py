"""
Hotwater load (it also calculates fresh water needs)
"""

from __future__ import division
from cea.constants import *
import numpy as np
import scipy
from math import pi
from cea.demand import constants
from cea.technologies import storage_tank as storage_tank

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Shanshan Hsieh"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

# import constants
D = constants.D
B_F = constants.B_F
P_WATER = P_WATER_KGPERM3
FLOWTAP = constants.FLOWTAP
C_P_W = HEAT_CAPACITY_OF_WATER_JPERKGK / 1000
TWW_SETPOINT = constants.TWW_SETPOINT


def calc_mww(schedule, water_lpd):
    """
    Algorithm to calculate the hourly mass flow rate of water

    :param schedule: hourly DHW demand profile [person/d.h]
    :param water_lpd: water emand per person per day in [L/person/day]
    """

    if schedule > 0:

        volume = schedule * water_lpd/ 1000 # m3/h
        massflow = volume * P_WATER/3600  # in kg/s

    else:
        volume = 0
        massflow = 0

    return massflow, volume

# final hot water demand calculation

def calc_Qwwf(Lcww_dis, Lsww_dis, Lvww_c, Lvww_dis, T_ext, Ta, Tww_re, Tww_sup_0, Y, gv, schedules, bpr):
    # Refactored from CalcThermalLoads
    """
    This function calculates the distribution heat loss and final energy consumption of domestic hot water.
    Final energy consumption of dhw includes dhw demand, sensible heat loss in hot water storage tank, and heat loss in the distribution network.
    :param Lcww_dis: Length of dhw usage circulation pipeline in m.
    :param Lsww_dis: Length of dhw usage distribution pipeline in m.
    :param Lvww_c: Length of dhw heating circulation pipeline in m.
    :param Lvww_dis: Length of dhw heating distribution pipeline in m.
    :param T_ext: Ambient temperature in C.
    :param Ta: Room temperature in C.
    :param Tww_re: Domestic hot water tank return temperature in C, this temperature is the ground water temperature, set according to norm.
    :param Tww_sup_0: Domestic hot water supply set point temperature in C.
    :param vw: specific fresh water consumption in m3/hr*m2.
    :param vww: specific domestic hot water consumption in m3/hr*m2.
    :param Y: linear trasmissivity coefficients of piping in W/m*K
    :return: mcptw: tap water capacity masss flow rate in kW_C
    """

    # calc end-use demand
    volume_flow_ww = schedules['Vww'] * bpr.internal_loads['Vww_lpd'] / 1000   # m3/h
    volume_flow_fw = schedules['Vw'] * bpr.internal_loads['Vw_lpd'] / 1000      # m3/h
    mww = volume_flow_ww * P_WATER /3600 # kg/s
    mcptw = (volume_flow_fw - volume_flow_ww)  * C_P_W * P_WATER / 3600 # kW_K tap water

    Qww = np.vectorize(calc_Qww)(mww, Tww_sup_0, Tww_re)
    Qww_0 = Qww.max()

    # distribution and circulation losses
    Vol_ls = Lsww_dis * ((D / 1000)/2) ** 2 * pi # m3, volume inside distribution pipe
    Qww_dis_ls_r = np.vectorize(calc_Qww_dis_ls_r)(Ta, Qww, Lsww_dis, Lcww_dis, Y[1], Qww_0, Vol_ls,
                                                   Tww_sup_0, gv)
    Qww_dis_ls_nr = np.vectorize(calc_Qww_dis_ls_nr)(Ta, Qww, Lvww_dis, Lvww_c, Y[0], Qww_0, Vol_ls,
                                                     Tww_sup_0, T_ext, gv)
    # storage losses
    Qww_st_ls, Tww_st, Qwwf = calc_Qww_st_ls(T_ext, Ta, Qww, volume_flow_ww, Qww_dis_ls_r, Qww_dis_ls_nr, gv)

    # final demand
    Qwwf_0 = Qwwf.max()
    mcpwwf = Qwwf / abs(Tww_st - Tww_re)

    return mww, mcptw, Qww, Qww_st_ls, Qwwf, Qwwf_0, Tww_st, volume_flow_ww, volume_flow_fw, mcpwwf


# end-use hot water demand calculation


def calc_Qww(mww, Tww_sup_0, Tww_re):
    """
    Calculates the DHW demand according to the supply temperature and flow rate.
    :param mww: required DHW flow rate in [kg/s]
    :param Tww_sup_0: Domestic hot water supply set point temperature.
    :param Tww_re: Domestic hot water tank return temperature in C, this temperature is the ground water temperature, set according to norm.
    :param Cpw: heat capacity of water [kJ/kgK]
    :return Qww: Heat demand for DHW in [Wh]
    """
    mcpww = mww * C_P_W * 1000  # W/K
    Qww = mcpww * (Tww_sup_0 - Tww_re)  # heating for dhw in Wh
    return Qww


# losess hot water demand calculation


def calc_Qww_dis_ls_r(Tair, Qww, Lsww_dis, Lcww_dis, Y, Qww_0, V, twws, gv):

    if Qww > 0:
        # Calculate tamb in basement according to EN
        tamb = Tair

        # Circulation circuit losses
        circ_ls = (twws - tamb) * Y * Lcww_dis * (Qww / Qww_0)

        # Distribtution circuit losses
        dis_ls = calc_disls(tamb, Qww, V, twws, Lsww_dis, Y, gv)

        Qww_d_ls_r = circ_ls + dis_ls
    else:
        Qww_d_ls_r = 0
    return Qww_d_ls_r


def calc_Qww_dis_ls_nr(tair, Qww, Lvww_dis, Lvww_c, Y, Qww_0, V, twws, te, gv):
    """

    :param tair:
    :param Qww:
    :param Lvww_dis:
    :param Lvww_c:
    :param Y:
    :param Qww_0:
    :param V:
    :param twws:
    :param te:
    :param gv:
    :return:
    """
    # TODO: documentation
    # date: legacy

    if Qww > 0:
        # Calculate tamb in basement according to EN
        tamb = tair - B_F * (tair - te)

        # Circulation losses
        d_circ_ls = (twws - tamb) * Y * (Lvww_c) * (Qww / Qww_0)

        # Distribution losses
        d_dis_ls = calc_disls(tamb, Qww, V, twws, Lvww_dis, Y, gv)
        Qww_d_ls_nr = d_dis_ls + d_circ_ls
    else:
        Qww_d_ls_nr = 0
    return Qww_d_ls_nr


def calc_disls(tamb, Vww, V, twws, Lsww_dis, Y, gv):
    """
    Calculates distribution losses in Wh according to Fonseca & Schlueter (2015) Eq. 24, which is in turn based
    on Annex A of ISO EN 15316 with pipe mass m_p,dis = 0.
    
    :param tamb: Room temperature in C
    :param Vww: volumetric flow rate of hot water demand (in m3)
    :param V: volume of water accumulated in the distribution network in m3
    :param twws: Domestic hot water supply set point temperature in C
    :param Lsww_dis: length of circulation/distribution pipeline in m
    :param p: water density kg/m3
    :param cpw: heat capacity of water in kJ/kgK
    :param Y: linear trasmissivity coefficient of piping in distribution network in W/m*K
    :param gv: globalvar.py

    :return losses: recoverable/non-recoverable losses due to distribution of DHW
    """
    if Vww > 0:
        TR = 3600 / ((Vww / 1000) / FLOWTAP) # Thermal response of insulated piping
        if TR > 3600: TR = 3600
        try:
            exponential = scipy.exp(-(Y * Lsww_dis * TR) / (P_WATER * C_P_W * V * 1000))
        except ZeroDivisionError:
            gv.log('twws: %(twws).2f, tamb: %(tamb).2f, p: %(p).2f, cpw: %(cpw).2f, V: %(V).2f',
                   twws=twws, tamb=tamb, p=P_WATER, cpw=C_P_W, V=V)
            raise ZeroDivisionError

        tamb = tamb + (twws - tamb) * exponential

        losses = (twws - tamb) * V * C_P_W * P_WATER / 3.6 # in Wh
    else:
        losses = 0
    return losses


def calc_Qww_st_ls(T_ext, Ta, Qww, Vww, Qww_dis_ls_r, Qww_dis_ls_nr, gv):
    """
    Calculates the heat flows within a fully mixed water storage tank for 8760 time-steps.
    :param T_ext: external temperature in [C]
    :param Ta: room temperature in [C]
    :param Qww: hourly DHW demand in [Wh]
    :param Vww: hourly DHW demand in [m3]
    :param Qww_dis_ls_r: recoverable loss in distribution in [Wh]
    :param Qww_dis_ls_nr: non-recoverable loss in distribution in [Wh]
    :param gv: globalvar.py

    :type T_ext: ndarray
    :type Ta: ndarray
    :type Qww: ndarray
    :type Vww: ndarray
    :type Qww_dis_ls_r: ndarray
    :type Qww_dis_ls_nr: ndarray
    :return:
    """
    Qwwf = np.zeros(8760)
    Qww_st_ls = np.zeros(8760)
    Tww_st = np.zeros(8760)
    Qd = np.zeros(8760)
    # calculate DHW tank size [in m3] based on the peak DHW demand in the building
    Vww_0 = Vww.max()
    T_ww_start_C = TWW_SETPOINT # assume the tank temperature at timestep 0 is at the set point

    if Vww_0 > 0:
        for k in range(8760):
            Area_tank_surface_m2 = storage_tank.calc_tank_surface_area(Vww_0)
            Q_tank_discharged_W = Qww[k] + Qww_dis_ls_r[k] + Qww_dis_ls_nr[k]
            Qww_st_ls[k], Qd[k], Qwwf[k] = storage_tank.calc_dhw_tank_heat_flows(Ta[k], T_ext[k], T_ww_start_C, Vww_0,
                                                                                 Q_tank_discharged_W, Area_tank_surface_m2)
            Tww_st[k] = storage_tank.calc_tank_temperature(T_ww_start_C, Qww_st_ls[k], Qd[k], Qwwf[k], Vww_0)
            T_ww_start_C = Tww_st[k] # update the temperature at the beginning of the next time step
    else:
        for k in range(8760):
            Tww_st[k] = np.nan
    return Qww_st_ls, Tww_st, Qwwf