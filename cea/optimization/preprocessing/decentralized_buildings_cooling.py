"""
Operation for decentralized buildings
"""
from __future__ import division

import time
from math import ceil

import numpy as np
import pandas as pd

import cea.config
import cea.globalvar
import cea.inputlocator
import cea.technologies.boiler as boiler
import cea.technologies.burner as burner
import cea.technologies.chiller_absorption as chiller_absorption
import cea.technologies.chiller_vapor_compression as chiller_vapor_compression
import cea.technologies.cooling_tower as cooling_tower
import cea.technologies.direct_expansion_units as dx
import cea.technologies.solar.solar_collector as solar_collector
import cea.technologies.substation as substation
from cea.constants import HEAT_CAPACITY_OF_WATER_JPERKGK, WH_TO_J
from cea.constants import HOURS_IN_YEAR
from cea.optimization.constants import SIZING_MARGIN, T_GENERATOR_FROM_FP_C, T_GENERATOR_FROM_ET_C, \
    Q_LOSS_DISCONNECTED, ACH_TYPE_SINGLE
from cea.optimization.lca_calculations import LcaCalculations
from cea.technologies.thermal_network.thermal_network import calculate_ground_temperature


def disconnected_buildings_cooling_main(locator, building_names, config, prices, lca):
    """
    Computes the parameters for the operation of disconnected buildings output results in csv files.
    There is no optimization at this point. The different cooling energy supply system configurations are calculated
    and compared 1 to 1 to each other. it is a classical combinatorial problem.
    The six supply system configurations include:
    (VCC: Vapor Compression Chiller, ACH: Absorption Chiller, CT: Cooling Tower, Boiler)
    (AHU: Air Handling Units, ARU: Air Recirculation Units, SCU: Sensible Cooling Units)
    - config 0: Direct Expansion / Mini-split units (NOTE: this configuration is not fully built yet)
    - config 1: VCC_to_AAS (AHU + ARU + SCU) + CT
    - config 2: FP + single-effect ACH_to_AAS (AHU + ARU + SCU) + Boiler + CT
    - config 3: ET + single-effect ACH_to_AAS (AHU + ARU + SCU) + Boiler + CT
    - config 4: VCC_to_AA (AHU + ARU) + VCC_to_S (SCU) + CT
    - config 5: VCC_to_AA (AHU + ARU) + single effect ACH_S (SCU) + CT + Boiler

    Note:
    1. Only cooling supply configurations are compared here. The demand for electricity is supplied from the grid,
    and the demand for domestic hot water is supplied from electric boilers.
    2. Single-effect chillers are coupled with flat-plate solar collectors, and the double-effect chillers are coupled
    with evacuated tube solar collectors.
    :param locator: locator class with paths to input/output files
    :param building_names: list with names of buildings
    :param gv: global variable class
    :param config: cea.config
    :param prices: prices class
    :return: one .csv file with results of operations of disconnected buildings; one .csv file with operation of the
    best configuration (Cost, CO2, Primary Energy)
    """

    t0 = time.clock()

    BestData = {}
    total_demand = pd.read_csv(locator.get_total_demand())

    substation.substation_main_cooling(locator, total_demand, building_names, cooling_configuration=['aru','ahu','scu']) # todo: redundant?

    for building_name in building_names:

        ## Calculate cooling loads for different combinations
        Qc_nom_combination_SCU_W, \
        T_re_SCU_K, \
        T_sup_SCU_K, \
        mdot_SCU_kgpers = calc_combined_cooling_loads(building_name, locator, total_demand,
                                                      cooling_configuration=['scu'])

        Qc_nom_combination_AHU_ARU_W, \
        T_re_AHU_ARU_K, \
        T_sup_AHU_ARU_K, \
        mdot_AHU_ARU_kgpers = calc_combined_cooling_loads(building_name, locator, total_demand,
                                                          cooling_configuration=['ahu','aru'])

        Qc_nom_combination_AHU_ARU_SCU_W, \
        T_re_AHU_ARU_SCU_K, \
        T_sup_AHU_ARU_SCU_K, \
        mdot_AHU_ARU_SCU_kgpers = calc_combined_cooling_loads(building_name, locator, total_demand,
                                                              cooling_configuration=['ahu','aru','scu'])


        ## Get hourly hot water supply condition of Solar Collectors (SC)
        # Flate Plate Solar Collectors
        SC_FP_data, T_hw_in_FP_C, el_aux_SC_FP_Wh, q_sc_gen_FP_Wh = get_SC_data(building_name, locator, panel_type = "FP")
        Capex_a_SC_FP_USD, Opex_SC_FP_USD, Capex_SC_FP_USD = solar_collector.calc_Cinv_SC(SC_FP_data['Area_SC_m2'][0],
                                                                                          locator, config,
                                                                                          panel_type="FP")
        # Evacuated Tube Solar Collectors
        SC_ET_data, T_hw_in_ET_C, el_aux_SC_ET_Wh, q_sc_gen_ET_Wh = get_SC_data(building_name, locator, panel_type="ET")
        Capex_a_SC_ET_USD, Opex_SC_ET_USD, Capex_SC_ET_USD = solar_collector.calc_Cinv_SC(SC_ET_data['Area_SC_m2'][0],
                                                                                          locator, config,
                                                                                          panel_type="ET")

        ## Calculate ground temperatures to estimate cold water supply temperatures for absorption chiller
        T_ground_K = calculate_ground_temperature(locator,
                                                  config)  # FIXME: change to outlet temperature from the cooling towers

        ## Get maximum technology unit size
        # VCC
        VCC_cost_data = pd.read_excel(locator.get_supply_systems(), sheet_name="Chiller")
        VCC_cost_data = VCC_cost_data[VCC_cost_data['code'] == 'CH3']
        max_VCC_unit_size_W = max(VCC_cost_data['cap_max'].values)
        # ACH
        Absorption_chiller_cost_data = pd.read_excel(locator.get_supply_systems(), sheet_name="Absorption_chiller")
        Absorption_chiller_cost_data = Absorption_chiller_cost_data[
            Absorption_chiller_cost_data['type'] == ACH_TYPE_SINGLE]
        max_ACH_unit_size_W = max(Absorption_chiller_cost_data['cap_max'].values)
        # # CT
        # CT_cost_data = pd.read_excel(locator.get_supply_systems(),sheet_name="CT")
        # CT_cost_data = CT_cost_data[Absorption_chiller_cost_data['code'] == 'CT1']
        # max_CT_size_W = max(CT_cost_data['cap_max'].values)
        # # Boiler
        # Boiler_cost_data = pd.read_excel(locator.get_supply_systems(),sheet_name="Boiler")
        # Boiler_cost_data = Boiler_cost_data[Absorption_chiller_cost_data['code'] == 'BO1']
        # max_Boiler_size_W = max(Boiler_cost_data['cap_max'].values)

        ## Initialize table to save results
        # save costs of all supply configurations
        operation_results = np.zeros((6, 10))
        operation_results = log_cooling_technologies_in_result_table(operation_results)
        # save supply system activation of all supply configurations
        all_supply_activation_dict = {}


        print building_name, ' decentralized building simulation'

        ## HOURLY OPERATION
        T_re_AHU_ARU_SCU_K = np.where(T_re_AHU_ARU_SCU_K > 0.0, T_re_AHU_ARU_SCU_K, T_sup_AHU_ARU_SCU_K)

        ## 0. DX operation
        print 'simulating Config 0: Direct Expansion Units -> AHU,ARU,SCU'
        el_DX_hourly_Wh = np.vectorize(dx.calc_DX)(mdot_AHU_ARU_SCU_kgpers, T_sup_AHU_ARU_SCU_K, T_re_AHU_ARU_SCU_K)
        # add electricity costs, CO2, PE
        operation_results[0][7] = sum(lca.ELEC_PRICE * el_DX_hourly_Wh)
        operation_results[0][8] = sum(el_DX_hourly_Wh * WH_TO_J / 1E6 * lca.EL_TO_CO2 /1E3) # ton CO2
        operation_results[0][9] = sum(el_DX_hourly_Wh * WH_TO_J / 1E6 * lca.EL_TO_OIL_EQ) # MJ oil
        # activation
        all_supply_activation_dict[0] = {'DX_el_Wh': el_DX_hourly_Wh}

        ## 1. VCC (AHU + ARU + SCU) + CT
        print 'Config 1: Vapor Compression Chillers -> AHU,ARU,SCU'
        # VCC operation
        Q_VCC_AHU_ARU_SCU_size_W, \
        number_of_VCC_AHU_ARU_SCU_chillers = get_tech_size_and_number(Qc_nom_combination_AHU_ARU_SCU_W,
                                                                      max_VCC_unit_size_W)
        VCC_to_AHU_ARU_SCU_operation = np.vectorize(chiller_vapor_compression.calc_VCC)(mdot_AHU_ARU_SCU_kgpers,
                                                                              T_sup_AHU_ARU_SCU_K,
                                                                              T_re_AHU_ARU_SCU_K,
                                                                              Q_VCC_AHU_ARU_SCU_size_W,
                                                                              number_of_VCC_AHU_ARU_SCU_chillers)
        q_cw_Wh = np.asarray([x['q_cw_W'] for x in VCC_to_AHU_ARU_SCU_operation])
        el_VCC_Wh = np.asarray([x['wdot_W'] for x in VCC_to_AHU_ARU_SCU_operation])
        # CT operation
        q_CT_VCC_to_AHU_ARU_SCU_W = q_cw_Wh
        CT_VCC_to_AHU_ARU_SCU_nom_size_W = np.max(q_CT_VCC_to_AHU_ARU_SCU_W) * (1 + SIZING_MARGIN)
        el_CT_Wh = np.vectorize(cooling_tower.calc_CT)(q_CT_VCC_to_AHU_ARU_SCU_W, CT_VCC_to_AHU_ARU_SCU_nom_size_W)
        # add costs
        el_total_Wh = el_VCC_Wh + el_CT_Wh
        operation_results[1][7] += sum(lca.ELEC_PRICE * el_total_Wh)  # CHF
        operation_results[1][8] += sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_CO2 / 1E3)  # ton CO2
        operation_results[1][9] += sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_OIL_EQ)  # MJ-oil-eq
        all_supply_activation_dict[1] = {'VCC_el_Wh': el_VCC_Wh,
                                         'CT_el_Wh': el_CT_Wh}



        # 2: SC_FP + single-effect ACH (AHU + ARU + SCU) + CT + Boiler + SC_FP
        print 'Config 2: Flat-plate Solar Collectors + Single-effect Absorption chillers -> AHU,ARU,SCU'
        # calculate single-effect ACH operation
        Q_ACH_AHU_ARU_SCU_size_W, \
        number_of_ACH_AHU_ARU_SCU_chillers = get_tech_size_and_number(Qc_nom_combination_AHU_ARU_SCU_W,
                                                                      max_ACH_unit_size_W)
        T_hw_out_single_ACH_K, \
        el_single_ACH_Wh, \
        q_cw_single_ACH_Wh, \
        q_hw_single_ACH_Wh = get_ACH_operation(Q_ACH_AHU_ARU_SCU_size_W, T_ground_K, T_hw_in_FP_C,
                                               T_re_AHU_ARU_SCU_K, T_sup_AHU_ARU_SCU_K, config, locator,
                                               mdot_AHU_ARU_SCU_kgpers)
        # CT operation
        q_CT_FP_to_single_ACH_to_AHU_ARU_SCU_W = q_cw_single_ACH_Wh
        CT_FP_to_single_ACH_to_AHU_ARU_SCU_nom_size_W = np.max(q_CT_FP_to_single_ACH_to_AHU_ARU_SCU_W) * (
                1 + SIZING_MARGIN)
        el_CT_Wh = np.vectorize(cooling_tower.calc_CT)(q_CT_FP_to_single_ACH_to_AHU_ARU_SCU_W,
                                                       CT_FP_to_single_ACH_to_AHU_ARU_SCU_nom_size_W)

        # boiler operation
        if not np.isclose(Q_ACH_AHU_ARU_SCU_size_W, 0.0):
            q_boiler_FP_to_single_ACH_to_AHU_ARU_SCU_W = q_hw_single_ACH_Wh - q_sc_gen_FP_Wh
            boiler_FP_to_single_ACH_to_AHU_ARU_SCU_nom_size_W = np.max(q_boiler_FP_to_single_ACH_to_AHU_ARU_SCU_W) * (
                    1 + SIZING_MARGIN)
            # TODO: this is assuming the mdot in SC is higher than hot water in the generator
            T_re_boiler_FP_to_single_ACH_to_AHU_ARU_SCU_K = T_hw_out_single_ACH_K
            boiler_eff = np.vectorize(boiler.calc_Cop_boiler)(q_boiler_FP_to_single_ACH_to_AHU_ARU_SCU_W,
                                                              boiler_FP_to_single_ACH_to_AHU_ARU_SCU_nom_size_W,
                                                              T_re_boiler_FP_to_single_ACH_to_AHU_ARU_SCU_K)
            Q_gas_for_boiler_Wh = np.divide(q_boiler_FP_to_single_ACH_to_AHU_ARU_SCU_W, boiler_eff,
                                            out=np.zeros_like(q_boiler_FP_to_single_ACH_to_AHU_ARU_SCU_W),
                                            where=boiler_eff!=0)
        else:
            boiler_FP_to_single_ACH_to_AHU_ARU_SCU_nom_size_W = 0.0
            Q_gas_for_boiler_Wh = np.zeros(len(el_single_ACH_Wh))

        # add electricity costs
        el_total_Wh = el_single_ACH_Wh + el_aux_SC_FP_Wh + el_CT_Wh
        operation_results[2][7] = sum(lca.ELEC_PRICE * el_total_Wh)  # CHF
        operation_results[2][8] = sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_CO2 / 1E3)  # ton CO2
        operation_results[2][9] = sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_OIL_EQ)  # MJ-oil-eq
        # add gas costs
        operation_results[2][7] += sum(prices.NG_PRICE * Q_gas_for_boiler_Wh)  # CHF
        operation_results[2][8] += sum(Q_gas_for_boiler_Wh * WH_TO_J / 1E6 * lca.NG_BACKUPBOILER_TO_CO2_STD / 1E3)  # ton CO2
        operation_results[2][9] += sum(Q_gas_for_boiler_Wh * WH_TO_J / 1E6 * lca.NG_BACKUPBOILER_TO_OIL_STD)  # MJ-oil-eq

        all_supply_activation_dict[2] = {'ACH_el_Wh': el_single_ACH_Wh,
                                         'CT_el_Wh': el_CT_Wh,
                                         'FP_el_Wh': el_aux_SC_FP_Wh,
                                         'Boiler_gas_Wh': Q_gas_for_boiler_Wh,
                                         'FP_solar_Wh': q_sc_gen_FP_Wh}



        # 3: SC_ET + single-effect ACH (AHU + ARU + SCU) + CT + Boiler + SC_ET
        print 'Config 3: Evacuated Tube Solar Collectors + Single-effect Absorption chillers -> AHU,ARU,SCU'
        T_hw_out_single_ACH_K, \
        el_single_ACH_Wh, \
        q_cw_single_ACH_Wh, \
        q_hw_single_ACH_Wh = get_ACH_operation(Q_ACH_AHU_ARU_SCU_size_W, T_ground_K, T_hw_in_ET_C,
                                               T_re_AHU_ARU_SCU_K, T_sup_AHU_ARU_SCU_K, config, locator,
                                               mdot_AHU_ARU_SCU_kgpers)
        # CT operation
        q_CT_ET_to_single_ACH_to_AHU_ARU_SCU_W = q_cw_single_ACH_Wh
        CT_ET_to_single_ACH_to_AHU_ARU_SCU_nom_size_W = np.max(q_CT_ET_to_single_ACH_to_AHU_ARU_SCU_W) * (
                1 + SIZING_MARGIN)
        el_CT_Wh = np.vectorize(cooling_tower.calc_CT)(q_CT_ET_to_single_ACH_to_AHU_ARU_SCU_W,
                                                       CT_ET_to_single_ACH_to_AHU_ARU_SCU_nom_size_W)

        # burner operation
        if not np.isclose(Q_ACH_AHU_ARU_SCU_size_W, 0.0):
            q_burner_ET_single_ACH_to_AHU_ARU_SCU_W = q_hw_single_ACH_Wh - q_sc_gen_ET_Wh
            # TODO: this is assuming the mdot in SC is higher than hot water in the generator
            T_re_boiler_ET_to_single_ACH_to_AHU_ARU_SCU_K = T_hw_out_single_ACH_K
            burner_ET_to_single_ACH_to_AHU_ARU_SCU_nom_size_W = np.max(q_burner_ET_single_ACH_to_AHU_ARU_SCU_W) * (
                    1 + SIZING_MARGIN)

            burner_eff = np.vectorize(burner.calc_cop_burner)(q_burner_ET_single_ACH_to_AHU_ARU_SCU_W,
                                                              burner_ET_to_single_ACH_to_AHU_ARU_SCU_nom_size_W)
            Q_gas_for_burner_Wh = q_burner_ET_single_ACH_to_AHU_ARU_SCU_W / burner_eff
        else:
            burner_ET_to_single_ACH_to_AHU_ARU_SCU_nom_size_W = 0.0
            Q_gas_for_burner_Wh = np.zeros(len(el_single_ACH_Wh))

        # add electricity costs
        el_total_Wh = el_single_ACH_Wh + el_aux_SC_ET_Wh + el_CT_Wh
        operation_results[3][7] = sum(lca.ELEC_PRICE * el_total_Wh)  # CHF
        operation_results[3][8] = sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_CO2 / 1E3)  # ton CO2
        operation_results[3][9] = sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_OIL_EQ)  # MJ-oil-eq
        # add gas costs
        operation_results[3][7] += sum(prices.NG_PRICE * Q_gas_for_burner_Wh)  # CHF
        operation_results[3][8] += sum(Q_gas_for_burner_Wh * WH_TO_J / 1E6 * lca.NG_BACKUPBOILER_TO_CO2_STD / 1E3)  # ton CO2
        operation_results[3][9] += sum(Q_gas_for_burner_Wh * WH_TO_J / 1E6 * lca.NG_BACKUPBOILER_TO_OIL_STD)  # MJ-oil-eq

        all_supply_activation_dict[3] = {'ACH_el_Wh': el_single_ACH_Wh,
                                         'CT_el_Wh': el_CT_Wh,
                                         'ET_el_Wh': el_aux_SC_ET_Wh,
                                         'Burner_gas_Wh': Q_gas_for_burner_Wh,
                                         'ET_solar_Wh': q_sc_gen_ET_Wh}



        # 4: VCC (AHU + ARU) + VCC (SCU) + CT
        print 'Config 4: Vapor Compression Chillers (HT) -> SCU & Vapor Compression Chillers (LT) -> AHU,ARU'
        # VCC (AHU + ARU) operation
        Q_VCC_AHU_ARU_size_W, \
        number_of_VCC_AHU_ARU_chillers = get_tech_size_and_number(Qc_nom_combination_AHU_ARU_W, max_VCC_unit_size_W)
        VCC_to_AHU_ARU_operation = np.vectorize(chiller_vapor_compression.calc_VCC)(mdot_AHU_ARU_kgpers,
                                                                      T_sup_AHU_ARU_K,
                                                                      T_re_AHU_ARU_K, Q_VCC_AHU_ARU_size_W,
                                                                      number_of_VCC_AHU_ARU_chillers)
        el_VCC_to_AHU_ARU_Wh = np.asarray([x['wdot_W'] for x in VCC_to_AHU_ARU_operation])
        q_cw_VCC_to_AHU_ARU_Wh = np.asarray([x['q_cw_W'] for x in VCC_to_AHU_ARU_operation])
        # VCC(SCU) operation
        Q_VCC_SCU_size_W, \
        number_of_VCC_SCU_chillers = get_tech_size_and_number(Qc_nom_combination_SCU_W, max_VCC_unit_size_W)
        VCC_to_SCU_operation = np.vectorize(chiller_vapor_compression.calc_VCC)(mdot_SCU_kgpers, T_sup_SCU_K,
                                                                  T_re_SCU_K, Q_VCC_SCU_size_W,
                                                                  number_of_VCC_SCU_chillers)
        el_VCC_to_SCU_Wh = np.asarray([x['wdot_W'] for x in VCC_to_SCU_operation])
        q_cw_VCC_to_SCU_Wh = np.asarray([x['q_cw_W'] for x in VCC_to_SCU_operation])

        el_VCC_total_Wh = el_VCC_to_AHU_ARU_Wh + el_VCC_to_SCU_Wh

        # CT operation
        q_CT_VCC_to_AHU_ARU_and_VCC_to_SCU_W = q_cw_VCC_to_AHU_ARU_Wh + q_cw_VCC_to_SCU_Wh
        CT_VCC_to_AHU_ARU_and_VCC_to_SCU_nom_size_W = np.max(q_CT_VCC_to_AHU_ARU_and_VCC_to_SCU_W) * (
                    1 + SIZING_MARGIN)
        el_CT_Wh = np.vectorize(cooling_tower.calc_CT)(q_CT_VCC_to_AHU_ARU_and_VCC_to_SCU_W,
                                                       CT_VCC_to_AHU_ARU_and_VCC_to_SCU_nom_size_W)

        # add el costs
        el_total_Wh = el_VCC_total_Wh + el_CT_Wh
        operation_results[4][7] += sum(lca.ELEC_PRICE * el_total_Wh)  # CHF
        operation_results[4][8] += sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_CO2 / 1E3)  # ton CO2
        operation_results[4][9] += sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_OIL_EQ)  # MJ-oil-eq

        all_supply_activation_dict[4] = {'VCCLT_el_Wh': el_VCC_to_AHU_ARU_Wh,
                                         'VCCHT_el_Wh': el_VCC_to_SCU_Wh,
                                         'CT_el_Wh': el_CT_Wh}



        # 5: VCC (AHU + ARU) + ACH (SCU) + CT
        print 'Config 5: Vapor Compression Chillers(LT) -> AHU,ARU & Flate-place SC + Absorption Chillers (HT) -> SCU'
        # ACH (SCU) operation
        Qnom_ACH_SCU_W, \
        number_of_ACH_SCU_chillers = get_tech_size_and_number(Qc_nom_combination_SCU_W, max_ACH_unit_size_W)
        FP_to_single_ACH_to_SCU_operation = np.vectorize(chiller_absorption.calc_chiller_main)(mdot_SCU_kgpers,
                                                                                 T_sup_SCU_K,
                                                                                 T_re_SCU_K,
                                                                                 T_hw_in_FP_C,
                                                                                 T_ground_K,
                                                                                 ACH_TYPE_SINGLE,
                                                                                 Qnom_ACH_SCU_W,
                                                                                 locator, config)
        el_FP_ACH_to_SCU_Wh = np.asarray([x['wdot_W'] for x in FP_to_single_ACH_to_SCU_operation])
        q_cw_FP_ACH_to_SCU_Wh = np.asarray([x['q_cw_W'] for x in FP_to_single_ACH_to_SCU_operation])
        q_hw_FP_ACH_to_SCU_Wh = np.asarray([x['q_hw_W'] for x in FP_to_single_ACH_to_SCU_operation])
        T_hw_FP_ACH_to_SCU_K = np.asarray([x['T_hw_out_C'] + 273.15 for x in FP_to_single_ACH_to_SCU_operation])

        # boiler operation
        if not np.isclose(Qnom_ACH_SCU_W, 0.0):
            # boiler operation
            q_boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_W = q_hw_FP_ACH_to_SCU_Wh - q_sc_gen_FP_Wh
            # TODO: this is assuming the mdot in SC is higher than hot water in the generator
            T_re_boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_K = T_hw_FP_ACH_to_SCU_K
            boiler_FP_to_single_ACH_to_SCU_nom_size_W = np.max(q_boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_W) * (
                        1 + SIZING_MARGIN)
            boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_nom_size_W = boiler_FP_to_single_ACH_to_SCU_nom_size_W  # fixme: redundant?

            boiler_eff = boiler.calc_Cop_boiler(q_boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_W,
                                                boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_nom_size_W,
                                                T_re_boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_K)
            Q_gas_for_boiler_Wh = np.divide(q_boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_W, boiler_eff,
                                            out=np.zeros_like(q_boiler_FP_to_single_ACH_to_AHU_ARU_SCU_W),
                                            where=boiler_eff != 0)
        else:
            boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_nom_size_W = 0.0
            Q_gas_for_boiler_Wh = np.zeros(len(el_FP_ACH_to_SCU_Wh))

        # CT operation
        q_CT_VCC_to_AHU_ARU_and_single_ACH_to_SCU_W = q_cw_VCC_to_AHU_ARU_Wh + q_cw_FP_ACH_to_SCU_Wh
        CT_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_nom_size_W = np.max(
            q_CT_VCC_to_AHU_ARU_and_single_ACH_to_SCU_W) * (1 + SIZING_MARGIN)
        el_CT_Wh = np.vectorize(cooling_tower.calc_CT)(q_CT_VCC_to_AHU_ARU_and_single_ACH_to_SCU_W,
                                                       CT_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_nom_size_W)

        # add electricity costs
        el_total_Wh = el_VCC_to_AHU_ARU_Wh + el_FP_ACH_to_SCU_Wh + el_aux_SC_FP_Wh + el_CT_Wh
        operation_results[5][7] = sum(lca.ELEC_PRICE* el_total_Wh)  # CHF
        operation_results[5][8] = sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_CO2 / 1E3)  # ton CO2
        operation_results[5][9] = sum(el_total_Wh * WH_TO_J / 1E6 * lca.EL_TO_OIL_EQ)  # MJ-oil-eq
        # add gas costs
        operation_results[5][7] += sum(prices.NG_PRICE * Q_gas_for_boiler_Wh)  # CHF
        operation_results[5][
            8] += sum(Q_gas_for_boiler_Wh * WH_TO_J / 1E6 * lca.NG_BACKUPBOILER_TO_CO2_STD / 1E3)  # ton CO2
        operation_results[5][
            9] += sum(Q_gas_for_boiler_Wh * WH_TO_J / 1E6 * lca.NG_BACKUPBOILER_TO_OIL_STD)  # MJ-oil-eq

        all_supply_activation_dict[5] = {'VCCLT_el_Wh': el_VCC_to_AHU_ARU_Wh,
                                         'ACHHT_el_Wh': el_FP_ACH_to_SCU_Wh,
                                         'FP_el_Wh': el_aux_SC_FP_Wh,
                                         'CT_el_Wh': el_CT_Wh,
                                         'Boiler_NG_Wh': Q_gas_for_boiler_Wh}

        ## Calculate Capex/Opex
        # Initialize arrays
        Capex_a_USD = np.zeros((6, 1))
        Capex_total_USD = np.zeros((6, 1))
        Opex_a_fixed_USD = np.zeros((6, 1))

        print 'Cost calculations'
        # 0: DX
        print '0: DX'
        Capex_a_DX_USD, Opex_fixed_DX_USD, Capex_DX_USD = dx.calc_Cinv_DX(Qc_nom_combination_AHU_ARU_SCU_W)
        Capex_a_USD[0][0] = Capex_a_DX_USD  # FIXME: a dummy value to rule out this configuration
        Capex_total_USD[0][0] = Capex_DX_USD  # FIXME: a dummy value to rule out this configuration
        Opex_a_fixed_USD[0][0] = Opex_fixed_DX_USD


        # 1: VCC + CT
        print '1: VCC + CT'
        Capex_a_VCC_USD, Opex_fixed_VCC_USD, Capex_VCC_USD = chiller_vapor_compression.calc_Cinv_VCC(
            Qc_nom_combination_AHU_ARU_SCU_W, locator, config, 'CH3')
        Capex_a_CT_USD, Opex_fixed_CT_USD, Capex_CT_USD = cooling_tower.calc_Cinv_CT(
            CT_VCC_to_AHU_ARU_SCU_nom_size_W, locator, config, 'CT1')

        Capex_a_USD[1][0] = Capex_a_CT_USD + Capex_a_VCC_USD
        Capex_total_USD[1][0] = Capex_CT_USD + Capex_VCC_USD
        Opex_a_fixed_USD[1][0] = Opex_fixed_CT_USD + Opex_fixed_VCC_USD


        # 2: single effect ACH + CT + Boiler + SC_FP
        print '2: single effect ACH + CT + Boiler + SC_FP'
        Capex_a_ACH_USD, Opex_fixed_ACH_USD, Capex_ACH_USD = chiller_absorption.calc_Cinv_ACH(
            Qc_nom_combination_AHU_ARU_SCU_W, locator, ACH_TYPE_SINGLE, config)
        Capex_a_CT_USD, Opex_fixed_CT_USD, Capex_CT_USD = cooling_tower.calc_Cinv_CT(
            CT_FP_to_single_ACH_to_AHU_ARU_SCU_nom_size_W, locator, config, 'CT1')
        Capex_a_boiler_USD, Opex_fixed_boiler_USD, Capex_boiler_USD = boiler.calc_Cinv_boiler(
            boiler_FP_to_single_ACH_to_AHU_ARU_SCU_nom_size_W, locator, config, 'BO1')
        Capex_a_USD[2][0] = Capex_a_CT_USD + Capex_a_ACH_USD + Capex_a_boiler_USD + Capex_a_SC_FP_USD
        Capex_total_USD[2][0] = Capex_CT_USD + Capex_ACH_USD + Capex_boiler_USD + Capex_SC_FP_USD
        Opex_a_fixed_USD[2][
            0] = Opex_fixed_CT_USD + Opex_fixed_ACH_USD + Opex_fixed_boiler_USD + Opex_SC_FP_USD

        # 3: double effect ACH + CT + Boiler + SC_ET
        print '3: double effect ACH + CT + Boiler + SC_ET'
        Capex_a_ACH_USD, Opex_fixed_ACH_USD, Capex_ACH_USD = chiller_absorption.calc_Cinv_ACH(
            Qc_nom_combination_AHU_ARU_SCU_W, locator, ACH_TYPE_SINGLE, config)
        Capex_a_CT_USD, Opex_fixed_CT_USD, Capex_CT_USD = cooling_tower.calc_Cinv_CT(
            CT_ET_to_single_ACH_to_AHU_ARU_SCU_nom_size_W, locator, config, 'CT1')
        Capex_a_burner_USD, Opex_fixed_burner_USD, Capex_burner_USD = burner.calc_Cinv_burner(
            burner_ET_to_single_ACH_to_AHU_ARU_SCU_nom_size_W, locator, config, 'BO1')
        Capex_a_USD[3][0] = Capex_a_CT_USD + Capex_a_ACH_USD + Capex_a_burner_USD + Capex_a_SC_ET_USD
        Capex_total_USD[3][0] = Capex_CT_USD + Capex_ACH_USD + Capex_burner_USD + Capex_SC_ET_USD
        Opex_a_fixed_USD[3][
            0] = Opex_fixed_CT_USD + Opex_fixed_ACH_USD + Opex_fixed_burner_USD + Opex_SC_ET_USD

        # 4: VCC (AHU + ARU) + VCC (SCU) + CT
        print '4: VCC (AHU + ARU) + VCC (SCU) + CT'
        Capex_a_VCC_AA_USD, Opex_VCC_AA_USD, Capex_VCC_AA_USD = chiller_vapor_compression.calc_Cinv_VCC(
            Qc_nom_combination_AHU_ARU_W, locator, config, 'CH3')
        Capex_a_VCC_S_USD, Opex_VCC_S_USD, Capex_VCC_S_USD = chiller_vapor_compression.calc_Cinv_VCC(
            Qc_nom_combination_SCU_W, locator, config, 'CH3')
        Capex_a_CT_USD, Opex_fixed_CT_USD, Capex_CT_USD = cooling_tower.calc_Cinv_CT(
            CT_VCC_to_AHU_ARU_and_VCC_to_SCU_nom_size_W, locator, config, 'CT1')
        Capex_a_USD[4][0] = Capex_a_CT_USD + Capex_a_VCC_AA_USD + Capex_a_VCC_S_USD
        Capex_total_USD[4][0] = Capex_CT_USD + Capex_VCC_AA_USD + Capex_VCC_S_USD
        Opex_a_fixed_USD[4][0] = Opex_fixed_CT_USD + Opex_VCC_AA_USD + Opex_VCC_S_USD

        # 5: VCC (AHU + ARU) + ACH (SCU) + CT + Boiler + SC_FP
        print '5: VCC (AHU + ARU) + ACH (SCU) + CT + Boiler + SC_FP'
        Capex_a_ACH_S_USD, Opex_fixed_ACH_S_USD, Capex_ACH_S_USD = chiller_absorption.calc_Cinv_ACH(
            Qc_nom_combination_SCU_W, locator, ACH_TYPE_SINGLE, config)
        Capex_a_CT_USD, Opex_fixed_CT_USD, Capex_CT_USD = cooling_tower.calc_Cinv_CT(
            CT_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_nom_size_W, locator, config, 'CT1')
        Capex_a_boiler_USD, Opex_fixed_boiler_USD, Capex_boiler_USD = boiler.calc_Cinv_boiler(
            boiler_VCC_to_AHU_ARU_and_FP_to_single_ACH_to_SCU_nom_size_W, locator, config, 'BO1')
        Capex_a_SC_FP_USD, Opex_SC_FP_USD, Capex_SC_FP_USD = solar_collector.calc_Cinv_SC(
            SC_FP_data['Area_SC_m2'][0], locator, config, panel_type="FP")
        Capex_a_USD[5][
            0] = Capex_a_CT_USD + Capex_a_VCC_AA_USD + Capex_a_ACH_S_USD + Capex_a_SC_FP_USD + Capex_a_boiler_USD
        Capex_total_USD[5][
            0] = Capex_CT_USD + Capex_VCC_AA_USD + Capex_ACH_S_USD + Capex_SC_FP_USD + Capex_boiler_USD
        Opex_a_fixed_USD[5][
            0] = Opex_fixed_CT_USD + Opex_VCC_AA_USD + Opex_fixed_ACH_S_USD + Opex_SC_FP_USD + Opex_fixed_boiler_USD


        ## Determine the best configuration
        number_of_configuration = len(operation_results)
        Best = np.zeros((number_of_configuration, 1))
        indexBest = 0

        # write all results from the configurations into TotalCosts, TotalCO2, TotalPrim
        TAC_USD = np.zeros((number_of_configuration, 2))
        TotalCO2 = np.zeros((number_of_configuration, 2))
        TotalPrim = np.zeros((number_of_configuration, 2))
        Opex_a_USD = np.zeros((number_of_configuration, 2))
        for i in range(number_of_configuration):
            TAC_USD[i][0] = TotalCO2[i][0] = TotalPrim[i][0] = Opex_a_USD[i][0] = i
            Opex_a_USD[i][1] = Opex_a_fixed_USD[i][0] + operation_results[i][7]
            TAC_USD[i][1] = Capex_a_USD[i][0] + Opex_a_USD[i][1]
            TotalCO2[i][1] = operation_results[i][8]
            TotalPrim[i][1] = operation_results[i][9]

        # rank results
        CostsS = TAC_USD[np.argsort(TAC_USD[:, 1])]
        CO2S = TotalCO2[np.argsort(TotalCO2[:, 1])]
        PrimS = TotalPrim[np.argsort(TotalPrim[:, 1])]

        el = len(CostsS)
        rank = 0
        Bestfound = False
        optsearch = np.empty(el)
        optsearch.fill(3)
        indexBest = 0

        while not Bestfound and rank < el:
            optsearch[int(CostsS[rank][0])] -= 1
            optsearch[int(CO2S[rank][0])] -= 1
            optsearch[int(PrimS[rank][0])] -= 1
            if np.count_nonzero(optsearch) != el:
                Bestfound = True
                indexBest = np.where(optsearch == 0)[0][0]
            rank += 1

        # get the best option according to the ranking.
        Best[indexBest][0] = 1

        # Save results in csv file
        dico = {}

        dico["DX to AHU_ARU_SCU Share"] = operation_results[:, 0]
        dico["VCC to AHU_ARU_SCU Share"] = operation_results[:, 1]
        dico["single effect ACH to AHU_ARU_SCU Share (FP)"] = operation_results[:, 2]
        dico["single effect ACH to AHU_ARU_SCU Share (ET)"] = operation_results[:, 3]
        dico["VCC to AHU_ARU Share"] = operation_results[:, 4]
        dico["VCC to SCU Share"] = operation_results[:, 5]
        dico["single effect ACH to SCU Share (FP)"] = operation_results[:, 6]

        # performance indicators of the configurations
        dico["Capex_a_USD"] = Capex_a_USD[:, 0]
        dico["Capex_total_USD"] = Capex_total_USD[:, 0]
        dico["Opex_a_USD"] = Opex_a_USD[:, 1]
        dico["Opex_a_fixed_USD"] = Opex_a_fixed_USD[:, 0]
        dico["Opex_a_var_USD"] = operation_results[:, 7]
        dico["GHG_tonCO2"] = operation_results[:, 8]
        dico["PEN_MJoil"] = operation_results[:, 9]
        dico["TAC_USD"] = TAC_USD[:, 1]
        dico["Best configuration"] = Best[:, 0]
        dico["Nominal Power DX to AHU_ARU_SCU [W]"] = operation_results[:, 0] * Qc_nom_combination_AHU_ARU_SCU_W
        dico["Nominal Power VCC to AHU_ARU_SCU [W]"] = operation_results[:, 1] * Qc_nom_combination_AHU_ARU_SCU_W
        dico["Nominal Power single effect ACH to AHU_ARU_SCU (FP) [W]"] = operation_results[:,
                                                                          2] * Qc_nom_combination_AHU_ARU_SCU_W
        dico["Nominal Power single effect ACH to AHU_ARU_SCU (ET) [W]"] = operation_results[:,
                                                                          3] * Qc_nom_combination_AHU_ARU_SCU_W
        dico["Nominal Power VCC to AHU_ARU [W]"] = operation_results[:, 4] * Qc_nom_combination_AHU_ARU_W
        dico["Nominal Power VCC to SCU [W]"] = operation_results[:, 5] * Qc_nom_combination_SCU_W
        dico["Nominal Power single effect ACH to SCU (FP) [W]"] = operation_results[:, 6] * Qc_nom_combination_SCU_W

        dico_df = pd.DataFrame(dico)
        fName = locator.get_optimization_decentralized_folder_building_result_cooling(building_name, 'AHU_ARU_SCU')
        dico_df.to_csv(fName, sep=',')

        # save activation for the best supply system configuration
        best_activation_df = pd.DataFrame.from_dict(all_supply_activation_dict[indexBest]) #
        best_activation_df.to_csv(locator.get_optimization_decentralized_folder_building_cooling_activation(building_name, 'AHU_ARU_SCU'))


    print time.clock() - t0, "seconds process time for the decentralized Building Routine \n"


