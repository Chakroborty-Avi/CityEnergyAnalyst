"""
Verify the format of DB for CEA-4 model.

"""


import os
import cea.config
import time
import pandas as pd
import numpy as np
from cea.schemas import schemas
import sys


__author__ = "Zhongming Shi"
__copyright__ = "Copyright 2025, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Zhongming Shi"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Reynold Mok"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

from cea.datamanagement.format_helper.cea4_verify import verify_file_against_schema_4

ARCHETYPES = ['CONSTRUCTION_TYPE', 'USE_TYPE']
SCHEDULES_FOLDER = ['SCHEDULES']
ENVELOPE_ASSEMBLIES = ['MASS', 'TIGHTNESS', 'FLOOR', 'WALL', 'WINDOW', 'SHADING', 'ROOF']
HVAC_ASSEMBLIES = ['HVAC_CONTROLLER', 'HVAC_HOT_WATER', 'HVAC_HEATING', 'HVAC_COOLING', 'HVAC_VENTILATION']
SUPPLY_ASSEMBLIES = ['SUPPLY_COOLING', 'SUPPLY_ELECTRICITY', 'SUPPLY_HEATING', 'SUPPLY_HOT_WATER']
CONVERSION_COMPONENTS = ['ABSORPTION_CHILLERS', 'BOILERS', 'BORE_HOLES', 'COGENERATION_PLANTS', 'COOLING_TOWERS',
                         'FUEL_CELLS', 'HEAT_EXCHANGERS', 'HEAT_PUMPS', 'HYDRAULIC_PUMPS', 'PHOTOVOLTAIC_PANELS',
                         'PHOTOVOLTAIC_THERMAL_PANELS', 'POWER_TRANSFORMERS', 'SOLAR_THERMAL_PANELS',
                         'THERMAL_ENERGY_STORAGES', 'UNITARY_AIR_CONDITIONERS', 'VAPOR_COMPRESSION_CHILLERS'
                         ]
DISTRIBUTION_COMPONENTS = ['THERMAL_GRID']
FEEDSTOCKS_COMPONENTS = ['BIOGAS', 'COAL', 'DRYBIOMASS', 'ENERGY_CARRIERS', 'GRID', 'HYDROGEN', 'NATURALGAS', 'OIL', 'SOLAR', 'WETBIOMASS', 'WOOD']
dict_assembly = {'MASS': 'envelope_type_mass', 'TIGHTNESS': 'envelope_type_leak', 'FLOOR': 'envelope_type_floor',
                 'WALL': 'envelope_type_wall', 'WINDOW': 'envelope_type_win', 'SHADING': 'envelope_type_shade',
                 'ROOF': 'envelope_type_roof', 'HVAC_CONTROLLER': 'hvac_type_ctrl', 'HVAC_HOT_WATER': 'hvac_type_dhw',
                 'HVAC_HEATING': 'hvac_type_hs', 'HVAC_COOLING': 'hvac_type_cs', 'HVAC_VENTILATION': 'hvac_type_vent',
                 'SUPPLY_COOLING': 'supply_type_cs', 'SUPPLY_ELECTRICITY': 'supply_type_el', 'SUPPLY_HEATING': 'supply_type_hs',
                 'SUPPLY_HOT_WATER': 'supply_type_dhw',
                 }
