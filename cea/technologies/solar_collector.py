"""
solar collectors
"""

from __future__ import division
import numpy as np
import pandas as pd
import cea.globalvar
import cea.inputlocator
from math import *
import re
import time
from cea.utilities import dbfreader
from cea.utilities import epwreader
from cea.utilities import solar_equations

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


# SC heat generation

def calc_SC(locator, radiation_csv, metadata_csv, latitude, longitude, weather_path, building_name, pvonroof, pvonwall,
            misc_losses, worst_hour, type_SCpanel, T_in, min_radiation, date_start):

    t0 = time.clock()

    # weather data
    weather_data = epwreader.epw_reader(weather_path)
    print 'reading weather data done'

    # solar properties
    g, Sz, Az, ha, trr_mean, worst_sh, worst_Az = solar_equations.calc_sun_properties(latitude,longitude, weather_data,
                                                                                                        date_start,
                                                                                                        worst_hour)
    print 'calculating solar properties done'

    # get properties of the panel to evaluate
    n0, c1, c2, mB0_r, mB_max_r, mB_min_r, C_eff, t_max, IAM_d, Aratio, Apanel, dP1, dP2, dP3, dP4 = calc_properties_SC(
        type_SCpanel)
    print 'gathering properties of PV panel'

    # select sensor point with sufficient solar radiation
    max_yearly_radiation, min_yearly_production, sensors_rad_clean, sensors_metadata_clean = \
        solar_equations.filter_low_potential(weather_data, radiation_csv, metadata_csv, min_radiation, pvonroof, pvonwall)

    print 'filtering low potential sensor points done'

    # Calculate the heights of all buildings for length of vertical pipes
    height = locator.get_total_demand().height.sum()

    if not sensors_metadata_clean.empty:
        # calculate optimal angle and tilt for panels
        sensors_metadata_cat = solar_equations.optimal_angle_and_tilt(sensors_metadata_clean, latitude, worst_sh, worst_Az, trr_mean,
                                                      max_yearly_radiation, module_length=2) #FIXME: change module length to panel property
        print 'calculating optimal tile angle and separation done'

        # group the sensors with the same tilt, surface azimuth, and total radiation
        Number_groups, hourlydata_groups, number_points, prop_observers = calc_groups(sensors_rad_clean, sensors_metadata_cat)

        print 'generating groups of sensor points done'

        results, Final = SC_generation(type_SCpanel, hourlydata_groups, prop_observers, number_points, g, Sz, Az, ha,
                                  latitude, T_in, height)


        Final.to_csv(locator.SC_results(building_name= building_name), index=True, float_format='%.2f')  # print PV generation potential
        sensors_metadata_cat.to_csv(locator.SC_metadata_results(building_name= building_name), index=True, float_format='%.2f')  # print selected metadata of the selected sensors

        print 'done - time elapsed:', (time.clock() - t0), ' seconds'
    return

# =========================
# SC heat production
# =========================

