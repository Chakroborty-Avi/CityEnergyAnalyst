# -*- coding: utf-8 -*-
"""
    hvac_kaempf
    ===========
    contains debugged version of HVAC model of Kämpf [1]
    originally coded by J. Fonseca
    debugged  by G. Happle
    Literature:
    [1] Kämpf, Jérôme Henri
        On the modelling and optimisation of urban energy fluxes
        http://dx.doi.org/10.5075/epfl-thesis-4548
"""

from __future__ import division
import numpy as np
from cea.utilities.physics import calc_h, calc_w, calc_t_from_h

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


"""
=========================================
all outside air unit
=========================================
"""


def calc_hvac(rhum_1, temp_1, temp_zone_set, qv_req, qe_sen, temp_5_prev, wint, gv, timestep):
    """
    HVAC model of Kämpf [1]

    Parameters
    ----------
    rhum_1 : external relative humidity at time step t (%)
    temp_1 : external air temperature at time step t (°C)
    temp_zone_set : zone air set point temperature (°C), [=Ta from calc thermal loads, including control strategy]
    qv_req : ventilation requirements at time step t according to the mixed occupancy schedule of the building (m3/s)
    qe_sen : sensible heating or cooling load to be supplied by the HVAC system at time step t in [W]
    temp_5_prev : zone air temperature at time step t-1 (°C)
    wint : internal moisture gains at time step t according to the mixed occupancy schedule of the building (kg/s)
    gv : object of class globalvar
    timestep : hour of the year [0..8760]

    Returns
    -------
    qe_hs_sen
    qe_cs_sen
    qe_hum
    qe_dehum
    pel_hum_aux
    ma_hs
    ma_cs
    ts_hs
    ts_cs
    tr_hs
    tr_cs
    w2
    w3
    t5
    """

    # State No. 5 # indoor air set point
    t5_prime = temp_zone_set

    # state after heat exchanger
    t2, w2 = calc_hex(rhum_1, gv, temp_1, temp_5_prev, timestep)  # (°C), (kg/kg)

    # print(t5_prime)
    if abs(qe_sen) != 0:  # to account for the bug of possible -0.0
        # sensible and latent loads
        qe_sen = qe_sen * 0.001  # transform in kJ/s

        # State No. 3
        # Assuming that AHU does not modify the air humidity
        w3v = w2 # virtual moisture content at state 3

        # MODIFICATIONS OF FONSECA, HSIEH and HAPPLE to the model
        # *******************************************************
        # first we guess the temperature of supply based on the sensible heating load and the required vetilation mass flow rate
        h_t5_prime_w3v = calc_h(t5_prime, w3v)  # for enthalpy change in first assumption, see Eq.(4.31) in [1]

        h_t3v_w3v = h_t5_prime_w3v + qe_sen/(gv.Pair * qv_req)  # needed enthalpy of virtual supply air with no change in w3 humidity

        t3v = calc_t_from_h(h_t3v_w3v, w3v)  # virtual supply temperature

        # evaluate t3v
        if qe_sen > 0:  # if heating
            t3 = np.nanmax([t2, np.nanmin([t3v, gv.temp_sup_heat_hvac])])
                     # heating system supply temperature in (°C) # TODO: document choose t2 if higher
            # choose higher temperature of heated air and HEX air, which is lower than maximal supply temperature
            # modification by Happle and Hsieh: HVAC supplies at inlet temperature if higher than supply temperature

        elif qe_sen < 0:  # if cooling
            t3 = np.nanmin([t2, np.nanmax([t3v, gv.temp_sup_cool_hvac])])  # cooling system supply temperature in (°C)  # TODO: document choose t2 if lower
            # choose lower temperature of cooled air and HEX air, which is higher than the minimal supply temperature

            # modification by Happle and Hsieh: HVAC supplies at inlet temperature if lower than supply temperature
        else:
            t3 = np.nan
            print('Warning: Entered HVAC calculation without sensible heat load')
            print(qe_sen)

        # initial guess of mass flow rate
        h_t5_prime_w3v = calc_h(t5_prime, w3v)  # for enthalpy change in first assumption, see Eq.(4.31) in [1]
        h_t3_w3v = calc_h(t3, w3v)  # for enthalpy change in first assumption, see Eq.(4.31) in [1]
        # Eq. (4.34) in [1] for first prediction of mass flow rater in (kg/s)
        m1 = -qe_sen / (h_t5_prime_w3v - h_t3_w3v)  # TODO: use dynamic air density

        # determine virtual state in the zone without moisture conditioning
        # moisture balance accounting for internal moisture load, see also Eq. (4.32) in [1]
        w5_prime = (wint + w3v * m1) / m1

        # room supply moisture content:
        if qe_sen > 0:  # if heating
            # algorithm for heating case
            w3 = calc_w3_heating_case(t5_prime, w2, w5_prime, t3, gv)
            ts = t3 # plus expected delta T drop in the ducts TODO: check and document value of temp increase
        elif qe_sen < 0:  # if cooling
            # algorithm for cooling case
            w3 = calc_w3_cooling_case(t5_prime, w2, t3, w5_prime)
            ts = t3 # minus expected delta T rise in the ducts TODO: check and document value of temp decrease
        else:
            ts = np.nan
            w3 = np.nan
            print('Warning: Entered HVAC calculation without sensible heat load')
            print(qe_sen)

        # State of Supply
        ws = w3

        # the new mass flow rate
        h_t5_prime_w3 = calc_h(t5_prime, w3)
        h_t3_w3 = calc_h(t3, w3)
        m = -qe_sen / (h_t5_prime_w3 - h_t3_w3)

        # TODO: now the energy of humidification and dehumidification can be calculated
        h_t2_ws = calc_h(t2, ws)
        h_t2_w2 = calc_h(t2, w2)
        qe_hum_dehum = m * (h_t2_ws - h_t2_w2) * 1000  # TODO: document energy for (de)humidification

        # TODO: could be replaced by min() and max() functions
        if qe_hum_dehum > 0:  # humidification
            qe_hum = qe_hum_dehum
            qe_dehum = 0
        elif qe_hum_dehum < 0:  # dehumidification
            qe_hum = 0
            qe_dehum = qe_hum_dehum
        else:
            qe_hum = 0
            qe_dehum = 0

        # Total loads
        h_t2_w2 = calc_h(t2, w2)
        h_ts_ws = calc_h(ts, ws)
        qe_tot = m * (h_ts_ws - h_t2_w2) * 1000  # TODO: document

        # qe_free = - m * (h_t5_prime_w3 - calc_h(temp_1, calc_w(temp_1,rhum_1))) * 1000
        # q_sen_tot = qe_tot + qe_free - qe_hum_dehum

        # Adiabatic humidifier - computation of electrical auxiliary loads
        if qe_hum > 0:
            pel_hum_aux = 15 / 3600 * m  # assuming a performance of 15 W por Kg/h of humidified air source: bertagnolo 2012
        else:
            pel_hum_aux = 0

        if qe_sen > 0:
            qe_hs_sen = qe_tot - qe_hum
            ma_hs = m
            ts_hs = ts
            tr_hs = t2
            qe_cs_sen = 0
            ma_cs = 0
            ts_cs = np.nan  # set unused temperatures to nan as they could potentially have the value 0
            tr_cs = np.nan  # set unused temperatures to nan as they could potentially have the value 0
        elif qe_sen < 0:
            qe_cs_sen = qe_tot - qe_dehum
            ma_hs = 0
            ts_hs = np.nan  # set unused temperatures to nan as they could potentially have the value 0
            tr_hs = np.nan  # set unused temperatures to nan as they could potentially have the value 0
            ma_cs = m
            ts_cs = ts
            tr_cs = t2
            qe_hs_sen = 0

        else:
            qe_hs_sen = 0
            qe_cs_sen = 0
            ma_hs = 0
            ma_cs = 0
            ts_hs = np.nan
            ts_cs = np.nan
            tr_hs = np.nan
            tr_cs = np.nan
            print('Warning: Entered HVAC calculation without sensible heat load')
            print(qe_sen)
    else:
        qe_hum = 0
        qe_dehum = 0
        qe_hs_sen = 0
        qe_cs_sen = 0
        w2 = w3 = 0
        pel_hum_aux = 0
        ma_hs = ma_cs = 0
        ts_hs = ts_cs = np.nan  # set unused temperatures to nan as they could potentially have the value 0
        tr_cs = t2  # temperature after hex
        tr_hs = t2  # temperature after hex

        # TODO: return air mass flow rates
    t5 = t5_prime  # FIXME: this should not be input or output of this function

    return qe_hs_sen, qe_cs_sen, qe_hum, qe_dehum, pel_hum_aux, ma_hs, ma_cs, ts_hs, ts_cs, tr_hs, tr_cs, w2, w3, t5