def log_cooling_technologies_in_result_table(result_AHU_ARU_SCU):
    """
    The cooling technologies are listed as follow:
    0: DX -> AHU,ARU,SCU
    1: VCC -> AHU,ARU,SCU
    2: FP + ACH -> AHU,ARU,SCU
    3: ET + ACH -> AHU,ARU,SCU
    4: VCC -> AHU,ARU
    5: VCC -> SCU
    6: FP + ACH -> SCU
    :param result_AHU_ARU_SCU:
    :return:
    """
    # logging the supply technology used in each configuration
    # config 0: DX
    result_AHU_ARU_SCU[0][0] = 1
    # config 1: VCC to AHU
    result_AHU_ARU_SCU[1][1] = 1
    # config 2: single-effect ACH with FP to AHU & ARU & SCU
    result_AHU_ARU_SCU[2][2] = 1
    # config 3: single-effect ACH with ET to AHU & ARU & SCU
    result_AHU_ARU_SCU[3][3] = 1
    # config 4: VCC to AHU + ARU and VCC to SCU
    result_AHU_ARU_SCU[4][4] = 1
    result_AHU_ARU_SCU[4][5] = 1
    # config 5: VCC to AHU + ARU and single effect ACH to SCU
    result_AHU_ARU_SCU[5][4] = 1
    result_AHU_ARU_SCU[5][6] = 1
    return result_AHU_ARU_SCU


