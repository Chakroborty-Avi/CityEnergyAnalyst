"""
This is the dashboard of CEA
"""
from __future__ import division
from __future__ import print_function

import os
import cea.config
import cea.inputlocator
from cea.plots.solar_potential.solar_radiation_curve import solar_radiation_curve
from cea.utilities import epwreader
import pandas as pd
import numpy as np

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

def aggregate(analysis_fields, building, locator):
    df = {}
    geometry = pd.read_csv(locator.get_radiation_metadata(building))
    geometry['code'] = geometry['TYPE'] + '_' + geometry['orientation']
    insolation = pd.read_json(locator.get_radiation_building(building))
    for field in analysis_fields:
        select_sensors = geometry.loc[geometry['code']== field].set_index('SURFACE')
        df[field] = np.array([select_sensors.ix[surface, 'AREA_m2'] * insolation[surface] for surface in select_sensors.index]).sum(axis=0)# W
    return (pd.DataFrame(df)/1000).round(2) # in kW

def dashboard(locator, config):

    # Local Variables
    # GET LOCAL VARIABLES
    building = "B05"

    #CREATE INSOLATION CURVE PER MAIN SURFACE
    output_path = locator.get_timeseries_plots_file(building + '_solar_radiation_curve')
    title = "Solar Radiation Curve for Building " + building
    analysis_fields = ['windows_east', 'windows_west', 'windows_south', 'windows_north',
                       'walls_east','walls_west','walls_south','walls_north','roofs_top', "T_out_dry_C"]
    data = aggregate(analysis_fields, building, locator)
    weather_data = epwreader.epw_reader(config.weather)[["date", "drybulb_C", "wetbulb_C", "skytemp_C"]]
    data["T_out_dry_C"] = weather_data["drybulb_C"].values
    data["DATE"] = weather_data["date"]
    solar_radiation_curve(data, analysis_fields, title, output_path)


def main(config):
    assert os.path.exists(config.scenario), 'Scenario not found: %s' % config.scenario
    locator = cea.inputlocator.InputLocator(config.scenario)

    # print out all configuration variables used by this script
    print("Running dashboard with scenario = %s" % config.scenario)

    dashboard(locator, config)

if __name__ == '__main__':
    main(cea.config.Configuration())