def calc_hvac_cooling(bpr, tsd, hoy, gv):
    """


    """

    temp_zone_set = tsd['theta_a'][hoy]
    rhum_1 = tsd['rh_ext'][hoy]
    temp_1 = tsd['T_ext'][hoy]
    temp_5_prev = tsd['theta_a'][hoy-1]
    qe_sen = tsd['Qcs_sen'][hoy] # get the total sensible load from the RC model, in this case without any mechanical ventilation losses??? NO!
    m_ve_hvac_req = tsd['m_ve_mech'][hoy]   # mechanical ventilation flow rate according to ventilation control
    wint = tsd['w_int'][hoy]

    # sensible cooling load provided by conditioning of ventilation air
    #  = enthalpy difference in air mass flow between supply and room temperature
    q_cs_sen_ventilation = calc_hvac_sensible_cooling_ventilaiton_air(bpr, tsd, hoy, gv)

    # calculate the part of the sensible load that is supplied by conditioning the recirculation air
    # = additional load that has to be covered by conditioning room air through recirculation
    # additional load can not be smaller than 0, over cooling situation
    q_cs_sen_recirculation = min(qe_sen - q_cs_sen_ventilation, 0) / 1000  # (kW)

    # indoor air set point
    t5 = temp_zone_set

    # ventilation air properties after heat exchanger
    t2, w2 = calc_hex(tsd, hoy, gv)  # (°C), (kg/kg)

    # State No. 3
    # Assuming that AHU does not modify the air humidity
    w3v = w2  # virtual moisture content at state 3

    # determine virtual state in the zone without moisture conditioning
    # moisture balance accounting for internal moisture load, see also Eq. (4.32) in [1]
    w5_prime = (wint + w3v * m_ve_hvac_req) / m_ve_hvac_req

    # supply air condition
    t3 = gv.temp_sup_cool_hvac

    # room supply moisture content:
    # algorithm for cooling case
    w3 = calc_w3_cooling_case(t5, w2, t3, w5_prime)

    # State of Supply
    ts = t3  # minus expected delta T rise in the ducts TODO: check and document value of temp decrease
    ws = w3

    # actual room condition
    w5 = (wint + w3 * m_ve_hvac_req) / m_ve_hvac_req
    h_w5_t5 = calc_h(t5, w5)

    # TODO: now the energy of humidification and dehumidification can be calculated
    h_t2_ws = calc_h(t2, ws)
    h_t2_w2 = calc_h(t2, w2)
    qe_hum_dehum = m_ve_hvac_req * (h_t2_ws - h_t2_w2) # (kW) TODO: document energy for (de)humidification

    # TODO: could be replaced by min() and max() functions
    if qe_hum_dehum > 0:  # humidification
        qe_hum = qe_hum_dehum
        qe_dehum = 0
    elif qe_hum_dehum < 0:  # dehumidification
        qe_hum = 0
        qe_dehum = qe_hum_dehum
    else:
        qe_hum = 0
        qe_dehum = 0

    # Total loads
    h_t2_w2 = calc_h(t2, w2)
    # h_ts_ws = calc_h(ts, ws)
    h_ts_w2 = calc_h(ts, w2)
    # qe_tot_ventilation_air = m_ve_hvac_req * (h_ts_ws - h_t2_w2)  # TODO: document
    q_cs_sen_hvac = m_ve_hvac_req * (h_ts_w2 - h_t2_w2)

    h_ts_w5 = calc_h(ts, w5)
    m_ve_hvac_recirculation = q_cs_sen_recirculation / (h_ts_w5 - h_w5_t5)

    # Adiabatic humidifier - computation of electrical auxiliary loads
    if qe_hum > 0:
        pel_hum_aux = 15 / 3600 * m_ve_hvac_req  # assuming a performance of 15 W por Kg/h of humidified air source: bertagnolo 2012
    else:
        pel_hum_aux = 0


    q_cs_sen_hvac = (q_cs_sen_hvac + q_cs_sen_recirculation) * 1000
    q_cs_lat_hvac = qe_dehum * 1000
    ma_sup_cs = m_ve_hvac_req + m_ve_hvac_recirculation
    ta_sup_cs = ts
    ta_re_cs = (m_ve_hvac_req * t2 + m_ve_hvac_recirculation * t5) / ma_sup_cs  # temperature mixing proportional to mass flow rates


    air_con_model_loads_flows_temperatures = {'q_cs_sen_hvac': q_cs_sen_hvac, \
                                              'q_cs_lat_hvac' : q_cs_lat_hvac, \
                                              'ma_sup_cs' : ma_sup_cs, \
                                              'ta_sup_cs' : ta_sup_cs, 'ta_re_cs' : ta_re_cs}

    #tsd['Qcs_sen_HVAC'][hoy] = (q_cs_sen_hvac + q_cs_sen_recirculation) * 1000
    #tsd['Qcs_lat_HVAC'][hoy] = qe_dehum * 1000
    #tsd['ma_sup_cs'][hoy] = m_ve_hvac_req + m_ve_hvac_recirculation
    #tsd['Ta_sup_cs'][hoy] = ts
    #tsd['Ta_re_cs'][hoy] = (m_ve_hvac_req * t2 + m_ve_hvac_recirculation * t5) / tsd['ma_sup_cs'][hoy]  # temperature mixing proportional to mass flow rates
    #tsd['Ehs_lat_aux'] = pel_hum_aux

    if m_ve_hvac_req + m_ve_hvac_recirculation < 0:
        raise ValueError

    return air_con_model_loads_flows_temperatures