ASSEMBLIES_FOLDERS = ['ENVELOPE', 'HVAC', 'SUPPLY']
COMPONENTS_FOLDERS = ['CONVERSION', 'DISTRIBUTION', 'FEEDSTOCKS']
dict_ASSEMBLIES = {'ENVELOPE': ENVELOPE_ASSEMBLIES, 'HVAC': HVAC_ASSEMBLIES, 'SUPPLY': SUPPLY_ASSEMBLIES}
mapping_dict_db_item_to_schema_locator = {'CONSTRUCTION_TYPE': 'get_database_archetypes_construction_type',
                                          'USE_TYPE': 'get_database_archetypes_use_type',
                                          'SCHEDULES': 'get_database_archetypes_schedules',
                                          'CONSTRUCTION': 'get_database_assemblies_envelope_construction',
                                          'MASS': 'get_database_assemblies_envelope_mass',
                                          'FLOOR': 'get_database_assemblies_envelope_floor',
                                          'WALL': 'get_database_assemblies_envelope_wall',
                                          'WINDOW': 'get_database_assemblies_envelope_window',
                                          'SHADING': 'get_database_assemblies_envelope_shading',
                                          'ROOF': 'get_database_assemblies_envelope_roof',
                                          'TIGHTNESS': 'get_database_assemblies_envelope_tightness',
                                          'HVAC_CONTROLLER': 'get_database_assemblies_hvac_controller',
                                          'HVAC_COOLING': 'get_database_assemblies_hvac_cooling',
                                          'HVAC_HEATING': 'get_database_assemblies_hvac_heating',
                                          'HVAC_HOT_WATER': 'get_database_assemblies_hvac_hot_water',
                                          'HVAC_VENTILATION': 'get_database_assemblies_hvac_ventilation',
                                          'SUPPLY_COOLING': 'get_database_assemblies_supply_cooling',
                                          'SUPPLY_HEATING': 'get_database_assemblies_supply_heating',
                                          'SUPPLY_HOT_WATER': 'get_database_assemblies_supply_hot_water',
                                          'SUPPLY_ELECTRICITY': 'get_database_assemblies_supply_electricity',
                                          'ABSORPTION_CHILLERS': 'get_database_components_conversion_absorption_chillers',
                                          'BOILERS': 'get_database_components_conversion_boilers',
                                          'BORE_HOLES': 'get_database_components_conversion_bore_holes',
                                          'COGENERATION_PLANTS': 'get_database_components_conversion_cogeneration_plants',
                                          'COOLING_TOWERS': 'get_database_components_conversion_cooling_towers',
                                          'FUEL_CELLS': 'get_database_components_conversion_fuel_cells',
                                          'HEAT_EXCHANGERS': 'get_database_components_conversion_heat_exchangers',
                                          'HEAT_PUMPS': 'get_database_components_conversion_heat_pumps',
                                          'HYDRAULIC_PUMPS': 'get_database_components_conversion_hydraulic_pumps',
                                          'PHOTOVOLTAIC_PANELS': 'get_database_components_conversion_photovoltaic_panels',
                                          'PHOTOVOLTAIC_THERMAL_PANELS': 'get_database_components_conversion_photovoltaic_thermal_panels',
                                          'POWER_TRANSFORMERS': 'get_database_components_conversion_power_transformers',
                                          'SOLAR_THERMAL_PANELS': 'get_database_components_conversion_solar_thermal_panels',
                                          'THERMAL_ENERGY_STORAGES': 'get_database_components_conversion_thermal_energy_storages',
                                          'UNITARY_AIR_CONDITIONERS': 'get_database_components_conversion_unitary_air_conditioners',
                                          'VAPOR_COMPRESSION_CHILLERS': 'get_database_components_conversion_vapor_compression_chillers',
                                          'DISTRIBUTION': 'get_database_components_distribution_thermal_grid',
                                          'BIOGAS': 'get_database_components_feedstocks_biogas',
                                          'COAL': 'get_database_components_feedstocks_coal',
                                          'DRYBIOMASS': 'get_database_components_feedstocks_drybiomass',
                                          'ENERGY_CARRIERS': 'get_database_components_feedstocks_energy_carriers',
                                          'GRID': 'get_database_components_feedstocks_grid',
                                          'HYDROGEN': 'get_database_components_feedstocks_hydrogen',
                                          'NATURALGAS': 'get_database_components_feedstocks_naturalgas',
                                          'OIL': 'get_database_components_feedstocks_oil',
                                          'SOLAR': 'get_database_components_feedstocks_solar',
                                          'WETBIOMASS': 'get_database_components_feedstocks_wetbiomass',
                                          'WOOD': 'get_database_components_feedstocks_wood',
                                          }

mapping_dict_db_item_to_id_column = {'CONSTRUCTION_TYPE': 'const_type',
                                     'USE_TYPE':'code',
                                     'SCHEDULES': 'hour',
                                     'ENVELOPE': 'code',
                                     'HVAC': 'code',
                                     'SUPPLY': 'code',
                                     'CONVERSION': 'code',
                                     'DISTRIBUTION': 'code',
                                     'FEEDSTOCKS': 'hour',
                                     'ENERGY_CARRIERS': 'code',
                                     }


## --------------------------------------------------------------------------------------------------------------------
## The paths to the input files for CEA-4
## --------------------------------------------------------------------------------------------------------------------

