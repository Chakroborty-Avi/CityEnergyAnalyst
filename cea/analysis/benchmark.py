# -*- coding: utf-8 -*-
"""
===========================
Benchmark plots
===========================

M. Mosteiro Romero  script development          31.08.16

"""
from __future__ import division

import os

import matplotlib.pyplot as plt
import pandas as pd
from geopandas import GeoDataFrame as gpdf

from cea import inputlocator

__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def benchmark(locator_list, output_file):
    """
    Algorithm to print graphs in PDF concerning the 2000 Watt society benchmark for different scenarios.

    Parameters
    ----------
    :param locator: a list of InputLocator instances set to each scenario to be computed. The first element in
    the array is always considered as the baseline for the comparison.
    :type locator: list
    :param output_file: the filename (pdf) to save the results as.
    :type output_file: str

    Side effects
    -------
    The following file is created by this script:
    - ouput_file: .pdf
        Plot of the embodied and operational emissions and primary energy demand
    """

    # setup: the labels and colors for the graphs are defined
    color_palette = ['g', 'r', 'y', 'c', 'b', 'm', 'k']
    legend = []
    graphs = ['embodied', 'operation', 'mobility', 'total']
    old_fields = ['nre_pen_GJ', 'ghg_ton', 'nre_pen_MJm2', 'ghg_kgm2']
    old_prefix = ['E_', 'O_', 'M_']
    fields = ['_GJ', '_ton', '_MJm2', '_kgm2']
    new_cols = {}
    # prepare a dictionary to contain the results for the maximum primary energy demand and emissions in the comparison
    # these are later used to set the scale of the axes of the plots
    scenario_max = {}
    for i in range(4):
        for j in range(3):
            new_cols[old_prefix[j] + old_fields[i]] = graphs[j] + fields[i]
        scenario_max[graphs[i] + fields[2]] = scenario_max[graphs[i] + fields[3]] = 0

    # calculate target values based on the baseline case
    targets = calc_benchmark_targets(locator_list[0])
    # calculate current values based on the baseline case
    values_today = calc_benchmark_today(locator_list[0])

    # start graphs
    fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, figsize=(16, 12))
    fig.text(0.07, 0.5, 'Greenhouse Gas Emissions [kg CO$_2$-eq/m$^2$-yr]', va='center', rotation='vertical')
    fig.text(0.375, 0.04, 'Non-Renewable Primary Energy Demand [MJ/m$^2$-yr]', ha='center')
    ax3.axis('off')
    ax6.axis('off')
    axes = [1, 2, 4, 5]

    # run for each locator (i.e., for each scenario)
    for n in range(len(locator_list)):
        locator = locator_list[n]
        scenario_name = os.path.basename(locator.scenario_path)

        # get embodied and operation PEN and GHG for each building from CSV files
        demand = pd.read_csv(locator.get_total_demand())
        df_buildings = pd.read_csv(locator.get_lca_embodied()).merge\
            (pd.read_csv(locator.get_lca_operation()),on = 'Name').merge\
            (pd.read_csv(locator.get_lca_mobility()),on = 'Name')
        df_buildings = df_buildings.rename(columns=new_cols)

        for i in range(4):
            col_list = [graphs[0] + fields[i], graphs[1] + fields[i], graphs[2] + fields[i]]
            df_buildings[graphs[3] + fields[i]] = df_buildings[col_list].sum(axis=1)

        # calculate total results for entire scenario
        df_scenario = df_buildings.drop('Name',axis=1).sum(axis=0)
        for graph in graphs:
            for j in range(2):
                df_scenario[graph + fields[j+2]] = df_scenario[graph + fields[j]] / df_scenario['GFA_m2'] * 1000
                if scenario_max[graph + fields[j+2]] < df_scenario[graph + fields[j+2]]:
                    scenario_max[graph + fields[j+2]] = df_scenario[graph + fields[j+2]]

        # plot scenario results
        for i in range(len(graphs)):
            plt.subplot(2, 3, axes[i])
            plt.plot(df_buildings[graphs[i]+fields[2]], df_buildings[graphs[i]+fields[3]],'o', color = color_palette[n])
            plt.plot(df_scenario[graphs[i]+fields[2]], df_scenario[graphs[i]+fields[3]], 'o', color = color_palette[n],
                     markersize = 15)
        legend.extend([scenario_name, scenario_name+' total'])

    # complete graphs
    plt.plot()
    for i in range(len(graphs)):
        # plot today and target values
        plt.subplot(2, 3, axes[i])
        plt.plot([0,targets[graphs[i] + fields[2]],targets[graphs[i] + fields[2]]],
                 [targets[graphs[i] + fields[3]],targets[graphs[i] + fields[3]],0], color='k')
        plt.plot([0, values_today[graphs[i] + fields[2]], values_today[graphs[i] + fields[2]]],
                 [values_today[graphs[i] + fields[3]], values_today[graphs[i] + fields[3]], 0], '--', color='k')
        # set axis limits
        if values_today[graphs[i] + fields[2]] > df_scenario[graphs[i] + fields[2]]:
            plt.axis([0, values_today[graphs[i] + fields[2]] * 1.2, 0, values_today[graphs[i] + fields[3]] * 1.2])
        else:
            plt.axis([0, scenario_max[graphs[i] + fields[2]] * 1.2, 0, values_today[graphs[i] + fields[3]] *
                      scenario_max[graphs[i] + fields[2]] / values_today[graphs[i] + fields[2]] * 1.2 ])
        # plot title
        plt.title(graphs[i])

    legend.extend(['Benchmark targets','Present day values'])
    legend_y = 1.2 + 0.05 * (len(locator_list) - 2)
    plt.legend(legend, bbox_to_anchor=(1.3, legend_y , 0.8, 0.102), loc=0, ncol=1 , mode="expand", borderaxespad=0,numpoints=1)

    # save to disk
    plt.savefig(output_file)
    plt.clf()
    plt.close()

