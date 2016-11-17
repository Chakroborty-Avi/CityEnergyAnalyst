"""
===========================
Mixed-integer algorithm main
===========================

"""

import time
import cea.optimization.conversion_storage.slave.least_cost as Least_Cost
import cea.optimization.conversion_storage.slave.seasonal_storage.storage_main as Storage_Opt

__author__ = "Tim Vollrath"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Tim Vollrath", "Thuy-An Nguyen", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"

def slave_main(locator, network_file_name, master_to_slave_vars, solar_features, gV):
    """
    This function calls the optimization storage and a least cost optimization fucntion.
    Both functions aim at selecting the dispatch pattern of the technologies selected by the evolutionary algorithm.

    :param locator: locator class
    :param network_file_name: name of the network file
    :param master_to_slave_vars: class MastertoSlaveVars containing the value of variables to be passed to the slave optimization
    for each individual
    :param solar_features: class solar_features
    :param gV: global variables class
    :return:
        E_oil_eq_MJ: primary energy
        CO2_kg_eq: co2 emissions
        cost_sum: accumualted costs during operation
        QUncoveredDesign: part of the design load not covered
        QUncoveredAnnual: part of the toal load not covered

    """
    t0 = time.time()
    
    # run storage optimization
    Storage_Opt.Storage_Optimization(locator, network_file_name, master_to_slave_vars, gV)
    
    # run activation pattern
    E_oil_eq_MJ, CO2_kg_eq, cost_sum,\
    QUncoveredDesign, QUncoveredAnnual = Least_Cost.Least_Cost_Optimization(locator, master_to_slave_vars,
                                                                            solar_features, gV)

    print " Slave Optimization done (", round(time.time()-t0,1)," seconds used for this task)"

    return E_oil_eq_MJ, CO2_kg_eq, cost_sum, QUncoveredDesign, QUncoveredAnnual
    
    