# The paths are relatively hardcoded for now without using the inputlocator script.
# This is because we want to iterate over all scenarios, which is currently not possible with the inputlocator script.
def path_to_db_file_4(scenario, item, sheet_name=None):

    if item == 'database':
        path_db_file = os.path.join(scenario, "inputs", "database")
    elif item == "CONSTRUCTION_TYPE":
        path_db_file = os.path.join(scenario, "inputs", "database", "ARCHETYPES", "CONSTRUCTION_TYPE.csv")
    elif item == "USE_TYPE":
        path_db_file = os.path.join(scenario, "inputs",  "database", "ARCHETYPES", "USE_TYPE.csv")
    elif item == "SCHEDULES":
        if sheet_name is None:
            path_db_file = os.path.join(scenario, "inputs", "database", "ARCHETYPES", "SCHEDULES")
        else:
            path_db_file = os.path.join(scenario, "inputs", "database", "ARCHETYPES", "SCHEDULES", "{use_type}.csv".format(use_type=sheet_name))
    elif item == "MONTHLY_MULTIPLIER":
        path_db_file = os.path.join(scenario, "inputs", "database", "ARCHETYPES", "SCHEDULES", "MONTHLY_MULTIPLIER.csv")
    elif item == "ENVELOPE":
        if sheet_name is None:
            path_db_file = os.path.join(scenario, "inputs",  "database", "ASSEMBLIES", "ENVELOPE")
        else:
            path_db_file = os.path.join(scenario, "inputs",  "database", "ASSEMBLIES", "ENVELOPE", "{envelope_assemblies}.csv".format(envelope_assemblies=sheet_name))
    elif item == "HVAC":
        if sheet_name is None:
            path_db_file = os.path.join(scenario, "inputs",  "database", "ASSEMBLIES", "HVAC")
        else:
            path_db_file = os.path.join(scenario, "inputs",  "database", "ASSEMBLIES", "HVAC", "{hvac_assemblies}.csv".format(hvac_assemblies=sheet_name))
    elif item == "SUPPLY":
        if sheet_name is None:
            path_db_file = os.path.join(scenario, "inputs",  "database", "ASSEMBLIES", "SUPPLY")
        else:
            path_db_file = os.path.join(scenario, "inputs",  "database", "ASSEMBLIES", "SUPPLY", "{supply_assemblies}.csv".format(supply_assemblies=sheet_name))
    elif item == "CONVERSION":
        if sheet_name is None:
            path_db_file = os.path.join(scenario, "inputs",  "database", "COMPONENTS", "CONVERSION")
        else:
            path_db_file = os.path.join(scenario, "inputs",  "database", "COMPONENTS", "CONVERSION", "{conversion_components}.csv".format(conversion_components=sheet_name))
    elif item == "DISTRIBUTION":
        path_db_file = os.path.join(scenario, "inputs",  "database", "COMPONENTS", "DISTRIBUTION", "THERMAL_GRID.csv")
    elif item == "FEEDSTOCKS":
        if sheet_name is None:
            path_db_file = os.path.join(scenario, "inputs",  "database", "COMPONENTS", "FEEDSTOCKS")
        else:
            path_db_file = os.path.join(scenario, "inputs",  "database", "COMPONENTS", "FEEDSTOCKS", "{feedstocks_components}.csv".format(feedstocks_components=sheet_name))
    else:
        raise ValueError(f"Unknown item {item}")

    return path_db_file


## --------------------------------------------------------------------------------------------------------------------
## Helper functions
## --------------------------------------------------------------------------------------------------------------------

