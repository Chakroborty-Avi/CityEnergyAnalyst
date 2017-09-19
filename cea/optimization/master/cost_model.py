# -*- coding: utf-8 -*-
"""
============================
Extra costs to an individual
============================

"""
from __future__ import division

import os

import cea.technologies.heating_network.thermal_network as network
import numpy as np
import pandas as pd

import cea.resources.natural_gas as ngas
import cea.technologies.boilers as boiler
import cea.technologies.cogeneration as chp
import cea.technologies.furnace as furnace
import cea.technologies.heat_exchangers as hex
import cea.technologies.heatpumps as hp

import cea.technologies.pumps as pumps
import cea.technologies.solar.photovoltaic as pv
import cea.technologies.solar.photovoltaic_thermal as pvt
import cea.technologies.solar.solar_collector as stc
import cea.technologies.thermal_network as network
import cea.technologies.thermal_storage as storage

__author__ = "Tim Vollrath"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Tim Vollrath", "Thuy-An Nguyen", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


def addCosts(indCombi, buildList, locator, dicoSupply, Q_uncovered_design_W, Q_uncovered_annual_W, solarFeat, ntwFeat, gv):
    """
    Computes additional costs / GHG emisions / primary energy needs
    for the individual
    addCosts = additional costs
    addCO2 = GHG emissions
    addPrm = primary energy needs

    :param indCombi: parameter indicating if the building is connected or not
    :param buildList: list of buildings in the district
    :param locator: input locator set to scenario
    :param dicoSupply: class containing the features of a specific individual
    :param Q_uncovered_design_W: hourly max of the heating uncovered demand
    :param Q_uncovered_annual_W: total heating uncovered
    :param solarFeat: solar features
    :param ntwFeat: network features
    :param gv: global variables
    :type indCombi: string
    :type buildList: list
    :type locator: string
    :type dicoSupply: class
    :type Q_uncovered_design_W: float
    :type Q_uncovered_annual_W: float
    :type solarFeat: class
    :type ntwFeat: class
    :type gv: class

    :return: returns the objectives addCosts, addCO2, addPrim
    :rtype: tuple
    """
    addCosts = 0
    addCO2 = 0
    addPrim = 0
    nBuildinNtw = 0
    
    # Add the features from the disconnected buildings
    print "\n COSTS FROM DISCONNECTED BUILDINGS"
    os.chdir(locator.get_optimization_disconnected_folder())
    CostDiscBuild = 0
    CO2DiscBuild = 0
    PrimDiscBuild = 0
    FurnaceInvCost = 0
    CCInvCost = 0
    BoilerBInvCost = 0
    BoilerPInvCost = 0 
    HPLakeInvC = 0
    HPSewInvC = 0
    GHPInvC = 0
    PVInvC = 0
    SCInvC = 0
    PVTInvC = 0
    BoilerAddInvC = 0
    StorageHEXCost = 0
    StorageHPCost = 0
    StorageInvC = 0
    NetworkCost = 0
    SubstHEXCost = 0
    PVTHEXCost = 0
    SCHEXCost = 0
    pumpCosts = 0
    GasConnectionInvCost = 0 
    
    for (index, building_name) in zip(indCombi, buildList):
        if index == "0":
            discFileName = "DiscOp_" + building_name + "_result.csv"
            df = pd.read_csv(discFileName)
            dfBest = df[df["Best configuration"] == 1]
            CostDiscBuild += dfBest["Total Costs [CHF]"].iloc[0] # [CHF]
            CO2DiscBuild += dfBest["CO2 Emissions [kgCO2-eq]"].iloc[0] # [kg CO2]
            PrimDiscBuild += dfBest["Primary Energy Needs [MJoil-eq]"].iloc[0] # [MJ-oil-eq]

            print  dfBest["Total Costs [CHF]"].iloc[0], building_name, "disconnected"

        else:
            nBuildinNtw += 1
    
    addCosts += CostDiscBuild
    addCO2 += CO2DiscBuild
    addPrim += PrimDiscBuild
    
    # Add the features for the distribution

    if indCombi.count("1") > 0:
        os.chdir(locator.get_optimization_slave_results_folder())
        
        print " \n MACHINERY COSTS"
        # Add the investment costs of the energy systems
        # Furnace
        if dicoSupply.Furnace_on == 1:
            P_design_W = dicoSupply.Furnace_Q_max

            fNameSlavePP = locator.get_optimization_slave_pp_activation_pattern(dicoSupply.configKey)
            dfFurnace = pd.read_csv(fNameSlavePP, usecols=["Q_Furnace_W"])
            arrayFurnace_W = np.array(dfFurnace)
            
            Q_annual_W =  0
            for i in range(int(np.shape(arrayFurnace_W)[0])):
                Q_annual_W += arrayFurnace_W[i][0]
            
            FurnaceInvCost = furnace.calc_Cinv_furnace(P_design_W, Q_annual_W, gv)
            addCosts += FurnaceInvCost
            
            print furnace.calc_Cinv_furnace(P_design_W, Q_annual_W, gv), " Furnace"
        
        # CC
        if dicoSupply.CC_on == 1:
            CC_size_W = dicoSupply.CC_GT_SIZE
            CCInvCost = chp.calc_Cinv_CCT(CC_size_W, gv)
            addCosts += CCInvCost
            print chp.calc_Cinv_CCT(CC_size_W, gv), " CC"
    
        # Boiler Base
        if dicoSupply.Boiler_on == 1:
            Q_design_W = dicoSupply.Boiler_Q_max

            fNameSlavePP = locator.get_optimization_slave_pp_activation_pattern(dicoSupply.configKey)
            dfBoilerBase = pd.read_csv(fNameSlavePP, usecols=["Q_BoilerBase_W"])
            arrayBoilerBase_W = np.array(dfBoilerBase)
            
            Q_annual_W =  0
            for i in range(int(np.shape(arrayBoilerBase_W)[0])):
                Q_annual_W += arrayBoilerBase_W[i][0]
                
            BoilerBInvCost = boiler.calc_Cinv_boiler(Q_design_W, Q_annual_W, gv)
            addCosts += BoilerBInvCost
            print boiler.calc_Cinv_boiler(Q_design_W, Q_annual_W, gv), " Boiler Base "
        
        # Boiler Peak
        if dicoSupply.BoilerPeak_on == 1:
            Q_design_W = dicoSupply.BoilerPeak_Q_max

            fNameSlavePP = locator.get_optimization_slave_pp_activation_pattern(dicoSupply.configKey)
            dfBoilerPeak = pd.read_csv(fNameSlavePP, usecols=["Q_BoilerPeak_W"])
            arrayBoilerPeak_W = np.array(dfBoilerPeak)
            
            Q_annual_W =  0
            for i in range(int(np.shape(arrayBoilerPeak_W)[0])):
                Q_annual_W += arrayBoilerPeak_W[i][0]
            BoilerPInvCost = boiler.calc_Cinv_boiler(Q_design_W, Q_annual_W, gv)
            addCosts += BoilerPInvCost
            print boiler.calc_Cinv_boiler(Q_design_W, Q_annual_W, gv), " Boiler Peak"

        
        # HP Lake
        if dicoSupply.HP_Lake_on == 1:
            HP_Size_W = dicoSupply.HPLake_maxSize
            HPLakeInvC = hp.calc_Cinv_HP(HP_Size_W, gv)
            addCosts += HPLakeInvC
            print hp.calc_Cinv_HP(HP_Size_W, gv), " HP Lake"
            
        # HP Sewage
        if dicoSupply.HP_Sew_on == 1:
            HP_Size_W = dicoSupply.HPSew_maxSize
            HPSewInvC = hp.calc_Cinv_HP(HP_Size_W, gv)
            addCosts += HPSewInvC
            print hp.calc_Cinv_HP(HP_Size_W, gv), "HP Sewage"
            
        # GHP
        if dicoSupply.GHP_on == 1:
            fNameSlavePP = locator.get_optimization_slave_pp_activation_pattern(dicoSupply.configKey)
            dfGHP = pd.read_csv(fNameSlavePP, usecols=["E_GHP_req_W"])
            arrayGHP_W = np.array(dfGHP)
            
            GHP_Enom_W = np.amax(arrayGHP_W)
            GHPInvC = hp.calc_Cinv_GHP(GHP_Enom_W, gv) * gv.EURO_TO_CHF
            addCosts += GHPInvC
            print hp.calc_Cinv_GHP(GHP_Enom_W, gv) * gv.EURO_TO_CHF, " GHP"
            
        # Solar technologies

        PV_peak_kW = dicoSupply.SOLAR_PART_PV * solarFeat.A_PV_m2 * gv.nPV #kW
        PVInvC = pv.calc_Cinv_pv(PV_peak_kW)
        addCosts += PVInvC
        print pv.calc_Cinv_pv(PV_peak_kW), "PV peak"
        
        SC_area_m2 = dicoSupply.SOLAR_PART_SC * solarFeat.A_SC_m2
        SCInvC = stc.calc_Cinv_SC(SC_area_m2, gv)
        addCosts += SCInvC
        print stc.calc_Cinv_SC(SC_area_m2, gv), "SC area"
        

        PVT_peak_kW = dicoSupply.SOLAR_PART_PVT * solarFeat.A_PVT_m2 * gv.nPVT #kW
        PVTInvC = pvt.calc_Cinv_PVT(PVT_peak_kW, gv)
        addCosts += PVTInvC
        print pvt.calc_Cinv_PVT(PVT_peak_kW, gv), "PVT peak"
        
        # Back-up boiler
        BoilerAddInvC = boiler.calc_Cinv_boiler(Q_uncovered_design_W, Q_uncovered_annual_W, gv)
        addCosts += BoilerAddInvC
        print boiler.calc_Cinv_boiler(Q_uncovered_design_W, Q_uncovered_annual_W, gv), "backup boiler"
        
    
        # Hex and HP for Heat recovery
        print "\n STORAGE PART COSTS"
        if dicoSupply.WasteServersHeatRecovery == 1:
            df = pd.read_csv(
                os.path.join(locator.get_optimization_network_results_folder(), dicoSupply.NETWORK_DATA_FILE),
                usecols=["Qcdata_netw_total_kWh"])
            array = np.array(df)
            Q_HEX_max_kWh = np.amax(array)
            StorageHEXCost += hex.calc_Cinv_HEX(Q_HEX_max_kWh, gv)
            
            print hex.calc_Cinv_HEX(Q_HEX_max_kWh, gv), "Hex for data center"

            df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                             usecols=["HPServerHeatDesignArray_kWh"])
            array = np.array(df)
            Q_HP_max_kWh = np.amax(array)
            StorageHEXCost += hp.calc_Cinv_HP(Q_HP_max_kWh, gv)
            print hp.calc_Cinv_HP(Q_HP_max_kWh, gv), "HP for data center"
            
        if dicoSupply.WasteCompressorHeatRecovery == 1:
            df = pd.read_csv(
                os.path.join(locator.get_optimization_network_results_folder(), dicoSupply.NETWORK_DATA_FILE),
                usecols=["Ecaf_netw_total_kWh"])
            array = np.array(df)
            Q_HEX_max_kWh = np.amax(array)
        
            StorageHEXCost += hex.calc_Cinv_HEX(Q_HEX_max_kWh, gv)
            print hex.calc_Cinv_HEX(Q_HEX_max_kWh, gv), "Hex for compressed air"

            df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                             usecols=["HPCompAirDesignArray_kWh"])
            array = np.array(df)
            Q_HP_max_kWh = np.amax(array)

            StorageHEXCost += hp.calc_Cinv_HP(Q_HP_max_kWh, gv)
            print hp.calc_Cinv_HP(Q_HP_max_kWh, gv), "HP for compressed air"
        addCosts += StorageHEXCost
        
        # Heat pump solar to storage
        df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                         usecols=["HPScDesignArray_Wh", "HPpvt_designArray_Wh"])
        array = np.array(df)
        Q_HP_max_PVT_Wh = np.amax(array[:,1])
        QhpMax_SC_Wh = np.amax(array[:,0])
        
        StorageHPCost += hp.calc_Cinv_HP(Q_HP_max_PVT_Wh, gv)
        print hp.calc_Cinv_HP(Q_HP_max_PVT_Wh, gv), "HP for PVT"

        StorageHPCost += hp.calc_Cinv_HP(QhpMax_SC_Wh, gv)
        print hp.calc_Cinv_HP(QhpMax_SC_Wh, gv), "HP for SC"
        
        # HP for storage operation
        df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                         usecols=["E_aux_ch_W", "E_aux_dech_W", "Q_from_storage_used_W", "Q_to_storage_W"])
        array = np.array(df)
        Q_HP_max_storage_W = 0
        for i in range(gv.DAYS_IN_YEAR * gv.HOURS_IN_DAY):
            if array[i][0] > 0:
                Q_HP_max_storage_W = max(Q_HP_max_storage_W, array[i][3] + array[i][0])
            elif array[i][1] > 0:
                Q_HP_max_storage_W = max(Q_HP_max_storage_W, array[i][2] + array[i][1])
        
        StorageHPCost += hp.calc_Cinv_HP(Q_HP_max_storage_W, gv)
        addCosts += StorageHPCost

        print hp.calc_Cinv_HP(Q_HP_max_storage_W, gv), "HP for storage"
        
        
        # Storage
        df = pd.read_csv(locator.get_optimization_slave_storage_operation_data(dicoSupply.configKey),
                         usecols=["Storage_Size_m3"], nrows=1)
        StorageVol_m3 = np.array(df)[0][0]
        StorageInvC += storage.calc_Cinv_storage(StorageVol_m3, gv)
        addCosts += StorageInvC
        print storage.calc_Cinv_storage(StorageVol_m3, gv), "Storage Costs"
        
        
        # Costs from distribution configuration
        print "\n COSTS FROM NETWORK CONFIGURATION"
        if gv.ZernezFlag == 1:
            NetworkCost += network.calc_Cinv_network_linear(gv.NetworkLengthZernez, gv) * nBuildinNtw / len(buildList)
        else:
            NetworkCost += ntwFeat.pipesCosts_DHN * nBuildinNtw / len(buildList)
        addCosts += NetworkCost
        print ntwFeat.pipesCosts_DHN * nBuildinNtw / len(buildList), "Pipes Costs"
    
        # HEX (1 per building in ntw)
        for (index, building_name) in zip(indCombi, buildList):
            if index == "1":
                df = pd.read_csv(locator.get_optimization_substations_results_file(building_name),
                                 usecols=["Q_dhw_W", "Q_heating_W"])
                subsArray = np.array(df)
                
                Q_max_W = np.amax( subsArray[:,0] + subsArray[:,1] )
                SubstHEXCost += hex.calc_Cinv_HEX(Q_max_W, gv)
                print hex.calc_Cinv_HEX(Q_max_W, gv), "Hex", building_name
        addCosts += SubstHEXCost

        # HEX for solar
        roof_area_m2 = np.array(pd.read_csv(locator.get_total_demand(), usecols=["Aroof_m2"]))

        areaAvail = 0
        for i in range( len(indCombi) ):
            index = indCombi[i]
            if index == "1":
                areaAvail += roof_area_m2[i][0]
                
        for i in range( len(indCombi) ):
            index = indCombi[i]
            if index == "1":
                share = roof_area_m2[i][0] / areaAvail
                #print share, "solar area share", buildList[i]
                
                Q_max_SC_Wh = solarFeat.Q_nom_SC_Wh * dicoSupply.SOLAR_PART_SC * share
                SCHEXCost += hex.calc_Cinv_HEX(Q_max_SC_Wh, gv)
                print hex.calc_Cinv_HEX(Q_max_SC_Wh, gv), "Hex SC", buildList[i]
                
                Q_max_PVT_Wh = solarFeat.Q_nom_PVT_Wh * dicoSupply.SOLAR_PART_PVT * share
                PVTHEXCost += hex.calc_Cinv_HEX(Q_max_PVT_Wh, gv)
                print hex.calc_Cinv_HEX(Q_max_PVT_Wh, gv), "Hex PVT", buildList[i]
        addCosts += SCHEXCost
        addCosts += PVTHEXCost
        
        print addCosts,"addCosts in extraCostsMain"
        # Pump operation costs
        pumpCosts = pumps.calc_Ctot_pump(dicoSupply, buildList, locator.get_optimization_network_results_folder(), ntwFeat, gv)
        addCosts += pumpCosts
        print pumpCosts, "Pump Operation costs in extraCostsMain\n"
    
    # import gas consumption data from:

    if indCombi.count("1") > 0:
        # import gas consumption data from:
        E_gas_PrimaryDataframe_W = pd.read_csv(locator.get_optimization_slave_primary_energy_by_source(dicoSupply.configKey),
            usecols=["E_gas_PrimaryPeakPower_W"])
        E_gas_primary_peak_power_W = float(np.array(E_gas_PrimaryDataframe_W))
        GasConnectionInvCost = ngas.calc_Cinv_gas(E_gas_primary_peak_power_W, gv)
    else:
        GasConnectionInvCost = 0.0
        
    addCosts += GasConnectionInvCost
    # Save data
    results = pd.DataFrame({
                            "SCInvC":[SCInvC],
                            "PVTInvC":[PVTInvC],
                            "BoilerAddInvC":[BoilerAddInvC],
                            "StorageHEXCost":[StorageHEXCost],
                            "StorageHPCost":[StorageHPCost],
                            "StorageInvC":[StorageInvC],
                            "StorageCostSum":[StorageInvC+StorageHPCost+StorageHEXCost],
                            "NetworkCost":[NetworkCost],
                            "SubstHEXCost":[SubstHEXCost],
                            "DHNInvestCost":[addCosts - CostDiscBuild],
                            "PVTHEXCost":[PVTHEXCost],
                            "CostDiscBuild":[CostDiscBuild],
                            "CO2DiscBuild":[CO2DiscBuild],
                            "PrimDiscBuild":[PrimDiscBuild],
                            "FurnaceInvCost":[FurnaceInvCost],
                            "BoilerBInvCost":[BoilerBInvCost],
                            "BoilerPInvCost":[BoilerPInvCost],
                            "HPLakeInvC":[HPLakeInvC],
                            "HPSewInvC":[HPSewInvC],
                            "SCHEXCost":[SCHEXCost],
                            "pumpCosts":[pumpCosts],
                            "SumInvestCost":[addCosts],
                            "GasConnectionInvCa":[GasConnectionInvCost]
                            })
    results.to_csv(locator.get_optimization_slave_investment_cost_detailed(dicoSupply.configKey), sep=',')

      
    return (addCosts, addCO2, addPrim)