def calc_benchmark_targets(locator):
    '''
    This function calculates the embodied, operation, mobility and total targets (ghg_kgm2 and pen_MJm2) for all
    buildings in a scenario.

    The target values for the Swiss case for each type of occupancy are based on the following sources:
        -   Swiss Society of Engineers and Architects (SIA), "SIA Efficiency Path 2040" (2011):
            'MULTI_RES', 'SINGLE_RES', 'SCHOOL', 'OFFICE'
        -   Kellenberger, D. et al. "Arealentwicklung fur die 2000-Watt gesellschaft: Leitfaden und Fallbeispiele" (2012):
            'HOTEL', 'RETAIL', 'FOODSTORE', 'RESTAURANT'
        -   Calculated based on "SIA Effizienzpfad: Bestimmung der Ziel- und Richtwerte mit dem Top-Down Approach" (2010):
            'HOSPITAL', 'INDUSTRY'
    Due to lack of sources, the following target values are, as of yet, undefined:
        'GYM', 'SWIMMING', 'SERVERROOM', 'COOLROOM'

    Parameters
    ----------
    :param locator: an InputLocator instance set to the scenario to compute
    :type locator: InputLocator

    Return
    ------
    :returns target: dict containing pen_MJm2 and ghg_kgm2 target values
    :rtype target: dict
    '''

    # local files
    demand = pd.read_csv(locator.get_total_demand())
    prop_occupancy = gpdf.from_file(locator.get_building_occupancy()).drop('geometry', axis=1)
    data_benchmark = locator.get_data_benchmark()
    occupancy = prop_occupancy.merge(demand,on='Name')

    categories = ['embodied', 'operation', 'mobility', 'total']
    suffix = ['_GJ', '_ton','_MJm2', '_kgm2']
    targets = {}
    area_study = 0

    factors = pd.read_excel(data_benchmark, sheetname=categories[0])
    for i in range(len(factors['code'])):
        if factors['code'][i] in occupancy:
            if factors['PEN'][i] > 0 and factors['CO2'][i] > 0:
                area_study += (occupancy['GFA_m2'] * occupancy[factors['code'][i]]).sum()

    for category in categories:
        factors = pd.read_excel(data_benchmark, sheetname = category)
        vt = factors['code']
        pt = factors['PEN']
        gt = factors['CO2']

        for j in range(len(suffix)):
            targets[category + suffix[j]] = 0
        for i in range(len(vt)):
            targets[category+suffix[0]] += (occupancy['GFA_m2'] * occupancy[vt[i]] * pt[i]).sum() / 1000
            targets[category+suffix[1]] += (occupancy['GFA_m2'] * occupancy[vt[i]] * gt[i]).sum() / 1000
        targets[category + suffix[2]] += targets[category+suffix[0]] / area_study * 1000
        targets[category + suffix[3]] += targets[category + suffix[1]] / area_study * 1000

    return targets