def SC_generation(type_SCpanel, group_radiation, prop_observers, number_points, weather_data, g, Sz, Az, ha, latitude,
                  Tin, height):
    n0, c1, c2, mB0_r, mB_max_r, mB_min_r, C_eff, t_max, IAM_d, Aratio, Apanel, dP1, dP2, dP3, dP4 = calc_properties_SC(
        type_SCpanel) #TODO: move out when testing is done
    aperature_area = Aratio * Apanel
    listgroups = number_points.count()  # counter from the vector with number of points
    listresults = [None] * listgroups
    listresults_perarea = [None] * listgroups
    listareasgroups = [None] * listgroups
    Sum_mcp = np.zeros(8760)
    Sum_qout = np.zeros(8760)
    Sum_Eaux = np.zeros(8760)
    Sum_qloss = np.zeros(8760)
    Tin_array = np.zeros(8760) + Tin
    Sum_Area_m = (prop_observers['area_netpv'] * number_points).sum()
    lv = 2  # grid lenght module length # TODO: change to module length
    Le = (2 * lv * number_points.sum()) / (Sum_Area_m * Aratio)
    Li = 2 * height / (Sum_Area_m * Aratio)
    Leq = Li + Le  # in m/m2
    if type_SCpanel == 2:  # for vaccum tubes
        Nseg = 100  # default number of subsdivisions for the calculation #TODO: find reference
    else:
        Nseg = 10  # default number of subsdivisions for the calculation

    for group in range(listgroups):
        teta_z = prop_observers.loc[group, 'aspect']  # azimuth of panels of group
        Area_group = prop_observers.loc[group, 'area_netpv'] * number_points[group]
        tilt_angle = prop_observers.loc[group, 'slope']  # tilt angle of panels
        radiation = pd.DataFrame({'I_sol': group_radiation[group]})  # choose vector with all values of Isol
        radiation['I_diffuse'] = weather_data.ratio_diffhout * radiation.I_sol  # calculate diffuse radiation
        radiation['I_direct'] = radiation['I_sol'] - radiation['I_diffuse']  # direct radaition

        # calculate incidence angle modifier for beam radiation
        IAM_b = calc_anglemodifierSC(Az, g, ha, teta_z, tilt_angle, type_SCpanel, latitude, Sz)  # direct angle modifier

        listresults[group] = calc_SC_module(radiation, tilt_angle, IAM_b, radiation.I_direct,
                                            radiation.I_diffuse, weather_data.drybulb_C,
                                            n0, c1, c2, mB0_r, mB_max_r, mB_min_r, C_eff, t_max, IAM_d, aperature_area,
                                            dP1, dP2, dP3, dP4, Tin, Leq, Le, Nseg)

        K = Area_group / Apanel
        listresults[group][5] = listresults[group][5] * K
        listresults[group][0] = listresults[group][0] * K
        listresults[group][1] = listresults[group][1] * K
        listresults[group][2] = listresults[group][2] * K

        listareasgroups[group] = Area_group

    for group in range(listgroups):
        mcp_array = listresults[group][5]
        qloss_array = listresults[group][0]
        qout_array = listresults[group][1]
        Eaux_array = listresults[group][2]
        Sum_qout = Sum_qout + qout_array
        Sum_Eaux = Sum_Eaux + Eaux_array
        Sum_qloss = Sum_qloss + qloss_array
        Sum_mcp = Sum_mcp + mcp_array

    Tout_group = (Sum_qout / Sum_mcp) + Tin  # in C

    Final = pd.DataFrame(
        {'Qsc_kWh': Sum_qout, 'Ts_C': Tin_array, 'Tr_C': Tout_group, 'mcp_kW/C': Sum_mcp, 'Eaux_kWh': Sum_Eaux,
         'Qsc_l_kWh': Sum_qloss, 'Area': sum(listareasgroups)}, index=range(8760))

    return listresults, Final


# def calc_groups(Clean_hourly, observers_fin):
#     # calculate number of optima groups as number of optimal combiantions.
#     groups_ob = Clean_hourly.groupby(['CATB', 'CATGB', 'CATteta_z'])
#     hourlydata_groups = groups_ob.mean().reset_index()
#     hourlydata_groups = pd.DataFrame(hourlydata_groups)
#     Number_pointsgroup = groups_ob.size().reset_index()
#     number_points = Number_pointsgroup[0]
#
#     groups_ob = observers_fin.groupby(['CATB', 'CATGB', 'CATteta_z'])
#     prop_observers = groups_ob.mean().reset_index()
#     prop_observers = pd.DataFrame(prop_observers)
#     Number_groups = groups_ob.size().count()
#
#     hourlydata_groups = hourlydata_groups.drop({'ID', 'GB', 'grid_code', 'pointid', 'array_s', 'area_netpv', 'aspect',
#                                                 'slope', 'CATB', 'CATGB', 'CATteta_z'}, axis=1).transpose().reindex(
#         axis=1)  # vector with radiation points of group
#     hourlydata_groups['newindex'] = hourlydata_groups.index
#     hourlydata_groups['newindex'] = hourlydata_groups.newindex.apply(lambda x: re.findall('\d+', x))
#     hourlydata_groups.index = range(8760)
#     for hour in range(8760):
#         hourlydata_groups.loc[hour, 'newindex'] = int(hourlydata_groups.loc[hour, 'newindex'][0])
#
#     hourlydata_groups.set_index('newindex', inplace=True)
#     hourlydata_groups.sort_index(inplace=True)
#     hourlydata_groups.index = range(8760)
#
#     return Number_groups, hourlydata_groups, number_points, prop_observers
#TODO: delete when done