def calc_hvac_sensible_cooling_ventilaiton_air(bpr, tsd, hoy, gv):


    temp_zone_set = tsd['theta_a'][hoy]
    rhum_1 = tsd['rh_ext'][hoy]
    temp_1 = tsd['T_ext'][hoy]
    temp_5_prev = tsd['theta_a'][hoy - 1]
    m_ve_hvac_req = tsd['m_ve_mech'][hoy]  # mechanical ventilation flow rate according to ventilation control

    # State No. 5 # indoor air set point
    t5_prime = temp_zone_set

    # state after heat exchanger
    # TODO: temperature could come from ventilation heat exchanger...
    t2, w2 = calc_hex(tsd, hoy, gv)  # (°C), (kg/kg)

    # State No. 3
    # Assuming that AHU does not modify the air humidity
    w3v = w2  # virtual moisture content at state 3

    # MODIFICATIONS HAPPLE to the model
    # *******************************************************
    # first we guess the temperature of supply based on the sensible heating load and the required vetilation mass flow rate
    h_t5_prime_w3v = calc_h(t5_prime, w3v)  # for enthalpy change in first assumption, see Eq.(4.31) in [1]

    t3 = gv.temp_sup_cool_hvac
    h_t3_w3v = calc_h(t3, w3v)  # for enthalpy change in first assumption, see Eq.(4.31) in [1]

    # calculate the part of the sensible load that can be supplied by conditioning the ventilation air
    q_cs_sen_ventilation = -m_ve_hvac_req * (h_t5_prime_w3v - h_t3_w3v)

    return q_cs_sen_ventilation * 1000 # convert from (kW) back to (W)