def get_ACH_operation(Q_ACH_unit_size_W, T_ground_K, T_SC_hw_in_C, T_chw_re_K, T_chw_sup_K, config, locator,
                      mdot_chw_kgpers):
    SC_to_single_ACH_operation = np.vectorize(chiller_absorption.calc_chiller_main)(mdot_chw_kgpers,
                                                                                    T_chw_sup_K,
                                                                                    T_chw_re_K,
                                                                                    T_SC_hw_in_C,
                                                                                    T_ground_K,
                                                                                    ACH_TYPE_SINGLE,
                                                                                    Q_ACH_unit_size_W,
                                                                                    locator, config)
    el_single_ACH_Wh = np.asarray([x['wdot_W'] for x in SC_to_single_ACH_operation])
    q_cw_single_ACH_Wh = np.asarray([x['q_cw_W'] for x in SC_to_single_ACH_operation])
    q_hw_single_ACH_Wh = np.asarray([x['q_hw_W'] for x in SC_to_single_ACH_operation])
    T_hw_out_single_ACH_K = np.asarray([x['T_hw_out_C'] + 273.15 for x in SC_to_single_ACH_operation])
    return T_hw_out_single_ACH_K, el_single_ACH_Wh, q_cw_single_ACH_Wh, q_hw_single_ACH_Wh