def calc_SC_module(radiation, tilt_angle, IAM_b_vector, I_direct_vector, I_diffuse_vector, Te_vector, n0, c1, c2,
                   mB0_r, mB_max_r, mB_min_r, C_eff, t_max, IAM_d, aperture_area, dP1, dP2, dP3, dP4, Tin, Leq, Le, Nseg):
    """
    This function calculates the heat production of solar collectors. The method is adapted from
    :param radiation:
    :param tilt_angle:
    :param IAM_b_vector:
    :param I_direct_vector:
    :param I_diffuse_vector:
    :param Te_vector:
    :param n0:
    :param c1:
    :param c2:
    :param mB0_r:
    :param mB_max_r:
    :param mB_min_r:
    :param C_eff:
    :param t_max:
    :param IAM_d:
    :param aperture_area:
    :param dP1:
    :param dP2:
    :param dP3:
    :param dP4:
    :param Tin:
    :param Leq:
    :param Le:
    :param Nseg:
    :return:
    """
    # panel to store the results per flow
    # method with no condensaiton gains, no wind or long-wave dependency, sky factor set to zero.
    # calculate radiation part

    # local variables
    Cp_waterglycol = 3680  # J/kgK  water glycol  specific heat #TODO: move to gv
    msc_max = mB_max_r * aperture_area / 3600  # maximum mass flow [kg/s] #TODO: move into the equation

    # Do the calculation of every time step for every possible flow condition
    # get states where highly performing values are obtained.
    mopt = 0  # para iniciar
    temperature_out = [np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760)]
    temperature_in = [np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760)]
    supply_out = [np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760)]
    supply_losses = [np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760)]
    Auxiliary = [np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760)]
    temperature_m = [np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760), np.zeros(8760)]
    specific_flows = [np.zeros(8760), (np.zeros(8760) + mB0_r) * aperture_area / 3600,
                      (np.zeros(8760) + mB_max_r) * aperture_area / 3600,
                      (np.zeros(8760) + mB_min_r) * aperture_area / 3600, np.zeros(8760), np.zeros(8760)]  # in kg/s
    specific_pressurelosses = [np.zeros(8760), (np.zeros(8760) + dP2) * aperture_area, (np.zeros(8760) + dP3) * aperture_area,
                               (np.zeros(8760) + dP4) * aperture_area, np.zeros(8760), np.zeros(8760)]  # in Pa
    supply_out_pre = np.zeros(8760)
    supply_out_total = np.zeros(8760)
    mcp = np.zeros(8760)

    # calculate net radiant heat (absorbed)
    tilt = radians(tilt_angle)
    S_vector = np.vectorize(calc_Sm_SC)(n0, IAM_b_vector, I_direct_vector, IAM_d, I_diffuse_vector,
                                           tilt)  # absorbed solar radiation in W/m2 is a mean of the group
    counter = 0
    Flag = False
    Flag2 = False
    for flow in range(6):
        Mo = 1
        TIME0 = 0
        DELT = 1  # timestep 1 hour
        delts = DELT * 3600  # convert time step in seconds
        Tfl = np.zeros([3, 1])  # create vector
        DT = np.zeros([3, 1])
        Tabs = np.zeros([3, 1])
        STORED = np.zeros([600, 1])
        TflA = np.zeros([600, 1])
        TflB = np.zeros([600, 1])
        TabsB = np.zeros([600, 1])
        TabsA = np.zeros([600, 1])
        qgainSeg = np.zeros([100, 1])
        for time in range(8760):
            Mfl = specific_flows[flow][time]
            if time < TIME0 + DELT / 2:
                for Iseg in range(101, 501):  # 400 points with the data
                    STORED[Iseg] = Tin
            else:
                for Iseg in range(1, Nseg):  # 400 points with the data
                    STORED[100 + Iseg] = STORED[200 + Iseg]
                    STORED[300 + Iseg] = STORED[400 + Iseg]

            # calculate stability criteria
            if Mfl > 0:
                stability_criteria = Mfl * Cp_waterglycol * Nseg * (DELT * 3600) / (C_eff * aperture_area)
                if stability_criteria <= 0.5:
                    print 'ERROR: stability criteria' + str(stability_criteria) + \
                          'is not reached with the aperature of ' + str(aperture_area) + 'at this flow rate ' + str(Mfl)

            Te = Te_vector[time]
            S = S_vector[time]
            Tfl[1] = 0  # mean absorber temp
            Tabs[1] = 0  # mean absorber initial tempr
            for Iseg in range(1, Nseg + 1):
                Tfl[1] = Tfl[1] + STORED[100 + Iseg] / Nseg
                Tabs[1] = Tabs[1] + STORED[300 + Iseg] / Nseg

            # first guess for Delta T
            if Mfl > 0:
                Tout = Tin + (S - (c1 + 0.5) * (Tin - Te)) / (Mfl * Cp_waterglycol / aperture_area)
                Tfl[2] = (Tin + Tout) / 2
            else:
                Tout = Te + S / (c1 + 0.5)
                Tfl[2] = Tout  # fluid temperature same as output
            DT[1] = Tfl[2] - Te

            # calculate qgain with the guess

            qgain = calc_qgain(Tfl, Tabs, S, DT, Tin, Tout, aperture_area, c1, c2, Mfl, delts, Cp_waterglycol, C_eff, Te)

            Aseg = aperture_area / Nseg
            for Iseg in range(1, Nseg + 1):
                TflA[Iseg] = STORED[100 + Iseg]
                TabsA[Iseg] = STORED[300 + Iseg]
                if Iseg > 1:
                    TinSeg = ToutSeg
                else:
                    TinSeg = Tin
                if Mfl > 0 and Mo == 1:
                    ToutSeg = ((Mfl * Cp_waterglycol * (TinSeg + 273)) / Aseg - (C_eff * (TinSeg + 273)) / (2 * delts) + qgain +
                               (C_eff * (TflA[Iseg] + 273) / delts)) / (Mfl * Cp_waterglycol / Aseg + C_eff / (2 * delts))
                    ToutSeg = ToutSeg - 273
                    TflB[Iseg] = (TinSeg + ToutSeg) / 2
                else:
                    Tfl[1] = TflA[Iseg]
                    Tabs[1] = TabsA[Iseg]
                    qgain = calc_qgain(Tfl, Tabs, S, DT, TinSeg, Tout, Aseg, c1, c2, Mfl, delts, Cp_waterglycol, C_eff, Te)
                    ToutSeg = Tout
                    if Mfl > 0:
                        TflB[Iseg] = (TinSeg + ToutSeg) / 2
                        ToutSeg = TflA[Iseg] + (qgain * delts) / C_eff
                    else:
                        TflB[Iseg] = ToutSeg
                    TflB[Iseg] = ToutSeg
                    qfluid = (ToutSeg - TinSeg) * Mfl * Cp_waterglycol / Aseg
                    qmtherm = (TflB[Iseg] - TflA[Iseg]) * C_eff / delts
                    qbal = qgain - qfluid - qmtherm
                    if abs(qbal) > 1:
                        time = time
                qgainSeg[Iseg] = qgain  # in W/m2
            # the resulting energy output
            qout = Mfl * Cp_waterglycol * (ToutSeg - Tin)
            Tabs[2] = 0
            # storage of the mean temperature
            for Iseg in range(1, Nseg + 1):
                STORED[200 + Iseg] = TflB[Iseg]
                STORED[400 + Iseg] = TabsB[Iseg]
                Tabs[2] = Tabs[2] + TabsB[Iseg] / Nseg

            # outputs
            temperature_out[flow][time] = ToutSeg
            temperature_in[flow][time] = Tin
            supply_out[flow][time] = qout / 1000  # in kW
            temperature_m[flow][time] = (Tin + ToutSeg) / 2  # Mean absorber temperature at present

            qgain = 0
            TavgB = 0
            TavgA = 0
            for Iseg in range(1, Nseg + 1):
                qgain = qgain + qgainSeg * Aseg  # W
                TavgA = TavgA + TflA[Iseg] / Nseg
                TavgB = TavgB + TflB[Iseg] / Nseg

            # OUT[9] = qgain/Area_a # in W/m2
            qmtherm = (TavgB - TavgA) * C_eff * aperture_area / delts
            qbal = qgain - qmtherm - qout

            # OUT[11] = qmtherm
            # OUT[12] = qbal
        if flow < 4:
            Auxiliary[flow] = np.vectorize(calc_Eaux_SC)(specific_flows[flow], specific_pressurelosses[flow],
                                                         Leq, aperture_area)  # in kW
        if flow == 3:
            q1 = supply_out[0]
            q2 = supply_out[1]
            q3 = supply_out[2]
            q4 = supply_out[3]
            E1 = Auxiliary[0]
            E2 = Auxiliary[1]
            E3 = Auxiliary[2]
            E4 = Auxiliary[3]
            specific_flows[4], specific_pressurelosses[4] = calc_optimal_mass_flow(q1, q2, q3, q4, E1, E2, E3, E4, 0,
                                                                                   mB0_r, mB_max_r, mB_min_r, 0,
                                                                                   dP2, dP3, dP4, aperture_area)
        if flow == 4:
            Auxiliary[flow] = np.vectorize(calc_Eaux_SC)(specific_flows[flow], specific_pressurelosses[flow],
                                                         Leq, aperture_area)  # in kW
            dp5 = specific_pressurelosses[flow]
            q5 = supply_out[flow]
            m5 = specific_flows[flow]
            ##poits where load is negative
            specific_flows[5], specific_pressurelosses[5] = calc_optimal_mass_flow_2(m5, q5, dp5)

        if flow == 5:
            supply_losses[flow] = np.vectorize(calc_qloss_net)(specific_flows[flow], Le, aperture_area, temperature_m[flow],
                                                               Te_vector, msc_max)
            supply_out_pre = supply_out[flow].copy() + supply_losses[flow].copy()
            Auxiliary[flow] = np.vectorize(calc_Eaux_SC)(specific_flows[flow], specific_pressurelosses[flow],
                                                         Leq, aperture_area)  # in kW
            supply_out_total = supply_out + 0.5 * Auxiliary[flow] - supply_losses[flow]
            mcp = specific_flows[flow] * (Cp_waterglycol / 1000)  # mcp in kW/c

    result = [supply_losses[5], supply_out_total[5], Auxiliary[5], temperature_out[flow], temperature_in[flow], mcp]
    return result


