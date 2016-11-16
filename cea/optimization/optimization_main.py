"""
============================
multi-objective optimization of supply systems for the CEA

============================

"""

from __future__ import division

import cea.optimization.master.master_main as master
import pandas as pd

import cea.optimization.network.network_opt_main as network_opt
from cea.optimization.preprocessing.preprocessing_main import preproccessing

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Thuy-an Ngugen", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


#============================
# optimization
#============================


def moo_optimization(locator, weather_file, gv):
    '''
    This function optimizes the conversion, storage and distribution systems of a heating network for the case study.
    It requires that solar technologies be calculated in advance and nodes of a network should have been already generated.
    :param locator: path to input locator
    :param weather_file: path to weather file
    :param gv: global variables class
    :return:
    '''

    # read total demand file and names and number of all buildings
    total_demand = pd.read_csv(locator.get_total_demand())
    building_names = total_demand.Name.values
    gv.num_tot_buildings = total_demand.Name.count()

    # preprocess information regarding resources and technologies (they are treated before the optimization)
    # optimize best systems for every individual building (they will compete against a district network solution)
    print "PRE-PROCESSING + SINGLE BUILDING OPTIMIZATION"
    extra_costs, extra_CO2, extra_prim, solarFeat = preproccessing(locator, total_demand, building_names, weather_file, gv)

    # optimize the network and linearalize the results (at the moment, there is only a linearilization of values in Zug)
    print "NETWORK OPTIMIZATION"
    ntwFeat = network_opt.network_opt_main()

    # optimize conversion systems
    print "CONVERSION AND STORAGE OPTIMIZATION"
    master.evolutionary_algo_main(locator, building_names, extra_costs, extra_CO2, extra_prim, solarFeat, ntwFeat, gv)


#============================
#test
#============================


def run_as_script(scenario_path=None):
    """
    run the whole optimization routine
    """
    import cea.inputlocator
    import cea.globalvar
    gv = cea.globalvar.GlobalVariables()

    if scenario_path is None:
        scenario_path = gv.scenario_reference

    locator = cea.inputlocator.InputLocator(scenario_path=scenario_path)
    weather_file = locator.get_default_weather()
    moo_optimization(locator=locator, weather_file= weather_file, gv=gv)

    print 'test_optimization_main() succeeded'

if __name__ == '__main__':
    run_as_script()

