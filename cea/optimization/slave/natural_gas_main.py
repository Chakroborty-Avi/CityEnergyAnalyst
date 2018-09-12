"""
Natural Gas Imports Script

This script calculates the imports of natural gas for a neighborhood to provide heating/cooling.
It has two loops: one for each of heating network and cooling network
This is then combined to calculate the total natural gas imports and the corresponding file is saved in the
respective folder
"""
from __future__ import division
from __future__ import print_function

import os
import pandas as pd
import numpy as np
import cea.config
import cea.inputlocator
from cea.optimization.lca_calculations import lca_calculations
from cea.constants import WH_TO_J

__author__ = "Sreepathi Bhargava Krishna"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Sreepathi Bhargava Krishna"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

def natural_gas_imports(generation, individual, locator, config):

    NG_total_heating_W = np.zeros(8760)
    NG_total_cooling_W = np.zeros(8760)
    NG_total_W = np.zeros(8760)

    if config.district_heating_network:
        data_heating = pd.read_csv(os.path.join(locator.get_optimization_slave_heating_activation_pattern(individual, generation)))
        NG_used_HPSew_W = data_heating["NG_used_HPSew_W"]
        NG_used_HPLake_W = data_heating["NG_used_HPLake_W"]
        NG_used_GHP_W = data_heating["NG_used_GHP_W"]
        NG_used_CHP_W = data_heating["NG_used_CHP_W"]
        NG_used_Furnace_W = data_heating["NG_used_Furnace_W"]
        NG_used_BaseBoiler_W = data_heating["NG_used_BaseBoiler_W"]
        NG_used_PeakBoiler_W = data_heating["NG_used_PeakBoiler_W"]
        NG_used_BackupBoiler_W = data_heating["NG_used_BackupBoiler_W"]

        for hour in range(8760):
            NG_total_heating_W[hour] = NG_used_HPSew_W[hour] + NG_used_HPLake_W[hour] + NG_used_GHP_W[hour] + \
                                       NG_used_CHP_W[hour] + NG_used_Furnace_W[hour] + NG_used_BaseBoiler_W[hour] + \
                                       NG_used_PeakBoiler_W[hour] + NG_used_BackupBoiler_W[hour]

        date = data_heating.DATE.values

        print (1)


    if config.district_cooling_network:
        data_cooling = pd.read_csv(
            os.path.join(locator.get_optimization_slave_cooling_activation_pattern(individual, generation)))

        # Natural Gas supply for the CCGT plant
        lca = lca_calculations(locator, config)
        co2_CCGT = data_cooling['CO2_from_using_CCGT']
        E_gen_CCGT_W = data_cooling['E_gen_CCGT_associated_with_absorption_chillers_W']
        NG_used_CCGT_W = np.zeros(8760)
        for hour in range(8760):
            NG_used_CCGT_W[hour] = (co2_CCGT[hour] + E_gen_CCGT_W[hour] * lca.EL_TO_CO2 * 3600E-6) * 1.0E6 / (lca.NG_CC_TO_CO2_STD * WH_TO_J)
            NG_total_cooling_W[hour] = NG_used_CCGT_W[hour]

        date = data_cooling.DATE.values


    for i in range(8760):
        NG_total_W[hour] = NG_total_heating_W[hour] + NG_total_cooling_W[hour]


    results = pd.DataFrame({"DATE": date,
                            "NG_total_W": NG_total_W})

    results.to_csv(locator.get_optimization_slave_natural_gas_imports(individual, generation), index=False)

    return results

def main(config):
    locator = cea.inputlocator.InputLocator(config.scenario)
    generation = 2
    individual = 2
    print("Calculating imports of natural gas of individual" + str(individual) + " of generation " + str(generation))

    natural_gas_imports(generation, individual, locator, config)


if __name__ == '__main__':
    main(cea.config.Configuration())