def verify_file_against_schema_4_db(scenario, item, verbose=True, sheet_name=None):
    """
    Validate a file against a schema section in a YAML file.

    Parameters:
    - scenario (str): Path to the scenario.
    - item (str): Locator for the file to validate (e.g., 'get_zone_geometry').
    - self: Reference to the calling class/module.
    - verbose (bool, optional): If True, print validation errors to the console.

    Returns:
    - List[dict]: List of validation errors.
    """
    schema = schemas()

    # File path and schema section
    file_path = path_to_db_file_4(scenario, item, sheet_name)
    if sheet_name is None:
        locator = mapping_dict_db_item_to_schema_locator[item]
    elif sheet_name is not None and item == 'SCHEDULES':
        locator = mapping_dict_db_item_to_schema_locator[item]
    else:
        locator = mapping_dict_db_item_to_schema_locator[sheet_name]

    schema_section = schema[locator]
    schema_columns = schema_section['schema']['columns']
    if sheet_name == 'ENERGY_CARRIERS':
        id_column = mapping_dict_db_item_to_id_column[sheet_name]
    else:
        id_column = mapping_dict_db_item_to_id_column[item]

    # Determine file type and load the data
    if file_path.endswith('.csv'):
        try:
            df = pd.read_csv(file_path)
            col_attr = 'Column'
        except Exception as e:
            raise ValueError(f"Failed to read .csv file: {file_path}. Error: {e}")
    else:
        raise ValueError(f"Unsupported file type: {file_path}. Only .csv files are supported.")

    if id_column not in df.columns:
        print(f"! CEA was not able to verify {os.path.basename(file_path)} "
              f"as a unique row identifier column such as (building) name or (component) code is not present.")

    errors = []
    missing_columns = []

    # Validation process
    for col_name, col_specs in schema_columns.items():
        if col_name not in df.columns:
            missing_columns.append(col_name)
            continue

        col_data = df[col_name]

        # Check type
        if col_specs['type'] == 'string':
            invalid = ~col_data.apply(lambda x: isinstance(x, str) or pd.isnull(x))
        elif col_specs['type'] == 'int':
            invalid = ~col_data.apply(lambda x: isinstance(x, (int, np.integer)) or pd.isnull(x))
        elif col_specs['type'] == 'float':
            invalid = ~col_data.apply(lambda x: isinstance(x, (float, int, np.floating, np.integer)) or pd.isnull(x))
        else:
            invalid = pd.Series(False, index=col_data.index)  # Unknown types are skipped

        for idx in invalid[invalid].index:
            identifier = df.at[idx, id_column]
            errors.append({col_attr: col_name, "Issue": "Invalid type", "Row": identifier, "Value": col_data[idx]})

        # Check range
        if 'min' in col_specs:
            out_of_range = col_data[col_data < col_specs['min']]
            for idx, value in out_of_range.items():
                identifier = df.at[idx, id_column]
                errors.append({col_attr: col_name, "Issue": f"Below minimum ({col_specs['min']})", "Row": identifier, "Value": value})

        if 'max' in col_specs:
            out_of_range = col_data[col_data > col_specs['max']]
            for idx, value in out_of_range.items():
                identifier = df.at[idx, id_column]
                errors.append({col_attr: col_name, "Issue": f"Above maximum ({col_specs['max']})", "Row": identifier, "Value": value})

    # Relax from the descriptive columns which not used in the modelling
    missing_columns = [item for item in missing_columns if item not in ['geometry', 'reference', 'description', 'assumption']]

    # Print results
    if errors:
        if verbose:
            for error in errors:
                print(error)
    elif verbose:
        print(f"Validation passed: All columns and values meet the CEA (schema) requirements.")

    return missing_columns, errors


def print_verification_results_4_db(scenario_name, dict_missing):

    if all(not value for value in dict_missing.values()):
        print("✓" * 3)
        print('The Database is verified as present and compatible with the current version of CEA-4 for Scenario: {scenario}, including:'.format(scenario=scenario_name),
              )
    else:
        print("!" * 3)
        print('All or some of Database files/columns are missing or incompatible with the current version of CEA-4 for Scenario: {scenario}. '.format(scenario=scenario_name))
        print('- If you are migrating your input data from CEA-3 to CEA-4 format, set the toggle `migrate_from_cea_3` to `True` for Feature CEA-4 Format Helper and click on Run. ')
        print('- If you manually prepared the Database, check the log for missing files and/or incompatible columns. Modify your Database accordingly.')


def verify_file_exists_4_db(scenario, items, sheet_name=None):
    """
    Verify if the files in the provided list exist for a given scenario.

    Parameters:
        scenario (str): Path or identifier for the scenario.
        items (list): List of file identifiers to check.

    Returns:
        list: A list of missing file identifiers, or an empty list if all files exist.
    """
    list_missing_files = []
    for file in items:
        if sheet_name is None:
            path = path_to_db_file_4(scenario, file)
            if not os.path.isfile(path):
                list_missing_files.append(file)
        else:
            for sheet in sheet_name:
                sheet = sheet.replace('HVAC_', '')
                sheet = sheet.replace('SUPPLY_', '')
                path = path_to_db_file_4(scenario, file, sheet)
                if not os.path.isfile(path):
                    list_missing_files.append(sheet)
    return list_missing_files