def calc_Sm_SC(n0, IAM_b, I_direct, IAM_d, I_diffuse, tilt):
    """
    Calculates the absorbed radiation for solar thermal collectors.
    :param n0: zero loss efficiency [-]
    :param IAM_b: incidence angle modifier for beam radiation [-]
    :param I_direct: direct/beam radiation [Wh/m2]
    :param IAM_d: incidence angle modifier for diffuse radiation [-]
    :param I_diffuse: diffuse radiation [Wh/m2]
    :param tilt: solar panel tilt angle [rad]
    :return S: absorbed radiation [Wh/m2]
    """
    S = n0 * IAM_b * I_direct + n0 * IAM_d * I_diffuse * (1 + cos(tilt)) / 2
    return S


def calc_qgain(Tfl, Tabs, qrad, DT, TinSub, Tout, Aseg, c1, c2, Mfl, delts, Cp_wg, C_eff, Te):
    xgain = 1
    xgainmax = 100
    exit = False
    while exit == False:
        qgain = qrad - c1 * (DT[1]) - c2 * abs(DT[1]) * DT[1]  # heat production from solar collector
        if Mfl > 0:
            Tout = ((Mfl * Cp_wg * TinSub) / Aseg - (C_eff * TinSub) / (2 * delts) + qgain + (
                C_eff * Tfl[1]) / delts) / (Mfl * Cp_wg / Aseg + C_eff / (2 * delts))
            Tfl[2] = (TinSub + Tout) / 2
            DT[2] = Tfl[2] - Te
            qdiff = Mfl / Aseg * Cp_wg * 2 * (DT[2] - DT[1])
        else:
            Tout = Tfl[1] + (qgain * delts) / C_eff
            Tfl[2] = Tout
            DT[2] = Tfl[2] - Te
            qdiff = 5 * (DT[2] - DT[1])

        if abs(qdiff < 0.1):
            DT[1] = DT[2]
            exit = True
        else:
            if xgain > 40: #FIXME: no iteration?
                DT[1] = (DT[1] + DT[2]) / 2
                if xgain == xgainmax:
                    exit = True
            else:
                DT[1] = DT[2]

    #FIXME: what is this part for?
    qout = Mfl * Cp_wg * (Tout - TinSub) / Aseg
    qmtherm = (Tfl[2] - Tfl[1]) * C_eff / delts
    qbal = qgain - qout - qmtherm
    if abs(qbal) > 1:
        qbal = qbal
    return qgain


