# -*- coding: utf-8 -*-
"""
===========================
Benchmark graphs algorithm
===========================

"""
from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd
from cea import inputlocator
from geopandas import GeoDataFrame as gpdf
import numpy as np
import os
import tempfile

from cea import globalvar

gv = globalvar.GlobalVariables()

def benchmark(locator_list):
    """
    algorithm to print graphs in PDF concerning the 2000 Watt society benchmark 
    for two scenarios (A and B)

    Parameters
    ----------

    :param locator: an array of InputLocator set to each first scenario to be computed
    :type locator: inputlocator.InputLocator
    :param output_file: the filename (pdf) to save the results as.

    Returns
    -------
    Graphs of the embodied and operational emissions and primary energy demand: .Pdf
    """

    # setup-time
    color_palette = ['g', 'r', 'y', 'c', 'b', 'm', 'k']
    legend = []
    graphs = ['embodied', 'operation', 'mobility', 'total']
    old_fields = ['pen_GJ', 'ghg_ton', 'pen_MJm2', 'ghg_kgm2']
    old_suffix = ['_x', '_y', '']
    fields = ['_GJ', '_ton', '_MJm2', '_kgm2']
    new_cols = {}
    scenario_max = {}
    for i in range(4):
        for j in range(3):
            new_cols[old_fields[i] + old_suffix[j]] = graphs[j] + fields[i]
        scenario_max[graphs[i] + fields[2]] = scenario_max[graphs[i] + fields[3]] = 0

    # calculate target values - THIS IS ASSUMING THE FIRST SCENARIO IS ALWAYS THE BASELINE! Need to confirm.
    targets = calc_benchmark_targets(locator_list[0])
    # calculate current values - THIS SHOULD NOT BE HARD CODED AND NEED A SOURCE (other than Inducity)
    values_today = calc_benchmark_today(locator_list[0])

    # start graphs
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, figsize=(16, 12))
    fig.text(0.07, 0.5, 'Greenhouse Gas Emissions [kg CO$_2$-eq/m$^2$-yr]', va='center', rotation='vertical')
    fig.text(0.5, 0.07, 'Primary Energy Demand [MJ/m$^2$-yr]', ha='center')  # , rotation='vertical')

    # run for each locator
    for n in range(len(locator_list)):
        locator = locator_list[n]
        scenario_name = os.path.basename(locator.scenario_path)

        # get embodied and operation PEN and GHG for each building from CSV files
        demand = pd.read_csv(locator.get_total_demand())
        df_buildings = pd.read_csv(locator.get_lca_embodied()).merge\
            (pd.read_csv(locator.get_lca_operation()),on = 'Name').merge\
            (pd.read_csv(locator.get_lca_mobility()),on = 'Name')
        df_buildings = df_buildings.rename(columns=new_cols)
        df_buildings = df_buildings.merge(demand[['Name','Af_m2']],on = 'Name')

        for i in range(4):
            col_list = [graphs[0] + fields[i], graphs[1] + fields[i], graphs[2] + fields[i]]
            df_buildings[graphs[3] + fields[i]] = df_buildings[col_list].sum(axis=1)

        # calculate total results for entire scenario
        df_scenario = df_buildings.drop('Name',axis=1).sum(axis=0)
        for graph in graphs:
            for j in range(2):
                df_scenario[graph + fields[j+2]] = df_scenario[graph + fields[j]] / df_scenario['Af_m2'] * 1000
                if scenario_max[graph + fields[j+2]] < df_scenario[graph + fields[j+2]]:
                    scenario_max[graph + fields[j+2]] = df_scenario[graph + fields[j+2]]


        for i in range(len(graphs)):
            plt.subplot(2,2,i+1)
            plt.plot(df_buildings[graphs[i]+fields[2]], df_buildings[graphs[i]+fields[3]],'o', color = color_palette[n])
            plt.plot(df_scenario[graphs[i]+fields[2]], df_scenario[graphs[i]+fields[3]], 'o', color = color_palette[n],
                     markersize = 15)
        legend.extend([scenario_name, scenario_name+' total'])
    # complete graphs
    plt.plot()
    for i in range(len(graphs)):
        # plot today and target values
        plt.subplot(2, 2, i + 1)
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
    plt.legend(legend, bbox_to_anchor=(-1.1, -0.2, 2, 0.102), loc=0, ncol=3 , mode="expand", borderaxespad=0,numpoints=1)
    '''
        , bbox_to_anchor=(-1.1, -0.2, 2, 0.102), loc=0, ncol=4, mode="expand", borderaxespad=0,
               fontsize=15, numpoints=1)
    '''
    # save to disk
    plt.savefig(locator_list[0].get_benchmark_plots_file())
    plt.clf()
    plt.close()