def calc_benchmark_today(locator):
    '''
    This function calculates the embodied, operation, mobility and total targets (ghg_kgm2 and pen_MJm2)
    for the area for the current national trend.

    The current values for the Swiss case for each type of occupancy are based on the following sources:
        -   Swiss Society of Engineers and Architects (SIA), "SIA Efficiency Path 2040" (2011):
            'MULTI_RES', 'SINGLE_RES', 'SCHOOL', 'OFFICE'
        -   Kellenberger, D. et al. "Arealentwicklung fur die 2000-Watt gesellschaft: Leitfaden und Fallbeispiele" (2012):
            'HOTEL', 'RETAIL', 'FOODSTORE', 'RESTAURANT'
        -   Calculated based on "SIA Effizienzpfad: Bestimmung der Ziel- und Richtwerte mit dem Top-Down Approach" (2010):
            'HOSPITAL', 'INDUSTRY'
    Due to lack of sources, the following target values are, as of yet, undefined:
        'GYM', 'SWIMMING', 'SERVERROOM', 'COOLROOM'

    Parameters
    ----------
    :param locator: an InputLocator instance set to the scenario to compute
    :type locator: InputLocator

    Return
    ------
    :returns target: dict containing pen_MJm2 and ghg_kgm2 target values
    :rtype target: dict
    '''

    # local files
    demand = pd.read_csv(locator.get_total_demand())
    prop_occupancy = gpdf.from_file(locator.get_building_occupancy()).drop('geometry', axis=1)
    data_benchmark_today = locator.get_data_benchmark_today()
    occupancy = prop_occupancy.merge(demand, on='Name')

    fields = ['Name', 'pen_GJ', 'ghg_ton', 'pen_MJm2', 'ghg_kgm2']
    categories = ['embodied', 'operation', 'mobility', 'total']
    suffix = ['_GJ', '_ton', '_MJm2', '_kgm2']
    values_today = {}
    area_study = 0

    factors = pd.read_excel(data_benchmark_today, sheetname=categories[0])
    for i in range(len(factors['code'])):
        if factors['code'][i] in occupancy:
            if factors['PEN'][i] > 0 and factors['CO2'][i] > 0:
                area_study += (occupancy['GFA_m2'] * occupancy[factors['code'][i]]).sum()

    for category in categories:
        factors = pd.read_excel(data_benchmark_today, sheetname=category)
        vt = factors['code']
        pt = factors['PEN']
        gt = factors['CO2']

        for j in range(len(suffix)):
            values_today[category + suffix[j]] = 0
        for i in range(len(vt)):
            values_today[category + suffix[0]] += (occupancy['GFA_m2'] * occupancy[vt[i]] * pt[i]).sum() / 1000
            values_today[category + suffix[1]] += (occupancy['GFA_m2'] * occupancy[vt[i]] * gt[i]).sum() / 1000
        values_today[category + suffix[2]] += values_today[category + suffix[0]] / area_study * 1000
        values_today[category + suffix[3]] += values_today[category + suffix[1]] / area_study * 1000

    return values_today

def test_benchmark():
    locator = inputlocator.InputLocator(scenario_path=r'C:\reference-case-zug\baseline')
    locator_list = [locator, locator, locator, locator]
    output_file = os.path.expandvars(r'%TEMP%\test_benchmark.pdf')
    benchmark(locator_list=locator_list, output_file=output_file)
    print 'test_benchmark() succeeded'

def test_benchmark_targets():
    locator = inputlocator.InputLocator(scenario_path=r'C:\reference-case-zug\baseline')
    calc_benchmark_targets(locator)

if __name__ == '__main__':
    test_benchmark()

