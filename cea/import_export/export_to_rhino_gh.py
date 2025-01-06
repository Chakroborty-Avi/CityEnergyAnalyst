"""
Export CEA files into Rhino/Grasshopper-ready format.

"""

import cea.inputlocator
import os
import cea.config
import time
import geopandas as gpd


__author__ = "Zhongming Shi"
__copyright__ = "Copyright 2024, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Zhongming Shi"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Reynold Mok"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

from cea.utilities.dbf import dbf_to_csv_xlsx
from cea.utilities.shapefile import shapefile_to_csv_xlsx
from cea.utilities.standardize_coordinates import get_lat_lon_projected_shapefile, get_projected_coordinate_system

def exec_export_csv_for_rhino(config, locator):
    """

    :param config: the configuration object to use
    :type config: cea.config.Configuration
    :param cea_scenario: path to the CEA scenario to be assessed using CEA
    :type cea_scenario: file path
    :return:
    """

    # Acquire the user inputs from config
    bool_include_zone = config.to_rhino_gh.include_zone
    bool_include_site = config.to_rhino_gh.include_site
    bool_include_surroundings = config.to_rhino_gh.include_surroundings
    bool_include_streets = config.to_rhino_gh.include_streets
    bool_include_trees = config.to_rhino_gh.include_trees

    # Create the folder to store all the exported files if it doesn't exist
    output_path = locator.get_export_rhino_from_cea_folder()
    os.makedirs(output_path, exist_ok=True)

    # Remove all files in folder
    for filename in os.listdir(output_path):
        file_path = os.path.join(output_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    gdf = gpd.read_file(locator.get_zone_geometry())
    lat, lon = get_lat_lon_projected_shapefile(gdf)  # Ensure this function is implemented
    new_crs = get_projected_coordinate_system(lat=lat, lon=lon)

    # Export zone info including typology
    if bool_include_zone:
        shapefile_to_csv_xlsx(locator.get_zone_geometry(), output_path, 'zone_to.csv', new_crs)

    if bool_include_site and os.path.isfile(locator.get_site_polygon()):
        shapefile_to_csv_xlsx(locator.get_site_polygon(), output_path, 'site_to.csv', new_crs)

    if bool_include_surroundings and os.path.isfile(locator.get_surroundings_geometry()):
        shapefile_to_csv_xlsx(locator.get_surroundings_geometry(), output_path, 'surroundings_to.csv', new_crs)

    if bool_include_streets and os.path.isfile(locator.get_street_network()):
        shapefile_to_csv_xlsx(locator.get_street_network(), output_path, 'streets_to.csv', new_crs)

    if bool_include_trees and os.path.isfile(locator.get_tree_geometry()):
        shapefile_to_csv_xlsx(locator.get_tree_geometry(), output_path, 'trees_to.csv', new_crs)


def main(config):

    # Start the timer
    t0 = time.perf_counter()

    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    assert os.path.exists(config.general.project), 'input file not found: %s' % config.project

    exec_export_csv_for_rhino(config, locator)

    # Print the time used for the entire processing
    time_elapsed = time.perf_counter() - t0
    print('The entire export to the current CEA Scenario to Rhino/Grasshopper-ready files is now completed - time elapsed: %d.2 seconds' % time_elapsed)


if __name__ == '__main__':
    main(cea.config.Configuration())