def calc_hvac_sensible_heating_ventilaiton_air(bpr, tsd, hoy, gv):


    temp_zone_set = tsd['Ta'][hoy]
    rhum_1 = tsd['rh_ext'][hoy]
    temp_1 = tsd['T_ext'][hoy]
    temp_5_prev = tsd['Ta'][hoy - 1]
    m_ve_hvac_req = tsd['m_ve_mech'][hoy]  # (kg/s) mechanical ventilation flow rate according to ventilation control

    # State No. 5 # indoor air set point
    t5_prime = temp_zone_set

    # state after heat exchanger
    # TODO: temperature could come from ventilation heat exchanger...
    t2, w2 = calc_hex(rhum_1, gv, temp_1, temp_5_prev, hoy)  # (°C), (kg/kg)

    # State No. 3
    # Assuming that AHU does not modify the air humidity
    w3v = w2  # virtual moisture content at state 3

    # first we guess the temperature of supply based on the sensible heating load and the required vetilation mass flow rate
    h_t5_prime_w3v = calc_h(t5_prime, w3v)  # for enthalpy change in first assumption, see Eq.(4.31) in [1]

    t3 = gv.temp_sup_heat_hvac
    h_t3_w3v = calc_h(t3, w3v)  # for enthalpy change in first assumption, see Eq.(4.31) in [1]

    # calculate the part of the sensible load that can be supplied by conditioning the ventilation air
    q_hs_sen_ventilation = -m_ve_hvac_req * (h_t5_prime_w3v - h_t3_w3v)  # (kW)

    return q_hs_sen_ventilation * 1000 # convert from (kW) back to (W)