def calc_qloss_net(Mfl, Le, Area_a, Tm, Te, maxmsc):
    """
    calculate non-recoverable losses
    :param Mfl:
    :param Le:
    :param Area_a:
    :param Tm:
    :param Te:
    :param maxmsc:
    :return:
    """

    qloss = 0.217 * Le * Area_a * (Tm - Te) * (Mfl / maxmsc) / 1000  # TODO: find reference for constant
    return qloss  # in kW


def calc_anglemodifierSC(Az_vector, g_vector, ha_vector, teta_z, tilt_angle, type_SCpanel, latitude, Sz_vector):

    def calc_teta_L(Az, teta_z, tilt, Sz):
        # calculate incident angles modifier of the longitudinal plane
        teta_la = tan(Sz) * cos(teta_z - Az)
        teta_l = degrees(abs(atan(teta_la) - tilt))  # longitudinal incidence angle
        if teta_l < 0:
            teta_l = min(89, abs(teta_l))
        if teta_l >= 90:
            teta_l = 89.999
        return teta_l  # in degrees

    def calc_teta_T(Az, Sz, teta_z):
        # calculate incident angles modifier of the transversal plane
        teta_ta = sin(Sz) * sin(abs(teta_z - Az))
        teta_T = degrees(atan(teta_ta / cos(teta_ta)))  # transversal incidence angle
        if teta_T < 0:
            teta_T = min(89, abs(teta_T))
        if teta_T >= 90:
            teta_T = 89.999
        return teta_T

   
    def calc_teta_L_max(teta_L):
        if teta_L < 0:
            teta_L = min(89, abs(teta_L))
        if teta_L >= 90:
            teta_L = 89.999
        return teta_L

    def calc_IAMb(teta_l, teta_T, type_SCpanel):
        if type_SCpanel == 1:  # # Flat plate collector   SOLEX blu SFP, 2012
            IAM_b = -0.00000002127039627042 * teta_l ** 4 + 0.00000143550893550934 * teta_l ** 3 - 0.00008493589743580050 * teta_l ** 2 + 0.00041588966590833100 * teta_l + 0.99930069929920900000
        if type_SCpanel == 2:  # # evacuated tube   Zewotherm SOL ZX-30 SFP, 2012
            IAML = -0.00000003365384615386 * teta_l ** 4 + 0.00000268745143745027 * teta_l ** 3 - 0.00010196678321666700 * teta_l ** 2 + 0.00088830613832779900 * teta_l + 0.99793706293541500000
            IAMT = 0.000000002794872 * teta_T ** 5 - 0.000000534731935 * teta_T ** 4 + 0.000027381118880 * teta_T ** 3 - 0.000326340326281 * teta_T ** 2 + 0.002973799531468 * teta_T + 1.000713286764210
            IAM_b = IAMT * IAML  # overall incidence angle modifier for beam radiation
        return IAM_b

    # convert to radians
    teta_z = radians(teta_z)
    tilt = radians(tilt_angle)

    g_vector = np.radians(g_vector)
    ha_vector = np.radians(ha_vector)
    lat = radians(latitude)
    Sz_vector = np.radians(Sz_vector)
    Az_vector = np.radians(Az_vector)
    Incidence_vector = np.vectorize(solar_equations.calc_incident_angle_beam)(g_vector, lat, ha_vector, tilt,
                                                              teta_z)  # incident angle in radians

    # calculate incident angles
    if type_SCpanel == 1:  #
        incident_angle = np.degrees(Incidence_vector)
        Teta_L = np.vectorize(calc_teta_L_max)(incident_angle)
        Teta_T = 0  # not necessary
    if type_SCpanel == 2:  #
        Teta_L = np.vectorize(calc_teta_L)(Az_vector, teta_z, tilt, Sz_vector)  # in degrees
        Teta_T = np.vectorize(calc_teta_T)(Az_vector, Sz_vector, teta_z, Incidence_vector)  # in degrees

    # calculate incident angle modifier for beam radiation
    IAM_b_vector = np.vectorize(calc_IAMb)(Teta_L, Teta_T, type_SCpanel)

    return IAM_b_vector