def calc_benchmark_targets(locator):
    '''
    Calculates the embodied, operation, mobility and total targets (ghg_kgm2
    and pen_MJm2) for all buildings in a scenario.
    :param locator: an InputLocator set to the scenario to compute
    :array target: pen_MJm2 and ghg_kgm2 target values
    '''

    # local files
    demand = pd.read_csv(locator.get_total_demand())
    prop_occupancy = gpdf.from_file(locator.get_building_occupancy()).drop('geometry', axis=1)
    data_benchmark = locator.get_data_benchmark()
    occupancy = prop_occupancy.merge(demand,on='Name')

    fields = ['Name', 'pen_GJ', 'ghg_ton', 'pen_MJm2', 'ghg_kgm2']
    categories = ['embodied', 'operation', 'mobility', 'total']
    suffix = ['_GJ', '_ton','_MJm2', '_kgm2']
    targets = {}
    area_study = 0

    factors = pd.read_excel(data_benchmark, sheetname=categories[0])
    for i in range(len(factors['code'])):
        if factors['code'][i] in occupancy:
            if factors['PEN'][i] > 0 and factors['CO2'][i] > 0:
                area_study += (occupancy['Af_m2'] * occupancy[factors['code'][i]]).sum()

    for category in categories:
        factors = pd.read_excel(data_benchmark, sheetname = category)
        vt = factors['code']
        pt = factors['PEN']
        gt = factors['CO2']

        for j in range(len(suffix)):
            targets[category + suffix[j]] = 0
        for i in range(len(vt)):
            targets[category+suffix[0]] += (occupancy['Af_m2'] * occupancy[vt[i]] * pt[i]).sum() / 1000
            targets[category+suffix[1]] += (occupancy['Af_m2'] * occupancy[vt[i]] * gt[i]).sum() / 1000
        targets[category + suffix[2]] += targets[category+suffix[0]] / area_study * 1000
        targets[category + suffix[3]] += targets[category + suffix[1]] / area_study * 1000

    return targets

def calc_benchmark_today(locator):
    '''
    Calculates the embodied, operation, mobility and total targets (ghg_kgm2
    and pen_MJm2) for the area for the current national trend.
    CURRENTLY BASED ON INDUCITY! Need a better source.
    :param locator: an InputLocator set to the scenario to compute
    :array values_today: pen_MJm2 and ghg_kgm2 for the scenario based on benchmarked present day situation
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
                area_study += (occupancy['Af_m2'] * occupancy[factors['code'][i]]).sum()

    for category in categories:
        factors = pd.read_excel(data_benchmark_today, sheetname=category)
        vt = factors['code']
        pt = factors['PEN']
        gt = factors['CO2']

        for j in range(len(suffix)):
            values_today[category + suffix[j]] = 0
        for i in range(len(vt)):
            values_today[category + suffix[0]] += (occupancy['Af_m2'] * occupancy[vt[i]] * pt[i]).sum() / 1000
            values_today[category + suffix[1]] += (occupancy['Af_m2'] * occupancy[vt[i]] * gt[i]).sum() / 1000
        values_today[category + suffix[2]] += values_today[category + suffix[0]] / area_study * 1000
        values_today[category + suffix[3]] += values_today[category + suffix[1]] / area_study * 1000

    return values_today

def test_benchmark():
    # HINTS FOR ARCGIS INTERFACE:
    # the user can select a maximum of 2 scenarios to graph (analysis fields!)
    locator1 = inputlocator.InputLocator(scenario_path=r'C:\reference-case\baseline')
    locator2 = inputlocator.InputLocator(scenario_path=r'C:\reference-case\baseline')
    locator_list = [locator1, locator2]
    benchmark(locator_list = locator_list)

def test_benchmark_targets():
    locator = inputlocator.InputLocator(scenario_path=r'C:\reference-case\baseline')
    from cea import globalvar
    gv = globalvar.GlobalVariables()
    calc_benchmark_targets(locator)

if __name__ == '__main__':
    test_benchmark()
    test_benchmark_targets()
