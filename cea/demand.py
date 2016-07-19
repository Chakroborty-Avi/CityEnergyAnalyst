"""
===========================
Analytical energy demand model algorithm
===========================

"""
from __future__ import division

import multiprocessing as mp

import pandas as pd

import cea.dem.sensible_loads as f
import cea.globalvar
import cea.inputlocator
import cea.maker as m
from cea.dem import thermal_loads
from cea.dem.thermal_loads import BuildingProperties
from cea.utils import epwreader

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Daren Thomas", "Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"


reload(f)
reload(cea.globalvar)


def demand_calculation(locator, weather_path, gv):
    """
    Algorithm to calculate the hourly dem of energy services in buildings
    using the integrated model of Fonseca et al. 2015. Applied energy.
    (http://dx.doi.org/10.1016/j.apenergy.2014.12.068)

    PARAMETERS
    ----------
    :param locator: An InputLocator to locate input files
    :type locator: inputlocator.InputLocator

    :param weather_path: A path to the EnergyPlus weather data file (.epw)
    :type weather_path: str

    :param gv: A GlobalVariable (context) instance
    :type gv: globalvar.GlobalVariable


    RETURNS
    -------

    :returns: None
    :rtype: NoneType


    INPUT / OUTPUT FILES
    --------------------

    - get_demand_results_folder: C:\reference-case\baseline\outputs\data\dem
    - get_temporary_folder: c:\users\darthoma\appdata\local\temp
    - get_temporary_file: c:\users\darthoma\appdata\local\temp\B153767T.csv (* for each building)
    - get_total_demand: C:\reference-case\baseline\outputs\data\dem\Total_demand.csv


    SIDE EFFECTS
    ------------

    Produces a dem file per building and a total dem file for the whole zone of interest.

    B153767T.csv: csv file for every building with hourly dem data
    Total_demand.csv: csv file of yearly dem data per buidling.
    """

    # starting date
    date = pd.date_range(gv.date_start, periods=8760, freq='H')

    # weather model
    weather_data = epwreader.epw_reader(weather_path)[['drybulb_C', 'relhum_percent', 'windspd_ms']]

    # building properties model
    building_properties = BuildingProperties(locator, gv)

    # schedules model
    list_uses = list(building_properties._prop_occupancy.drop('PFloor', axis=1).columns)
    schedules = m.schedule_maker(date, locator, list_uses)
    schedules_dict = {'list_uses': list_uses, 'schedules': schedules}

    # dem model
    num_buildings = len(building_properties)
    if gv.multiprocessing:
        thermal_loads_all_buildings_multiprocessing(building_properties, date, gv, locator, num_buildings,
                                                    schedules_dict,
                                                    weather_data)
    else:
        thermal_loads_all_buildings(building_properties, date, gv, locator, num_buildings, schedules_dict,
                                    weather_data)
    write_totals_csv(building_properties, locator)
    gv.log('done')


def write_totals_csv(building_properties, locator):
    """read in the temporary results files and append them to the Totals.csv file."""
    counter = 0
    for name in building_properties.list_building_names():
        temporary_file = locator.get_temporary_file('%(name)sT.csv' % locals())
        if counter == 0:
            df = pd.read_csv(temporary_file)
            counter += 1
        else:
            df2 = pd.read_csv(temporary_file)
            df = df.append(df2, ignore_index=True)
    df.to_csv(locator.get_total_demand(), index=False, float_format='%.2f')


def thermal_loads_all_buildings(building_properties, date, gv, locator, num_buildings, usage_schedules,
                                weather_data):
    for i, building in enumerate(building_properties.list_building_names()):
        bpr = building_properties[building]
        thermal_loads.calc_thermal_loads(
            building, bpr, weather_data, usage_schedules, date, gv,
            locator.get_demand_results_folder(),
            locator.get_temporary_folder())
        gv.log('Building No. %(bno)i completed out of %(num_buildings)i', bno=i + 1, num_buildings=num_buildings)


def thermal_loads_all_buildings_multiprocessing(building_properties, date, gv, locator, num_buildings, usage_schedules,
                                                weather_data):
    pool = mp.Pool()
    gv.log("Using %i CPU's" % mp.cpu_count())
    joblist = []
    for building in building_properties.list_building_names():
        bpr = building_properties[building]
        job = pool.apply_async(thermal_loads.calc_thermal_loads,
                               [building, bpr, weather_data, usage_schedules, date, gv,
                                locator.get_demand_results_folder(),
                                locator.get_temporary_folder()])
        joblist.append(job)
    for i, job in enumerate(joblist):
        job.get(60)
        gv.log('Building No. %(bno)i completed out of %(num_buildings)i', bno=i + 1, num_buildings=num_buildings)


def run_as_script(scenario_path=None, weather_path=None):
        if scenario_path is None:
            scenario_path = r'c:\reference-case\baseline'
        locator = cea.inputlocator.InputLocator(scenario_path=scenario_path)
        # for the interface, the user should pick a file out of of those in ...DB/Weather/...
        if weather_path is None:
            weather_path = locator.get_default_weather()
        gv = cea.globalvar.GlobalVariables()
        gv.log('Running dem calculation for scenario %(scenario)s', scenario=scenario_path)
        gv.log('Running dem calculation with weather file %(weather)s', weather=weather_path)
        demand_calculation(locator=locator, weather_path=weather_path, gv=gv)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scenario', help='Path to the scenario folder')
    parser.add_argument('-w', '--weather', help='Path to the weather file')
    args = parser.parse_args()
    run_as_script(scenario_path=args.scenario, weather_path=args.weather)