def calc_properties_SC(type_SCpanel):
    """
    properties of module
    :param type_SCpanel:
    :return:
    """
    if type_SCpanel == 1:  # # Flat plate collector   SOLEX blu SFP, 2012
        n0 = 0.775  # zero loss efficeincy
        c1 = 3.91  # W/m2K
        c2 = 0.0081  # W/m2K2
        # specific mass flow rates
        mB0_r = 57.98  # # in kg/h/m2   of aperture area
        mB_max_r = 86.97  # in kg/h/m2   of aperture area
        mB_min_r = 28.99  # in kg/h/m2   of aperture area
        C_eff = 8000  # thermal capacitance of module J/m2K
        t_max = 192  # stagnation temperature in C
        IAM_d = 0.87  # diffuse incident angle considered at 50 degrees
        aperture_area_ratio = 0.888  # the aperture/gross area ratio
        panel_area = 2.023  # m2
        dP1 = 0
        dP2 = 170 / (aperture_area_ratio * panel_area)
        dP3 = 270 / (aperture_area_ratio * panel_area)
        dP4 = 80 / (aperture_area_ratio * panel_area)
    if type_SCpanel == 2:  # # evacuated tube   Zewotherm SOL ZX-30 SFP, 2012
        n0 = 0.721
        c1 = 0.89  # W/m2K
        c2 = 0.0199  # W/m2K2

        # specific mass flow rates
        mB0_r = 88.2  # in kg/h/m2   of aperture area
        mB_max_r = 147.12  # in kg/h/m2
        mB_min_r = 33.10  # in kg/h/m2
        C_eff = 38000  # thermal capacitance of module anf fluid for Brine J/m2K
        t_max = 196  # stagnation temperature in C
        IAM_d = 0.91  # diffuse incident angle considered at 50 degrees
        aperture_area_ratio = 0.655  # the aperture/gross area ratio
        panel_area = 4.322  # m2
        dP1 = 0  # in Pa per m2
        dP2 = 8000 / (aperture_area_ratio * panel_area)  # in Pa per m2
        dP3 = 22000 / (aperture_area_ratio * panel_area)  # in Pa per m2
        dP4 = 2000 / (aperture_area_ratio * panel_area)  # in Pa per m2
        # Fluids Cp [kJ/kgK] Density [kg/m3] Used for
        # Water-glyucol 33%  3.68            1044 Collector Loop
        # Water 4.19             998 Secondary collector loop, store, loops for auxiliary

    return n0, c1, c2, mB0_r, mB_max_r, mB_min_r, C_eff, t_max, IAM_d, aperture_area_ratio, panel_area, dP1, dP2, dP3, dP4