def verify_assembly(scenario, ASSEMBLIES, list_missing_files_csv, print_results=True):
    list_existing_files_csv = list(set(dict_ASSEMBLIES[ASSEMBLIES]) - set(list_missing_files_csv))
    list_list_missing_columns_csv = []
    construction_type_df = pd.read_csv(path_to_db_file_4(scenario, 'CONSTRUCTION_TYPE'))
    for assembly in list_existing_files_csv:
        path_to_csv = path_to_db_file_4(scenario, ASSEMBLIES, assembly)
        list_archetype_code = construction_type_df[dict_assembly[assembly]].unique().tolist()
        item_df = pd.read_csv(path_to_csv)
        list_item_code = item_df['code'].unique().tolist()
        list_missing_item = list(set(list_archetype_code) - set(list_item_code))
        if list_missing_item:
            if print_results:
                print('! Ensure {assembly} type(s) are present in {assembly}.csv: {list_missing_item}'.format(assembly=assembly, list_missing_item=list_missing_item))

        list_missing_columns_csv, list_issues_against_csv = verify_file_against_schema_4_db(scenario, ASSEMBLIES, verbose=False, sheet_name=assembly)
        list_list_missing_columns_csv.append(list_missing_columns_csv)
        if print_results:
            if list_missing_columns_csv:
                print('! Ensure column(s) are present in {assembly}.csv: {missing_columns}'.format(assembly=assembly, missing_columns=list_missing_columns_csv))
            if list_issues_against_csv:
                print('! Check values in {assembly}.csv: {list_issues_against_schema}'.format(assembly=assembly, list_issues_against_schema=list_issues_against_csv))

    return list_list_missing_columns_csv