def calc_hvac_heating(bpr, tsd, hoy, gv):
    """


    """

    temp_zone_set = tsd['Ta'][hoy]
    rhum_1 = tsd['rh_ext'][hoy]
    temp_1 = tsd['T_ext'][hoy]
    temp_5_prev = tsd['Ta'][hoy-1]
    qe_sen = tsd['Qhs_sen'][hoy] # get the total sensible load from the RC model, in this case without any mechanical ventilation losses???
    m_ve_hvac_req = tsd['m_ve_mech'][hoy]   # (kg/s) mechanical ventilation flow rate according to ventilation control
    wint = tsd['w_int'][hoy]

    # sensible heating load provided by conditioning of ventilation air
    #  = enthalpy difference in air mass flow between supply and room temperature
    q_hs_sen_ventilation = calc_hvac_sensible_heating_ventilaiton_air(bpr, tsd, hoy, gv)

    # calculate the part of the sensible load that is supplied by conditioning the recirculation air
    # = additional load that has to be covered by conditioning room air through recirculation
    # additional load can not be smaller than 0, over cooling situation
    q_hs_sen_recirculation = max(qe_sen - q_hs_sen_ventilation, 0) / 1000

    # State No. 5 # indoor air set point
    t5 = temp_zone_set

    # state after heat exchanger
    t2, w2 = calc_hex(rhum_1, gv, temp_1, temp_5_prev, hoy)  # (°C), (kg/kg)

    # State No. 3
    # Assuming that AHU does not modify the air humidity
    w3v = w2  # virtual moisture content at state 3

    # determine virtual state in the zone without moisture conditioning
    # moisture balance accounting for internal moisture load, see also Eq. (4.32) in [1]
    w5_prime = (wint + w3v * m_ve_hvac_req) / m_ve_hvac_req

    t3 = gv.temp_sup_heat_hvac

    # room supply moisture content:
    # algorithm for heating case
    w3 = calc_w3_heating_case(t5, w2, w5_prime, t3, gv)
    ts = t3 # minus expected delta T rise in the ducts TODO: check and document value of temp decrease

    # State of Supply
    ws = w3

    # actual room condition
    w5 = (wint + w3 * m_ve_hvac_req) / m_ve_hvac_req
    h_w5_t5 = calc_h(t5, w5)

    # TODO: now the energy of humidification and dehumidification can be calculated
    h_t2_ws = calc_h(t2, ws)
    h_t2_w2 = calc_h(t2, w2)
    qe_hum_dehum = m_ve_hvac_req * (h_t2_ws - h_t2_w2)  # (kW) TODO: document energy for (de)humidification

    # TODO: could be replaced by min() and max() functions
    if qe_hum_dehum > 0:  # humidification
        qe_hum = qe_hum_dehum
        qe_dehum = 0
    elif qe_hum_dehum < 0:  # dehumidification
        qe_hum = 0
        qe_dehum = qe_hum_dehum
    else:
        qe_hum = 0
        qe_dehum = 0

    # Total loads
    h_t2_w2 = calc_h(t2, w2)
    # h_ts_ws = calc_h(ts, ws)
    h_ts_w2 = calc_h(ts, w2)
    # qe_tot_ventilation_air = m_ve_hvac_req * (h_ts_ws - h_t2_w2)  # TODO: document
    q_hs_sen_hvac = m_ve_hvac_req * (h_ts_w2 - h_t2_w2)

    h_ts_w5 = calc_h(ts, w5)

    m_ve_hvac_recirculation = q_hs_sen_recirculation / (h_ts_w5 - h_w5_t5)

    # qe_free = - m * (h_t5_prime_w3 - calc_h(temp_1, calc_w(temp_1,rhum_1))) * 1000
    # q_sen_tot = qe_tot + qe_free - qe_hum_dehum

    # Adiabatic humidifier - computation of electrical auxiliary loads
    if qe_hum > 0:
        pel_hum_aux = 15 / 3600 * m_ve_hvac_req  # assuming a performance of 15 W por Kg/h of humidified air source: bertagnolo 2012
    else:
        pel_hum_aux = 0


    tsd['Qhs_sen_HVAC'][hoy] = (q_hs_sen_hvac + q_hs_sen_recirculation * 1000)
    tsd['Qhs_lat_HVAC'][hoy] = qe_dehum * 1000
    tsd['ma_sup_hs'][hoy] = m_ve_hvac_req + m_ve_hvac_recirculation
    tsd['Ta_sup_hs'][hoy] = ts
    tsd['Ta_re_hs'][hoy] = (m_ve_hvac_req * t2 + m_ve_hvac_recirculation * t5) / tsd['ma_sup_hs'][hoy]  # temperature mixing proportional to mass flow rates
    tsd['Ehs_lat_aux'] = pel_hum_aux

    return