def calc_Eaux_SC(qV_des, Dp_collector, Leq, Aa):
    """
    auxiliary electricity solar collectors

    :param qV_des:
    :param Dp_collector:
    :param Leq:
    :param Aa:
    :return:
    """
    Ro = 1000  # kg/m3 # TODO: change to water density from gv
    dpl = 200  # pressure losses per length of pipe according to solar districts #FIXME[Q]: reference
    Fcr = 1.3  # factor losses of accessories
    Dp_friction = dpl * Leq * Aa * Fcr  # HANZENWILIAMSN PA/M
    Eaux = (qV_des / Ro) * (Dp_collector + Dp_friction) / 0.6 / 10  # energy necesary in kW from pumps#FIXME[Q]:what are the numbers for?
    return Eaux  # energy spent in kWh



def calc_optimal_mass_flow(q1, q2, q3, q4, E1, E2, E3, E4, m1, m2, m3, m4, dP1, dP2, dP3, dP4, Area_a):
    """
    This function determine the optimal mass flow rate and the corresponding pressure drop that maximize the
    total heat production in every time-step. It is done by maximizing the energy generation function (balance equation)
    assuming the electricity requirement is twice as valuable as the thermal output of the solar collector.

    :param q1:
    :param q2:
    :param q3:
    :param q4:
    :param E1:
    :param E2:
    :param E3:
    :param E4:
    :param m1:
    :param m2:
    :param m3:
    :param m4:
    :param dP1:
    :param dP2:
    :param dP3:
    :param dP4:
    :param Area_a:
    :return:

    """

    mass_flow_opt = np.empty(8760)
    dP_opt = np.empty(8760)
    const = Area_a / 3600
    mass_flow_all = [m1 * const, m2 * const, m3 * const, m4 * const]  # float points
    dP_all = [dP1 * Area_a, dP2 * Area_a, dP3 * Area_a, dP4 * Area_a]  # float points
    balances = [q1 - E1 * 2, q2 - E2 * 2, q3 - E3 * 2, q4 - E4 * 2]  # energy generation function #TODO: ref CEA
    for time in range(8760):
        balances_time = [balances[0][time], balances[1][time], balances[2][time], balances[3][time]]
        max_heat_production = np.max(balances_time)
        ix_max_heat_production = np.where(balances_time == max_heat_production)
        mass_flow_opt[time] = mass_flow_all[ix_max_heat_production[0][0]]
        dP_opt[time] = dP_all[ix_max_heat_production[0][0]]
    return mass_flow_opt, dP_opt


def calc_optimal_mass_flow_2(m, q, dp): #FIXME[Q]: reason for this calculation?
    for time in range(8760):
        if q[time] <= 0:
            m[time] = 0
            dp[time] = 0
    return m, dp


# optimal angle and tilt