def get_SC_data(building_name, locator, panel_type):
    SC_data = pd.read_csv(locator.SC_results(building_name, panel_type),
                             usecols=["T_SC_sup_C", "T_SC_re_C", "mcp_SC_kWperC", "Q_SC_gen_kWh", "Area_SC_m2",
                                      "Eaux_SC_kWh"])
    q_sc_gen_Wh = SC_data['Q_SC_gen_kWh'] * 1000
    q_sc_gen_Wh = np.where(q_sc_gen_Wh < 0.0, 0.0, q_sc_gen_Wh)
    el_aux_SC_Wh = SC_data['Eaux_SC_kWh'] * 1000
    if panel_type == "FP":
        T_hw_in_C = [x if x > T_GENERATOR_FROM_FP_C else T_GENERATOR_FROM_FP_C for x in SC_data['T_SC_re_C']]
    elif panel_type == "ET":
        T_hw_in_C = [x if x > T_GENERATOR_FROM_ET_C else T_GENERATOR_FROM_ET_C for x in SC_data['T_SC_re_C']]
    else:
        print 'invalid panel type: ', panel_type
    return SC_data, T_hw_in_C, el_aux_SC_Wh, q_sc_gen_Wh


def calc_combined_cooling_loads(building_name, locator, total_demand, cooling_configuration):
    buildings_name_with_cooling = [building_name]
    substation.substation_main_cooling(locator, total_demand, buildings_name_with_cooling, cooling_configuration)
    substation_operation = pd.read_csv(locator.get_optimization_substations_results_file(building_name, "DC", ""),
                            usecols=["T_supply_DC_space_cooling_data_center_and_refrigeration_result_K",
                                     "T_return_DC_space_cooling_data_center_and_refrigeration_result_K",
                                     "mdot_space_cooling_data_center_and_refrigeration_result_kgpers"])
    T_re_K = substation_operation["T_return_DC_space_cooling_data_center_and_refrigeration_result_K"].values
    T_sup_K = substation_operation["T_supply_DC_space_cooling_data_center_and_refrigeration_result_K"].values
    mdot_kgpers = substation_operation["mdot_space_cooling_data_center_and_refrigeration_result_kgpers"].values
    Qc_load_W = np.vectorize(calc_new_load)(mdot_kgpers, T_sup_K, T_re_K)
    Qc_design_W = Qc_load_W.max() * (1 + SIZING_MARGIN)
    return Qc_design_W, T_re_K, T_sup_K, mdot_kgpers


