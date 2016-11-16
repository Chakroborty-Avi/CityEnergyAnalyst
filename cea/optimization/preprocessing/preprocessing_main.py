"""
============================
pre-processing algorithm
============================

"""

from __future__ import division
import cea.optimization.preprocessing.processheat as process_heat
from cea.technologies import substation as subsM
from cea.optimization.preprocessing import decentralized_buildings as dbM
from cea.optimization.master import summarize_network_main as nM
from cea.optimization.preprocessing import electricity
from cea.utilities import  epwreader
from cea.resources import geothermal
import cea.optimization.supportFn as sFn

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Thuy-An Nguyen", "Tim Vollrath"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


def preproccessing(locator, total_demand, building_names, weather_file, gv):
    '''
    This function aims at preprocessing all data for the optimization.

    :param locator: path to locator function
    :param total_demand: dataframe with total demand and names of all building in the area
    :param building_names: dataframe with names of all buildings in the area
    :param weather_file: path to wather file
    :param gv: path to global variables class
    :return:
    extraCosts: extra pareto optimal costs due to electricity and process heat (
    these are treated separately and not considered inside the optimization)
    extraCO2: extra pareto optimal emissions due to electricity and process heat (
    these are treated separately and not considered inside the optimization)
    extraPrim: extra pareto optimal primary energy due to electricity and process heat (
    these are treated separately and not considered inside the optimization)
    solarFeat: extraction of solar features form the results of the solar technologies calculation.
    '''

    # read weather and calculate ground temperature from geothermal model
    T_ambient = epwreader.epw_reader(weather_file)['drybulb_C']
    gv.ground_temperature = geothermal.calc_ground_temperature(T_ambient.values, gv)

    # run substation model for every building. this will calculate temperatures of supply and return at the grid side.
    print "Run substation model for each building separately"
    subsM.substation_main(locator, total_demand, building_names, gv, Flag = True) # True if disconected buildings are calculated

    # estimate what would be the operation of single buildings only for heating
    print "Heating operation pattern for single buildings"
    dbM.discBuildOp(locator, building_names, gv)

    # at first estimate a network with all the buildings connected at it.
    print "Create network file with all buildings connected"
    nM.Network_Summary(locator, total_demand, building_names, gv, "all") #"_all" key for all buildings

    # extraction of solar features form the results of the solar technologies calculation.
    print "Solar features extraction"
    solarFeat = sFn.solarRead(locator, gv)

    # estimate the extra costs, emissions and primary energy of electricity.
    print "electricity"
    elecCosts, elecCO2, elecPrim = electricity.calc_pareto_electricity(locator, gv)

    # estimate the extra costs, emissions and primary energy for process heat
    print "Process Heat "
    hpCosts, hpCO2, hpPrim = process_heat.calc_pareto_Qhp(locator, total_demand, gv)

    extraCosts = elecCosts + hpCosts
    extraCO2 = elecCO2 + hpCO2
    extraPrim = elecPrim + hpPrim

    return extraCosts, extraCO2, extraPrim, solarFeat