def optimal_angle_and_tilt(observers_all, latitude, worst_sh, worst_Az, transmittivity,
                           grid_side, module_lenght, angle_north, Min_Isol, Max_Isol):
    def Calc_optimal_angle(teta_z, latitude, transmissivity):
        if transmissivity <= 0.15:
            gKt = 0.977
        elif 0.15 < transmissivity <= 0.7:
            gKt = 1.237 - 1.361 * transmissivity
        else:
            gKt = 0.273
        Tad = 0.98
        Tar = 0.97
        Pg = 0.2  # ground reflectance of 0.2
        l = radians(latitude)
        a = radians(teta_z)  # this is surface azimuth
        b = atan((cos(a) * tan(l)) * (1 / (1 + ((Tad * gKt - Tar * Pg) / (2 * (1 - gKt))))))
        return degrees(b)

    def Calc_optimal_spacing(Sh, Az, tilt_angle, module_lenght):
        h = module_lenght * sin(radians(tilt_angle))
        D1 = h / tan(radians(Sh))
        D = max(D1 * cos(radians(180 - Az)), D1 * cos(radians(Az - 180)))
        return D

    def Calc_categoriesroof(teta_z, B, GB, Max_Isol):
        if -122.5 < teta_z <= -67:
            CATteta_z = 1
        elif -67 < teta_z <= -22.5:
            CATteta_z = 3
        elif -22.5 < teta_z <= 22.5:
            CATteta_z = 5
        elif 22.5 < teta_z <= 67:
            CATteta_z = 4
        elif 67 <= teta_z <= 122.5:
            CATteta_z = 2

        if 0 < B <= 5:
            CATB = 1  # flat roof
        elif 5 < B <= 15:
            CATB = 2  # tilted 25 degrees
        elif 15 < B <= 25:
            CATB = 3  # tilted 25 degrees
        elif 25 < B <= 40:
            CATB = 4  # tilted 25 degrees
        elif 40 < B <= 60:
            CATB = 5  # tilted 25 degrees
        elif B > 60:
            CATB = 6  # tilted 25 degrees

        GB_percent = GB / Max_Isol
        if 0 < GB_percent <= 0.25:
            CATGB = 1  # flat roof
        elif 0.25 < GB_percent <= 0.50:
            CATGB = 2
        elif 0.50 < GB_percent <= 0.75:
            CATGB = 3
        elif 0.75 < GB_percent <= 0.90:
            CATGB = 4
        elif 0.90 < GB_percent <= 1:
            CATGB = 5

        return CATB, CATGB, CATteta_z

    # calculate values for flat roofs Slope < 5 degrees.
    optimal_angle_flat = Calc_optimal_angle(0, latitude, transmittivity)
    optimal_spacing_flat = Calc_optimal_spacing(worst_sh, worst_Az, optimal_angle_flat, module_lenght)
    arcpy.AddField_management(observers_all, "array_s", "DOUBLE")
    arcpy.AddField_management(observers_all, "area_netpv", "DOUBLE")
    arcpy.AddField_management(observers_all, "CATB", "SHORT")
    arcpy.AddField_management(observers_all, "CATGB", "SHORT")
    arcpy.AddField_management(observers_all, "CATteta_z", "SHORT")
    fields = ('aspect', 'slope', 'GB', "array_s", "area_netpv", "CATB", "CATGB", "CATteta_z")
    # go inside the database and perform the changes
    with arcpy.da.UpdateCursor(observers_all, fields) as cursor:
        for row in cursor:
            aspect = row[0]
            slope = row[1]
            if slope > 5:  # no t a flat roof.
                B = slope
                array_s = 0
                if 180 <= aspect < 360:  # convert the aspect of arcgis to azimuth
                    teta_z = aspect - 180
                elif 0 < aspect < 180:
                    teta_z = aspect - 180  # negative in the east band
                elif aspect == 0 or aspect == 360:
                    teta_z = 180
                if -angle_north <= teta_z <= angle_north and row[2] > Min_Isol:
                    row[0] = teta_z
                    row[1] = B
                    row[3] = array_s
                    row[4] = (grid_side - array_s) / cos(radians(abs(B))) * grid_side
                    row[5], row[6], row[7] = Calc_categoriesroof(teta_z, B, row[2], Max_Isol)
                    cursor.updateRow(row)
                else:
                    cursor.deleteRow()
            else:
                teta_z = 0  # flat surface, all panels will be oriented towards south # optimal angle in degrees
                B = optimal_angle_flat
                array_s = optimal_spacing_flat
                if row[2] > Min_Isol:
                    row[0] = teta_z
                    row[1] = B
                    row[3] = array_s
                    row[4] = (grid_side - array_s) / cos(radians(abs(B))) * grid_side
                    row[5], row[6], row[7] = Calc_categoriesroof(teta_z, B, row[2], Max_Isol)
                    cursor.updateRow(row)
                else:
                    cursor.deleteRow()



# investment and maintenance costs
def calc_Cinv_SC(Area, gv):
    """
    Lifetime 35 years
    """
    InvCa = 2050 * Area / gv.SC_n  # [CHF/y]

    return InvCa





def test_solar_collector():
    gv = cea.globalvar.GlobalVariables()
    scenario_path = gv.scenario_reference
    locator = cea.inputlocator.InputLocator(scenario_path=scenario_path)
    weather_path = locator.get_default_weather()
    list_buildings_names = dbfreader.dbf2df(locator.get_building_occupancy())['Name']

    min_radiation = 0.75  # points are selected with at least a minimum production of this % from the maximum in the area.
    type_SCpanel = 1  # monocrystalline, T2 is poly and T3 is amorphous. it relates to the database of technologies
    T_in = 75 # average temeperature #FIXME:defininition
    worst_hour = 8744  # first hour of sun on the solar solstice
    misc_losses = 0.1  # cabling, resistances etc.. #TODO:delete
    sc_on_roof = True  # flag for considering PV on roof #FIXME: define
    sc_on_wall = True  # flag for considering PV on wall #FIXME: define
    longitude = 7.439583333333333
    latitude = 46.95240555555556
    date_start = gv.date_start

    for building in list_buildings_names:
        radiation = locator.get_radiation_building(building_name= building)
        radiation_metadata = locator.get_radiation_metadata(building_name= building)
        calc_SC(locator=locator, radiation_csv=radiation, metadata_csv=radiation_metadata, latitude=latitude,
                longitude=longitude, weather_path=weather_path, building_name=building,
                sc_on_roof=sc_on_roof, sc_on_wall=sc_on_wall, misc_losses=misc_losses, worst_hour=worst_hour,
                type_SCpanel=type_SCpanel, T_in=T_in, min_radiation=min_radiation, date_start=date_start)



if __name__ == '__main__':
    test_solar_collector()