def get_csv_filenames(folder_path):
    """
    Get the names of all .csv files in the specified folder.

    Parameters:
    - folder_path (str): Path to the folder.

    Returns:
    - List[str]: A list of file names without path and without extension.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"The provided path '{folder_path}' is not a valid directory.")

    # List all .csv files and remove the extension
    csv_filenames = [
        os.path.splitext(file)[0]  # Remove the file extension
        for file in os.listdir(folder_path)  # List files in the folder
        if file.endswith('.csv')  # Check for .csv extension
    ]

    return csv_filenames

## --------------------------------------------------------------------------------------------------------------------
## Unique traits for the CEA-4 format
## --------------------------------------------------------------------------------------------------------------------


def cea4_verify_db(scenario, print_results=False):
    """
    Verify the database for the CEA-4 format.

    :param scenario: the scenario to verify
    :param print_results: if True, print the results
    :return: a dictionary with the missing files
    """

    dict_missing_db = {}

    #1. verify columns and values in .csv files for archetypes
    list_missing_files_csv_archetypes = verify_file_exists_4_db(scenario, ARCHETYPES)
    if list_missing_files_csv_archetypes:
        print('! Ensure .csv file(s) are present in the ARCHETYPES folder: {list_missing_files_csv}'.format(list_missing_files_csv=list_missing_files_csv_archetypes))
        print('! CONSTRUCTION_TYPE.csv and USE_TYPE.csv are fundamental and should be present in the ARCHETYPES folder.')
        print('! The CEA-4 Database verification is aborted.')
        sys.exit(0)

    for item in ARCHETYPES:
        if item not in list_missing_files_csv_archetypes:
            list_missing_columns_csv_archetypes, list_issues_against_csv_archetypes = verify_file_against_schema_4_db(scenario, item, verbose=False)
            dict_missing_db[item] = list_missing_columns_csv_archetypes
            if print_results:
                if list_missing_columns_csv_archetypes:
                    print('! Ensure column(s) are present in {item}.csv: {missing_columns}'.format(item=item, missing_columns=list_missing_columns_csv_archetypes))
                if list_issues_against_csv_archetypes:
                    print('! Check value(s) in {item}.csv: {list_issues_against_schema}'.format(item=item, list_issues_against_schema=list_issues_against_csv_archetypes))

    #2. verify columns and values in .csv files for schedules
    use_type_df = pd.read_csv(path_to_db_file_4(scenario, 'USE_TYPE'))
    list_use_types = use_type_df['code'].tolist()
    list_missing_files_csv_schedules = verify_file_exists_4_db(scenario, SCHEDULES_FOLDER, sheet_name=list_use_types)
    if list_missing_files_csv_schedules:
        if print_results:
            print('! Ensure .csv file(s) are present in the ARCHETYPES>SCHEDULES folder: {list_missing_files_csv}'.format(list_missing_files_csv=list_missing_files_csv_schedules))

    for sheet in list_use_types:
        list_missing_columns_csv_schedules, list_issues_against_csv_schedules = verify_file_against_schema_4_db(scenario, 'SCHEDULES', verbose=False, sheet_name=sheet)
        dict_missing_db[SCHEDULES_FOLDER[0]] = list_missing_columns_csv_schedules
        if print_results:
            if list_missing_columns_csv_schedules:
                print('! Ensure column(s) are present in {sheet}.csv: {missing_columns}'.format(sheet=sheet, missing_columns=list_missing_columns_csv_schedules))
            if list_issues_against_csv_schedules:
                print('! Check value(s) in {sheet}.csv: {list_issues_against_schema}'.format(sheet=sheet, list_issues_against_schema=list_issues_against_csv_schedules))

    #3. verify columns and values in .csv files for assemblies
    for ASSEMBLIES in ASSEMBLIES_FOLDERS:
        list_missing_files_csv = verify_file_exists_4_db(scenario, [ASSEMBLIES], dict_ASSEMBLIES[ASSEMBLIES])
        if list_missing_files_csv:
            if print_results:
                print('! Ensure .csv file(s) are present in the ASSEMBLIES>{ASSEMBLIES} folder: {list_missing_files_csv}'.format(ASSEMBLIES=ASSEMBLIES, list_missing_files_csv=list_missing_files_csv))

        list_list_missing_columns_csv = verify_assembly(scenario, ASSEMBLIES, list_missing_files_csv, print_results)
        dict_missing_db[ASSEMBLIES] = list_list_missing_columns_csv

    #4. verify columns and values in .csv files for components - conversion
    list_missing_files_csv_conversion_components = verify_file_exists_4_db(scenario, ['CONVERSION'], CONVERSION_COMPONENTS)
    if list_missing_files_csv_conversion_components:
        print('! Ensure .csv file(s) are present in the COMPONENTS>CONVERSION folder: {list_missing_files_csv}'.format(list_missing_files_csv=list_missing_files_csv_conversion_components))

    list_conversion_supply = []
    list_conversion_db = get_csv_filenames(path_to_db_file_4(scenario, 'CONVERSION'))
    for supply_type in ['SUPPLY_HEATING', 'SUPPLY_COOLING']:
        if supply_type not in verify_file_exists_4_db(scenario, ['SUPPLY'], dict_ASSEMBLIES['SUPPLY']):
            supply_df = pd.read_csv(path_to_db_file_4(scenario, 'SUPPLY', supply_type))
            list_conversion_supply.append(supply_df['primary_components', 'secondary_components', 'tertiary_components'].unique())
            list_conversion_supply = [item for sublist in list_conversion_supply for item in sublist]
    list_missing_conversion = list(set(list_conversion_supply) - set(list_conversion_db))
    if list_missing_conversion:
        if print_results:
            print('! Ensure .csv file(s) are present in COMPONENTS>CONVERSION folder: {list_missing_conversion}'.format(list_missing_conversion=list_missing_conversion))

    for sheet in list_conversion_db:
        list_missing_columns_csv_conversion, list_issues_against_csv_conversion = verify_file_against_schema_4_db(scenario, 'CONVERSION', verbose=False, sheet_name=sheet)
        dict_missing_db['CONVERSION'] = list_missing_columns_csv_conversion
        if print_results:
            if list_missing_columns_csv_conversion:
                print('! Ensure column(s) are present in {conversion}.csv: {missing_columns}'.format(conversion=sheet, missing_columns=list_missing_columns_csv_conversion))
            if list_issues_against_csv_conversion:
                print('! Check value(s) in {conversion}.csv: {list_issues_against_schema}'.format(conversion=sheet, list_issues_against_schema=list_issues_against_csv_conversion))

    #5. verify columns and values in .csv files for components - distribution
    list_missing_files_csv_distribution_components = verify_file_exists_4_db(scenario, ['DISTRIBUTION'], DISTRIBUTION_COMPONENTS)
    if list_missing_files_csv_distribution_components:
        print('! Ensure .csv file(s) are present in the COMPONENTS>DISTRIBUTION folder: {list_missing_files_csv}'.format(list_missing_files_csv=list_missing_files_csv_distribution_components))

    list_missing_columns_csv_distribution, list_issues_against_csv_distribution = verify_file_against_schema_4_db(scenario, 'DISTRIBUTION', verbose=False)
    dict_missing_db['DISTRIBUTION'] = list_missing_columns_csv_distribution
    if print_results:
        if list_missing_columns_csv_distribution:
            print('! Ensure column(s) are present in DISTRIBUTION.csv: {missing_columns}'.format(missing_columns=list_missing_columns_csv_distribution))
        if list_issues_against_csv_distribution:
            print('! Check value(s) in DISTRIBUTION.csv: {list_issues_against_schema}'.format(list_issues_against_schema=list_issues_against_csv_distribution))

    #6. verify columns and values in .csv files for components - feedstocks
    list_missing_files_csv_feedstocks_components = verify_file_exists_4_db(scenario, ['FEEDSTOCKS'], FEEDSTOCKS_COMPONENTS)
    if list_missing_files_csv_feedstocks_components:
        print('! Ensure .csv file(s) are present in the COMPONENTS folder: {list_missing_files_csv}'.format(list_missing_files_csv=list_missing_files_csv_feedstocks_components))

    list_feedstocks_supply = []
    list_feedstocks_db = get_csv_filenames(path_to_db_file_4(scenario, 'FEEDSTOCKS'))
    for supply_type in SUPPLY_ASSEMBLIES:
        if supply_type not in verify_file_exists_4_db(scenario, ['SUPPLY'], dict_ASSEMBLIES['SUPPLY']):
            supply_df = pd.read_csv(path_to_db_file_4(scenario, supply_type))
            list_feedstocks_supply.append(supply_df['feedstock'].unique())
            list_feedstocks_supply = [item for sublist in list_feedstocks_supply for item in sublist]
    list_missing_feedstocks = list(set(list_feedstocks_supply) - set(list_feedstocks_db))
    if list_missing_feedstocks:
        if print_results:
            print('! Ensure .csv file(s) are present in COMPONENTS>FEEDSTOCKS folder: {list_missing_feedstocks}'.format(list_missing_feedstocks=list_missing_feedstocks))

    for sheet in list_feedstocks_db:
        list_missing_columns_csv_feedstocks, list_issues_against_csv_feedstocks = verify_file_against_schema_4_db(scenario, 'FEEDSTOCKS', verbose=False, sheet_name=sheet)
        dict_missing_db['FEEDSTOCKS'] = list_missing_columns_csv_feedstocks
        if print_results:
            if list_missing_columns_csv_feedstocks:
                print('! Ensure column(s) are present in {feedstocks}.csv: {missing_columns}'.format(feedstocks=sheet, missing_columns=list_missing_columns_csv_feedstocks))
            if list_issues_against_csv_feedstocks:
                print('! Check value(s) in {feedstocks}.csv: {list_issues_against_schema}'.format(feedstocks=sheet, list_issues_against_schema=list_issues_against_csv_feedstocks))

    return dict_missing_db

## --------------------------------------------------------------------------------------------------------------------
## Main function
## --------------------------------------------------------------------------------------------------------------------


def main(config):
    # Start the timer
    t0 = time.perf_counter()
    assert os.path.exists(config.general.project), 'input file not found: %s' % config.project

    # Get the scenario name
    scenario = config.scenario
    scenario_name = os.path.basename(scenario)

    # Print: Start
    div_len = 37 - len(scenario_name)
    print('+' * 60)
    print("-" * 1 + ' Scenario: {scenario} '.format(scenario=scenario_name) + "-" * div_len)

    # Execute the verification
    dict_missing_db = cea4_verify_db(scenario, print_results=True)

    # Print the results
    print_verification_results_4_db(scenario_name, dict_missing_db)

    # Print the time used for the entire processing
    time_elapsed = time.perf_counter() - t0

    # Print: End
    print('+' * 60)
    print('The entire process of CEA-4 format verification is now completed - time elapsed: %.2f seconds' % time_elapsed)

if __name__ == '__main__':
    main(cea.config.Configuration())