"""
=========================================
air Heat exchanger unit
=========================================
"""
def calc_hex(tsd, hoy, gv):
    """
    Calculates air properties of mechanical ventilation system with heat exchanger
    Modeled after 2.4.2 in SIA 2044

    Parameters
    ----------
    rel_humidity_ext : (%)
    gv : globalvar
    qv_mech : required air volume flow (kg/s)
    temp_ext : external temperature at time t (°C)
    temp_zone_prev : ventilation zone air temperature at time t-1 (°C)

    Returns
    -------
    t2, w2 : temperature and moisture content of inlet air after heat exchanger

    """
    # TODO add literature

    rel_humidity_ext = tsd['rh_ext'][hoy]
    temp_ext = tsd['T_ext'][hoy]

    # FIXME: dynamic HEX efficiency
    # Properties of heat recovery and required air incl. Leakage
    # qv_mech = qv_mech * 1.0184  # in m3/s corrected taking into account leakage # TODO: add source
    # Veff = gv.Vmax * qv_mech / qv_mech_dim  # Eq. (85) in SIA 2044
    # nrec = gv.nrec_N - gv.C1 * (Veff - 2)  # heat exchanger coefficient # TODO: add source
    nrec = gv.nrec_N  # for now use constant efficiency for heat recovery

    # State No. 1
    w1 = calc_w(temp_ext, rel_humidity_ext)  # outdoor moisture (kg/kg)

    # State No. 2
    # inlet air temperature after HEX calculated from zone air temperature at time step t-1 (°C)
    t2 = tsd['theta_ve_mech'][hoy]
    w2 = min(w1, calc_w(t2, 100))  # inlet air moisture (kg/kg), Eq. (4.24) in [1]

    # TODO: document
    # bypass heat exchanger if use is not beneficial
    #if temp_zone_prev > temp_ext and not gv.is_heating_season(timestep):
        #t2 = temp_ext
        #w2 = w1
        # print('bypass HEX cooling')
    #elif temp_zone_prev < temp_ext and gv.is_heating_season(timestep):
        #t2 = temp_ext
        #w2 = w1
        # print('bypass HEX heating')

    return t2, w2


