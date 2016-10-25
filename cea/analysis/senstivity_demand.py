# -*- coding: utf-8 -*-
"""
===========================
Sensitivity of demand_main.py

This script uses the morris algorithm (morris 1991)(campologo 2011) and Sobol Algorithm Sltalli 20110
to screen the most sensitive variables of a selection of parameters of the CEA.
Th morris method serves to basic screening o finput variables and it is base on OAT
The Sobol method serves for a complete sensitivity analysis of input variables. It is based on variance methods.

===========================

"""
from __future__ import division

from cea.demand import demand_main

import multiprocessing as mp
from SALib.analyze import sobol, morris
from SALib.sample.saltelli import sample as sampler_sobol
from SALib.sample.morris import sample as sampler_morris
import pandas as pd
import numpy as np
import time

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"

# main
def sensitivity_main(locator, weather_path, gv, output_parameters, groups_var, num_samples, method):
    """
    This function creates the sensitivity analysis problem for either sobol or morris methods.
    It calculates the number of samples for the analysis and calls the CEA to run every sample.


    :param locator: locator class
    :param weather_path: path to weather file
    :param gv: global variables class
    :param output_parameters: list of output parameters to analyse
    :param groups_var: list with group names of variables to analyse. it relates the database of
    uncertaintity variables of the CEA:  locator.get_uncertainty_db()
    :param num_samples: number of samples to calculate
    :param method: 'morris' or 'sobol' methods
    :return: .xls file stored in locator.get_sensitivity_output(). every spreadsheet of the workbook
    stores a matrix whose content is the output of one sensitivity parameter and one output_parameter:

    - columns: groups of variables to anlyse.
    - rows: number of buildings of the case study under analysis.
    - content: sensitivity parameter per output parameter

    every sensitivity parameter depends on the method:

    - sobol: S1, ST and ST_conf >>for more information refereto SaBil documentation
    - morris: mu_star, sigma and mu_star_conf >> for more information refereto SaBil documentation

    """
    t0 = time.clock()

    #Model constants
    gv.multiprocessing = False # false to deactivate the multiprocessing in the demand algorithm
                               # multiprocessing will be activated in this algorithm.
    gv.resol = 'monthly'
    gv.output_type = 'sensitivity'

    #Define the model inputs
    for group in groups_var:
        variables = pd.read_excel(locator.get_uncertainty_db(), group)

    num_vars = variables.name.count() #integer with number of variables
    names = variables.name.values # [,,] with names of each variable
    bounds = []
    for var in range(num_vars):
        limits = [variables.loc[var,'min'],variables.loc[var,'max']]
        bounds.append(limits)

    #define the problem
    problem = {'num_vars': num_vars,'names': names, 'bounds': bounds, 'groups': None}

    #create samples (combinations of variables)
    if method is 'sobol':
        second_order = False
        samples = sampler_sobol(problem, N=num_samples, calc_second_order=second_order)
    else:
        grid = 2
        levels = 4
        optimal_trajects = int(0.04*num_samples)
        samples = sampler_morris(problem, N=num_samples, grid_jump=grid, num_levels=levels,

                                 optimal_trajectories=optimal_trajects, local_optimization=True)
    gv.log('Sampling done, time elapsed: %(time_elapsed).2f seconds', time_elapsed=time.clock() - t0)
    gv.log('Running %i samples' %len(samples))

    #call the CEA for building demand and store the results of every sample in a vector
    simulations = screening_cea_multiprocessing(samples, names, output_parameters, locator, weather_path, gv)

    gv.log('Simulations done - time elapsed: %(time_elapsed).2f seconds', time_elapsed=time.clock() - t0)
    #do morris analysis and output to excel
    buildings_num = simulations[0].shape[0]
    writer = pd.ExcelWriter(locator.get_sensitivity_output(method, num_samples))
    for parameter in output_parameters:
        results_1 = []
        results_2 = []
        results_3 = []
        for building in range(buildings_num):
            simulations_parameter = np.array([x.loc[building, parameter] for x in simulations])
            if method is 'sobol':
                sobol_result = sobol.analyze(problem, simulations_parameter, calc_second_order=second_order)
                results_1.append(sobol_result['S1'])
                results_2.append(sobol_result['ST'])
                results_3.append(sobol_result['ST_conf'])
            else:
                morris_result = morris.analyze(problem, samples, simulations_parameter, grid_jump=grid, num_levels=levels)
                results_1.append(morris_result['mu_star'])
                results_2.append(morris_result['sigma'])
                results_3.append(morris_result['mu_star_conf'])
        pd.DataFrame(results_1, columns = problem['names']).to_excel(writer,parameter+'S1')
        pd.DataFrame(results_2, columns=problem['names']).to_excel(writer, parameter+'ST')
        pd.DataFrame(results_3, columns=problem['names']).to_excel(writer, parameter + 'conf')

    writer.save()
    gv.log('Sensitivity analysis done - time elapsed: %(time_elapsed).2f seconds', time_elapsed=time.clock() - t0)

# function to call cea
def screening_cea_multiprocessing(samples, names, output_parameters, locator, weather_path, gv):
    """
    This functions calls the simulation of samples in the CEA using multiprocessing

    :param samples: list of lists of samples to simulate
    :param names: names of buildings to simulate
    :param output_parameters: list of output parameters to analyse
    :param locator: path to locator class
    :param weather_path:  path to weather file
    :param gv: global variables class
    :return: List of Dataframes with output of simulation. It relates the results
    of every outputparameter per building simulated.

    """
    pool = mp.Pool()
    gv.log("Using %i CPU's" % mp.cpu_count())
    joblist = [pool.apply_async(screening_cea, [counter, sample,  names, output_parameters, locator, weather_path, gv])
               for sample, counter in zip(samples, range(len(samples)))]
    results = [job.get() for job in joblist]
    # return in order
    results = sorted(results, key=lambda tup: tup[0])
    results = [x[1] for x in results]
    return results

def screening_cea(counter, sample,  var_names, output_parameters, locator, weather_path, gv):
    """

    :param counter: counter keepin gth enumber of samples analyzed. it serves to sort the results from asynchronous
    multiprocessing in order
    :param sample: sample to simulate
    :param var_names: names of variables to analyze
    :param output_parameters: list of output parameters to analyse
    :param locator: path to locator class
    :param weather_path: path to weather file
    :param gv: global variables class
    :return: Dataframes with output of simulation of a building. It relates the results
    of every outputparameter.
    """

    #create a dict with the new input vatiables form the sample and pass in gv
    gv.samples = dict(zip(var_names, sample))
    result = None
    while result is None:  # trick to avoid that arcgis stops calculating the days and tries again.
       try:
           result = demand_main.demand_calculation(locator, weather_path, gv)[output_parameters]
       except Exception, e:
           print e, result
           pass
    gv.log('Sample No. %s finished' %(counter+1))
    return (counter,result)

def run_as_script():
    import cea.globalvar as gv
    import cea.inputlocator as inputlocator
    gv = gv.GlobalVariables()
    scenario_path = gv.scenario_reference
    locator = inputlocator.InputLocator(scenario_path=scenario_path)
    weather_path = locator.get_default_weather()
    output_parameters = ['QHf_MWhyr', 'QCf_MWhyr', 'Ef_MWhyr',]
    method = 'sobol'
    groups_var =  ['THERMAL']
    num_samples = 100 #generally 1000 or until it converges
    sensitivity_main(locator, weather_path, gv, output_parameters, groups_var, num_samples, method)

if __name__ == '__main__':
    run_as_script()