def get_tech_size_and_number(Qc_nom_W, max_tech_size_W):
    if Qc_nom_W <= max_tech_size_W:
        Q_installed_W = Qc_nom_W
        number_of_installation = 1
    else:
        number_of_installation = int(ceil(Qc_nom_W / max_tech_size_W))
        Q_installed_W = Qc_nom_W / number_of_installation
    return Q_installed_W, number_of_installation


# ============================
# other functions
# ============================
def calc_new_load(mdot_kgpers, T_sup_K, T_re_K):
    """
    This function calculates the load distribution side of the district heating distribution.
    :param mdot_kgpers: mass flow
    :param T_sup_K: chilled water supply temperautre
    :param T_re_K: chilled water return temperature
    :type mdot_kgpers: float
    :type TsupDH: float
    :type T_re_K: float
    :return: Q_cooling_load: load of the distribution
    :rtype: float
    """
    if mdot_kgpers > 0:
        Q_cooling_load_W = mdot_kgpers * HEAT_CAPACITY_OF_WATER_JPERKGK * (T_re_K - T_sup_K) * (
                1 + Q_LOSS_DISCONNECTED)  # for cooling load
        if Q_cooling_load_W < 0:
            raise ValueError('Q_cooling_load less than zero, check temperatures!')
    else:
        Q_cooling_load_W = 0

    return Q_cooling_load_W


# ============================
# test
# ============================


def main(config):
    """
    run the whole preprocessing routine
    """
    from cea.optimization.prices import Prices as Prices
    print('Running decentralized model for buildings with scenario = %s' % config.scenario)

    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    total_demand = pd.read_csv(locator.get_total_demand())
    building_names = total_demand.Name
    prices = Prices(locator, config)
    lca = LcaCalculations(locator, config.optimization.detailed_electricity_pricing)
    disconnected_buildings_cooling_main(locator, building_names, config, prices, lca)

    print 'test_decentralized_buildings_cooling() succeeded'


if __name__ == '__main__':
    main(cea.config.Configuration())
