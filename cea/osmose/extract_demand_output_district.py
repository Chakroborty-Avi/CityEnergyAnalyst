import pandas as pd
import numpy as np
import os
from geopandas import GeoDataFrame as Gdf
from simpledbf import Dbf5
from cea.osmose.extract_demand_outputs import extract_cea_outputs_to_osmose_main, path_to_osmose_project_bui, \
    path_to_osmose_project_hcs


def extract_demand_output_district_to_osmose(path_to_district_folder, timesteps, season, specified_building):

    # read building function and GFA from district
    occupancy_df = read_dbf(path_to_district_folder, 'occupancy')
    occupancy_df = occupancy_df.set_index('Name')
    # calculate Af
    geometry_df = calc_Af(path_to_district_folder)
    # calculate Af per function
    Af_per_function = {}
    for function in ['HOTEL', 'OFFICE', 'RETAIL']:
        buildings = occupancy_df[function][occupancy_df[function]==1].index
        Af_per_function[function[:3]] = geometry_df['Af'][buildings].sum()

    # read building function
    for case in ['WTP_CBD_m_WP1_OFF', 'WTP_CBD_m_WP1_HOT', 'WTP_CBD_m_WP1_RET']:
        output_building, output_hcs = extract_cea_outputs_to_osmose_main(case, timesteps, season, specified_building,
                                                                         problem_type='district')
        # get file and extrapolate
        building_Af_m2 = output_hcs['Af_m2'][0]
        multiplication_factor = Af_per_function[case.split('_')[4]] / building_Af_m2
        ## output_building
        columns_with_scalar_values = [column for column in output_building.columns if 'Tww' not in column]
        scalar_df = output_building[columns_with_scalar_values] * multiplication_factor
        output_building.update(scalar_df)
        output_building.T.to_csv(path_to_osmose_project_bui('B_' + case.split('_')[4]), header=False) # save files
        ## output_hcs
        columns_with_scalar_values = [column for column in output_hcs.columns
                               if ('v_' in column or 'V_' in column or 'm_' in column or 'M_' in column or
                                   'Af_m2' in column or 'Vf_m3' in column)]
        scalar_df = output_hcs[columns_with_scalar_values] * multiplication_factor
        output_hcs.update(scalar_df)
        output_hcs.T.to_csv(path_to_osmose_project_hcs('B_' + case.split('_')[4], 'hcs'), header=False) # save files
        # remove T_OAU_offcoil
        T_OAU_offcoil_df = output_hcs[[column for column in output_hcs.columns if 'T_OAU_offcoil' in column]]
        output_hcs.drop(columns=[column for column in output_hcs.columns if 'T_OAU_offcoil' in column], inplace=True)
        # save output_hcs for each T_OAU_offcoil
        for i, column in enumerate(T_OAU_offcoil_df.columns):
            new_hcs_df = output_hcs.copy()
            new_hcs_df['T_OAU_offcoil'] = T_OAU_offcoil_df[column]
            file_name_extension = 'hcs_in' + str(i + 1)
            new_hcs_df.T.to_csv(path_to_osmose_project_hcs('B_'+case.split('_')[4], file_name_extension), header=False)



def calc_Af(path_to_district_folder):
    geometry_df = read_dbf(path_to_district_folder, 'geometry')
    geometry_df['footprint'] = geometry_df.area
    geometry_df['GFA'] = geometry_df['footprint'] * (
            geometry_df['floors_bg'] + geometry_df['floors_ag'])  # gross floor area
    geometry_df = geometry_df.set_index('Name')
    architecture_df = read_dbf(path_to_district_folder, 'architecture')
    architecture_df = architecture_df.set_index('Name')
    geometry_df['Af'] = geometry_df['GFA'] * architecture_df['Hs_ag']
    return geometry_df


def read_dbf(path_to_district_folder, file_name):
    file_paths = {'occupancy': 'inputs\\building-properties\\occupancy.dbf',
                  'geometry': 'inputs\\building-geometry\\zone.dbf',
                  'architecture': 'inputs\\building-properties\\architecture.dbf'}
    if file_name == 'geometry':
        df = Gdf.from_file(os.path.join(path_to_district_folder, file_paths[file_name]))
    else:
        dbf = Dbf5(os.path.join(path_to_district_folder, file_paths[file_name]))
        df = dbf.to_dataframe()
    return df



if __name__ == '__main__':
    path_to_district_folder = 'C:\\SG_cases\\SDC'
    timesteps = 24
    season = 'Summer'
    specified_building = ["B006"]
    extract_demand_output_district_to_osmose(path_to_district_folder, timesteps, season, specified_building)