"""
=========================================
Moisture balance
=========================================
"""

def calc_w3_heating_case(t5, w2, w5, t3, gv):
    """
    Algorithm 1 Determination of the room's supply moisture content (w3) for the heating case
     from Kaempf's HVAC model [1]

    Source:
    [1] Kämpf, Jérôme Henri
        On the modelling and optimisation of urban energy fluxes
        http://dx.doi.org/10.5075/epfl-thesis-4548


    Parameters
    ----------
    t5 : temperature 5 in (°C)
    w2 : moisture content 2 in (kg/kg dry air)
    w5 : moisture content 5 in (kg/kg dry air)
    t3 : temperature 3 in (°C)
    gv : globalvar

    Returns
    -------
    w3 : moisture content of HVAC supply air in (kg/kg dry air)
    """

    # get constants and properties
    temp_comf_max = gv.temp_comf_max  # limits of comfort in zone TODO: get from properties
    hum_comf_max = gv.rhum_comf_max  # limits of comfort in zone TODO: get from properties

    w_liminf = calc_w(t5, 30)  # TODO: document
    w_limsup = calc_w(t5, 70)  # TODO: document
    w_comf_max = calc_w(temp_comf_max, hum_comf_max)  # moisture content at maximum comfortable state

    if w5 < w_liminf:
        # humidification
        w3 = w_liminf - w5 + w2

    elif w5 > w_limsup and w5 < w_comf_max:
        # heating and no dehumidification
        # delta_HVAC = calc_t(w5,70)-t5
        w3 = w2

    elif w5 > w_comf_max:
        # dehumidification
        w3 = max(min(min(w_comf_max - w5 + w2, calc_w(t3, 100)), w_limsup - w5 + w2), 0)

    else:
        # no moisture control
        w3 = w2

    return w3


def calc_w3_cooling_case(t5, w2, t3, w5):
    """
    Algorithm 2 Determination of the room's supply moisture content (w3) for the cooling case from Kaempf's HVAC model
    for non-evaporative cooling

    Source:
    [1] Kämpf, Jérôme Henri
        On the modelling and optimisation of urban energy fluxes
        http://dx.doi.org/10.5075/epfl-thesis-4548


    Parameters
    ----------
    t5 : temperature 5 in (°C)
    w2 : moisture content 2 in (kg/kg dry air)
    t3 : temperature 3 in (°C)
    w5 : moisture content 5 in (kg/kg dry air)

    Returns
    -------
    w3 : moisture content of HVAC supply air in (kg/kg dry air)
    """

    # get constants and properties
    w_liminf = calc_w(t5, 30)  # TODO: document
    w_limsup = calc_w(t5, 70)  # TODO: document

    if w5 > w_limsup:
        # dehumidification
        w3 = max(min(w_limsup - w5 + w2, calc_w(t3, 100)), 0)

    elif w5 < w_liminf:
        # humidification
        w3 = w_liminf - w5 + w2

    else:
        w3 = min(w2, calc_w(t3, 100))

    return w3
