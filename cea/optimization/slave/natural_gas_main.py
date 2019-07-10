"""
Natural Gas Imports Script

This script calculates the imports of natural gas for a neighborhood to provide heating/cooling.
It has two loops: one for each of heating network and cooling network
This is then combined to calculate the total natural gas imports and the corresponding file is saved in the
respective folder
"""
from __future__ import division
from __future__ import print_function

import cea.config
import cea.inputlocator

__author__ = "Sreepathi Bhargava Krishna"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Sreepathi Bhargava Krishna"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def natural_gas_imports(heating_dispatch,
                        cooling_dispatch):
    NG_used_HPSew_W = heating_dispatch["NG_used_HPSew_W"]
    NG_used_HPLake_W = heating_dispatch["NG_used_HPLake_W"]
    NG_used_GHP_W = heating_dispatch["NG_used_GHP_W"]
    NG_used_CHP_W = heating_dispatch["NG_used_CHP_W"]
    NG_used_Furnace_W = heating_dispatch["NG_used_Furnace_W"]
    NG_used_BaseBoiler_W = heating_dispatch["NG_used_BaseBoiler_W"]
    NG_used_PeakBoiler_W = heating_dispatch["NG_used_PeakBoiler_W"]
    NG_used_BackupBoiler_W = heating_dispatch["NG_used_BackupBoiler_W"]
    NG_used_CCGT_W = cooling_dispatch["NG_used_CCGT_W"]

    NG_total_heating_W = [a + b + c + d + e + f + g + h for a, b, c, d, e, f, g, h in
                          zip(NG_used_HPSew_W, NG_used_HPLake_W, NG_used_GHP_W, NG_used_CHP_W, NG_used_Furnace_W, \
                              NG_used_BaseBoiler_W, NG_used_PeakBoiler_W, NG_used_BackupBoiler_W)]

    NG_total_cooling_W = NG_used_CCGT_W

    NG_total_W = NG_total_heating_W + NG_total_cooling_W

    naturalgas_dispatch = {
        "NG_GRID_connected_W": NG_total_W,
        "NG_GRID_heating_connected_W": NG_total_heating_W,
        "NG_GRID_cooling_connected_W": NG_total_cooling_W,
        "NG_used_HPSew_W": NG_used_HPSew_W,
        "NG_used_HPLake_W": NG_used_HPLake_W,
        "NG_used_GHP_W": NG_used_GHP_W,
        "NG_used_CHP_W": NG_used_CHP_W,
        "NG_used_Furnace_W": NG_used_Furnace_W,
        "NG_used_BaseBoiler_W": NG_used_BaseBoiler_W,
        "NG_used_PeakBoiler_W": NG_used_PeakBoiler_W,
        "NG_used_BackupBoiler_W": NG_used_BackupBoiler_W,
        "NG_used_CCGT_W": NG_used_CCGT_W
    }

    return naturalgas_dispatch


def main(config):
    locator = cea.inputlocator.InputLocator(config.scenario)
    generation = 2
    individual = 2
    print("Calculating imports of natural gas of individual" + str(individual) + " of generation " + str(generation))
    district_heating_network = config.optimization.district_heating_network
    district_cooling_network = config.optimization.district_cooling_network

    natural_gas_imports(generation, individual, locator, district_heating_network, district_cooling_network)


if __name__ == '__main__':
    main(cea.config.Configuration())
