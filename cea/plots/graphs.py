# -*- coding: utf-8 -*-
"""
===========================
graphs algorithm
===========================
J. Fonseca  script development          18.09.15
D. Thomas   formatting and cleaning
D. Thomas   integration in toolbox

"""
from __future__ import division

import matplotlib.pyplot as plt
import pandas as pd

import cea.inputlocator

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Daren Thomas"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"

def graphs_demand(locator, analysis_fields, gv):
    """
    algorithm to print graphs in PDF concerning the dynamics of each and all buildings

    Parameters
    ----------

    :param locator: an InputLocator set to the scenario to compute
    :type locator: inputlocator.InputLocator

    :param analysis_fields: list of fields (column names in Totals.csv) to analyse
    :type analysis_fields: list[string]

    Returns
    -------
    Graphs of each building and total: .Pdf
        heat map file per variable of interest n.
    """

    # get name of files to map
    building_names = pd.read_csv(locator.get_total_demand()).Name
    num_buildings = len(building_names)
    # setup-time
    color_palette = ['g', 'r', 'y', 'c']
    fields2 = [ x.split('_')[0]+"_MWhyr" for x in analysis_fields]
    fields_date = analysis_fields.append('DATE')

    # get dataframes for totals
    total_file =  pd.read_csv(locator.get_total_demand()).set_index('Name')
    area_df = total_file['GFA_m2']
    total_demand = total_file[fields2]

    # create figure for every name
    counter = 0
    from matplotlib.backends.backend_pdf import PdfPages
    for name in building_names[:2]:
        # CREATE PDF FILE
        pdf = PdfPages(locator.get_demand_plots_file(name))

        # CREATE FIRST PAGE WITH TIMESERIES
        df = pd.read_csv(locator.get_demand_results_file(name), usecols=fields_date)
        df.index = pd.to_datetime(df.DATE)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, figsize=(12,16))
        fig.text(0.07, 0.5, 'Demand [kW]', va='center', rotation='vertical')

        df.plot(ax=ax1, y=analysis_fields, title='YEAR', color=color_palette, label=' ', legend=False)
        df[408:576].plot(ax=ax2, y=analysis_fields, title='WINTER', legend=False, color=color_palette)
        df[4102:4270].plot(ax=ax3, y=analysis_fields, title='SUMMER', legend=False, color=color_palette)
        df[3096:3264].plot(ax=ax4, y=analysis_fields, title='SPRING AND FALL', legend=False, color=color_palette)

        ax4.legend(bbox_to_anchor=(0, -0.4, 1, 0.102), loc=0, ncol=4, mode="expand", borderaxespad=0, fontsize=15)
        ax1.set_xlabel('')
        ax2.set_xlabel('')
        ax3.set_xlabel('')
        ax4.set_xlabel('')
        fig.subplots_adjust(hspace=0.5)
        pdf.savefig()
        plt.close()

        # CREATE SECOND PAGE WITH PLOTS OF TOTAL VALUES
        fig = plt.figure(figsize=(12, 6))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        dftogether = pd.DataFrame({'TOTAL': total_demand.ix[name]}).T
        dftogether.plot(ax=ax1, kind='bar', title='TOTAL YEARLY CONSUMPTION', legend=False, stacked=True, color=color_palette)
        ax1.set_ylabel('Yearly Consumption  [MWh/yr]')

        dftogether2 = pd.DataFrame({'EUI': (total_demand.ix[name] / area_df.ix[name] * 1000)}).T
        dftogether2.plot(ax=ax2, kind='bar', legend=False, title='ENERGY USE INTENSITY', stacked=True, color=color_palette)
        ax2.set_ylabel('Energy Use Intensity EUI [kWh/m2.yr]')

        pdf.savefig()
        plt.close()
        plt.clf()
        pdf.close()


        gv.log('Building No. %(bno)i completed out of %(btot)i', bno=counter+1, btot=num_buildings)
        counter += 1


def test_graph_demand(scenario_path=None):
    # HINTS FOR ARCGIS INTERFACE:
    # the user should see all the column names of the total_demands.csv
    # the user can select a maximum of 4 of those column names to graph (analysis fields!
    from cea import globalvar
    gv = globalvar.GlobalVariables()
    analysis_fields = ["Ealf_kWh", "Qhsf_kWh", "Qwwf_kWh", "Qcsf_kWh"]

    if scenario_path is None:
        scenario_path = gv.scenario_reference
    locator = cea.inputlocator.InputLocator(scenario_path=scenario_path)


    graphs_demand(locator=locator, analysis_fields=analysis_fields, gv=gv)
    print 'test_graph_demand() succeeded'

if __name__ == '__main__':
    test_graph_demand()

