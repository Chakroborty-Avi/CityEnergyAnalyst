import os
import cea.config as config
import cea.inputlocator
import pandas
import geopandas
import json
import pysal.core


locator = cea.inputlocator.InputLocator(config.Configuration().scenario)
# NAMING_FILE_PATH = os.path.join(os.path.dirname(cea.config.__file__),'plots/naming.csv')
# with open(NAMING_FILE_PATH) as naming_file:
#     NAMING = {row['VARIABLE']: (row['SHORT_DESCRIPTION'],row['UNIT']) for row in csv.DictReader(naming_file)}


trace_data=[('input', 'demand', 'get_archetypes_properties', 'databases/CH/archetypes', 'construction_properties.xlsx'), ('input', 'demand', 'get_archetypes_schedules', 'databases/CH/archetypes', 'occupancy_schedules.xlsx'), ('input', 'demand', 'get_archetypes_system_controls', 'databases/CH/archetypes', 'system_controls.xlsx'), ('input', 'demand', 'get_building_age', 'inputs/building-properties', 'age.dbf'), ('input', 'demand', 'get_building_architecture', 'inputs/building-properties', 'architecture.dbf'), ('input', 'demand', 'get_building_comfort', 'inputs/building-properties', 'indoor_comfort.dbf'), ('input', 'demand', 'get_building_hvac', 'inputs/building-properties', 'technical_systems.dbf'), ('input', 'demand', 'get_building_internal', 'inputs/building-properties', 'internal_loads.dbf'), ('input', 'demand', 'get_building_occupancy', 'inputs/building-properties', 'occupancy.dbf'), ('input', 'demand', 'get_building_supply', 'inputs/building-properties', 'supply_systems.dbf'), ('input', 'demand', 'get_envelope_systems', 'databases/CH/systems', 'envelope_systems.xls'), ('input', 'demand', 'get_life_cycle_inventory_supply_systems', 'databases/CH/lifecycle', 'LCA_infrastructure.xlsx'), ('input', 'demand', 'get_radiation_building', 'outputs/data/solar-radiation', '{BUILDING}_insolation_Whm2.json'), ('input', 'demand', 'get_radiation_metadata', 'outputs/data/solar-radiation', '{BUILDING}_geometry.csv'), ('input', 'demand', 'get_technical_emission_systems', 'databases/CH/systems', 'emission_systems.xls'), ('input', 'demand', 'cea/databases/weather', '../../users/jack/documents/github/cityenergyanalyst/cea/databases/weather', 'Zug.epw'), ('input', 'demand', 'get_zone_geometry', 'inputs/building-geometry', 'zone.shp'), ('output', 'demand', 'get_demand_results_file', 'outputs/data/demand', '{BUILDING}.csv'), ('output', 'demand', 'get_total_demand', 'outputs/data/demand', 'Total_demand.csv')]
results_set = set([('get_radiation_building', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B07_insolation_Whm2.json'), ('get_radiation_metadata', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B01_geometry.csv'), ('get_building_comfort', 'C:\\reference-case-open\\baseline\\inputs\\building-properties\\indoor_comfort.dbf'), ('get_temporary_file', u'c:\\users\\jack\\appdata\\local\\temp\\B05T.csv'), ('get_demand_results_file', u'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\B08.csv'), ('get_building_properties_folder', 'C:\\reference-case-open\\baseline\\inputs\\building-properties'), ('get_radiation_metadata', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B06_geometry.csv'), ('get_building_occupancy', 'C:\\reference-case-open\\baseline\\inputs\\building-properties\\occupancy.dbf'), ('get_envelope_systems', 'C:\\reference-case-open\\baseline\\databases\\CH\\systems\\envelope_systems.xls'), ('get_building_age', 'C:\\reference-case-open\\baseline\\inputs\\building-properties\\age.dbf'), ('get_archetypes_system_controls', 'C:\\reference-case-open\\baseline\\databases\\CH\\archetypes\\system_controls.xlsx'), ('get_weather', 'c:\\users\\jack\\documents\\github\\cityenergyanalyst\\cea\\databases\\weather\\Zug.epw'), ('get_zone_geometry', 'C:\\reference-case-open\\baseline\\inputs\\building-geometry\\zone.shp'), ('get_temporary_file', u'c:\\users\\jack\\appdata\\local\\temp\\B09T.csv'), ('get_building_supply', 'C:\\reference-case-open\\baseline\\inputs\\building-properties\\supply_systems.dbf'), ('get_demand_results_file', u'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\B05.csv'), ('get_radiation_building', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B03_insolation_Whm2.json'), ('get_demand_results_file', u'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\B06.csv'), ('get_solar_radiation_folder', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation'), ('get_temporary_folder', 'c:\\users\\jack\\appdata\\local\\temp'), ('get_radiation_metadata', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B09_geometry.csv'), ('get_radiation_building', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B09_insolation_Whm2.json'), ('get_radiation_metadata', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B05_geometry.csv'), ('get_radiation_metadata', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B07_geometry.csv'), ('get_radiation_metadata', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B08_geometry.csv'), ('get_radiation_metadata', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B03_geometry.csv'), ('get_life_cycle_inventory_supply_systems', 'C:\\reference-case-open\\baseline\\databases\\CH\\lifecycle\\LCA_infrastructure.xlsx'), ('get_archetypes_schedules', 'C:\\reference-case-open\\baseline\\databases\\CH\\archetypes\\occupancy_schedules.xlsx'), ('get_temporary_file', u'c:\\users\\jack\\appdata\\local\\temp\\B04T.csv'), ('get_radiation_building', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B01_insolation_Whm2.json'), ('get_building_architecture', 'C:\\reference-case-open\\baseline\\inputs\\building-properties\\architecture.dbf'), ('get_technical_emission_systems', 'C:\\reference-case-open\\baseline\\databases\\CH\\systems\\emission_systems.xls'), ('get_demand_results_file', u'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\B03.csv'), ('get_temporary_file', u'c:\\users\\jack\\appdata\\local\\temp\\B08T.csv'), ('get_temporary_file', u'c:\\users\\jack\\appdata\\local\\temp\\B06T.csv'), ('get_building_internal', 'C:\\reference-case-open\\baseline\\inputs\\building-properties\\internal_loads.dbf'), ('get_temporary_file', u'c:\\users\\jack\\appdata\\local\\temp\\B01T.csv'), ('get_radiation_building', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B04_insolation_Whm2.json'), ('get_archetypes_properties', 'C:\\reference-case-open\\baseline\\databases\\CH\\archetypes\\construction_properties.xlsx'), ('find_db_path', 'c:\\users\\jack\\documents\\github\\cityenergyanalyst\\cea\\databases'), ('get_radiation_building', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B02_insolation_Whm2.json'), ('get_demand_results_file', u'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\B04.csv'), ('get_radiation_metadata', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B04_geometry.csv'), ('get_radiation_building', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B08_insolation_Whm2.json'), ('get_demand_results_folder', 'C:\\reference-case-open\\baseline\\outputs\\data\\demand'), ('get_demand_results_file', u'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\B02.csv'), ('get_temporary_file', u'c:\\users\\jack\\appdata\\local\\temp\\B02T.csv'), ('get_building_hvac', 'C:\\reference-case-open\\baseline\\inputs\\building-properties\\technical_systems.dbf'), ('get_radiation_building', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B05_insolation_Whm2.json'), ('get_building_geometry_folder', 'C:\\reference-case-open\\baseline\\inputs\\building-geometry'), ('get_radiation_metadata', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B02_geometry.csv'), ('get_demand_results_file', u'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\B01.csv'), ('get_temporary_file', u'c:\\users\\jack\\appdata\\local\\temp\\B07T.csv'), ('get_radiation_building', 'C:\\reference-case-open\\baseline\\outputs\\data\\solar-radiation\\B06_insolation_Whm2.json'), ('get_demand_results_file', u'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\B09.csv'), ('get_temporary_file', u'c:\\users\\jack\\appdata\\local\\temp\\B03T.csv'), ('get_demand_results_file', u'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\B07.csv'), ('get_total_demand', 'C:\\reference-case-open\\baseline\\outputs\\data\\demand\\Total_demand.csv')])
locator_meta = {}
meta_set = set()
building_spec_file = []

for locator_method, filename in results_set:
    if os.path.isdir(filename):
        continue
    if locator_method == 'get_temporary_file':
        # this file is probably already deleted (hopefully?)
        continue
    # create new method separating trace_data used for graphviz and results_set used for metadata
    if os.path.isfile(filename):
        buildings = locator.get_zone_building_names()

        for building in buildings:
            if os.path.basename(filename).find(building) != -1:
                building_spec_file.append(filename)
                filename = filename.replace(building, buildings[0])
                meta_set.add((locator_method, filename))
        if filename not in building_spec_file:
            meta_set.add((locator_method, filename))


for locator_method, filename in meta_set:

    file_name = os.path.basename(filename).split('.')[0]
    file_type = filename.split('.')[1]
    location = os.path.dirname(filename.replace('\\', '/'))
    description = eval('cea.inputlocator.InputLocator(config.Configuration().scenario).' + str(
        locator_method) + '.__doc__')



    if file_type == 'xls' or file_type == 'xlsx':

# def get_xls_meta(filename):

        xls = pandas.ExcelFile(filename, on_demand=True)
        contents = dict((k, {}) for k in xls.sheet_names)

        for sheet in contents:
            db = pandas.read_excel(filename, sheet_name=sheet, on_demand=True)

            # if the xls appears to be row indexed
            if 'Unnamed: 1' in db.columns:
                db = db.T
                new_cols = []
                for i in db.columns:
                    if i == i:
                        new_cols.append(i)
                db.index = range(len(db))
                db = db[new_cols]

            attributes = dict((k, ()) for k in db)

            for attr in attributes.keys():

                dtype = set()

                for data in zip(db[attr]):
                    for i in range(0, len(data)):
                        dtype.add(type(data[i]))

                    attributes[attr] = (data[0], dtype)

            contents[sheet] = attributes


#        return contents

    if file_type == 'csv':

# def get_csv_meta():
        db = pandas.read_csv(filename)
        contents = {}
        attributes = dict((k, ()) for k in db)

        for attr in attributes.keys():
            dtype = set()
            for data in zip(db[attr]):
                for i in range(0, len(data)):
                    dtype.add(type(data[i]))
                attributes[attr] = (data[0], dtype)

        contents['Sheet1'] = attributes


# def get_dbf_meta():
    if file_type == 'dbf':

        db = pysal.open(filename, 'r')
        contents = {}
        attributes = dict((k, ()) for k in db.header)
        dtype = set()

        for attr in attributes.keys():
            data = db.by_col(attr)
            dtype.add(type(data))
            attributes[attr] = (data[0], dtype)
        contents['Sheet1'] = attributes




# def get_json_meta():
    if file_type == 'json':


        with open(filename, 'r') as f:
            db = json.load(f)
            contents = {}
            attributes = dict((k, ()) for k in db.keys())

            for attr in attributes.keys():
                dtype = set()

                for data in zip(db[attr]):
                    dtype.add(type(data[0]))
                    attributes[attr] = (data[0], dtype)
        contents['Sheet1'] = attributes

    # def get_shp_meta():
    if file_type == 'shp':

        db = geopandas.read_file(filename)
        contents = {}
        attributes = dict((k, ()) for k in db.keys())

        for attr in attributes.keys():

            dtype = set()
            for data in zip(db[attr]):
                length = len(data)
                for i in range(0, len(data)):
                    dtype.add(type(data[i]))
                    attributes[attr] = (data[0], dtype, length)
        contents['Sheet1'] = attributes

    # def get_epw_meta():
    if file_type == 'epw':
        epw_labels = ['year (index = 0)', 'month (index = 1)', 'day (index = 2)', 'hour (index = 3)',
                      'minute (index = 4)', 'datasource (index = 5)', 'drybulb_C (index = 6)', 'dewpoint_C (index = 7)',
                      'relhum_percent (index = 8)', 'atmos_Pa (index = 9)', 'exthorrad_Whm2 (index = 10)',
                      'extdirrad_Whm2 (index = 11)', 'horirsky_Whm2 (index = 12)', 'glohorrad_Whm2 (index = 13)',
                      'dirnorrad_Whm2 (index = 14)', 'difhorrad_Whm2 (index = 15)', 'glohorillum_lux (index = 16)',
                      'dirnorillum_lux (index = 17)', 'difhorillum_lux (index = 18)', 'zenlum_lux (index = 19)',
                      'winddir_deg (index = 20)', 'windspd_ms (index = 21)', 'totskycvr_tenths (index = 22)',
                      'opaqskycvr_tenths (index = 23)', 'visibility_km (index = 24)', 'ceiling_hgt_m (index = 25)',
                      'presweathobs (index = 26)', 'presweathcodes (index = 27)', 'precip_wtr_mm (index = 28)',
                      'aerosol_opt_thousandths (index = 29)', 'snowdepth_cm (index = 30)',
                      'days_last_snow (index = 31)', 'Albedo (index = 32)', 'liq_precip_depth_mm (index = 33)',
                      'liq_precip_rate_Hour (index = 34)']

        attributes = dict((k, ()) for k in epw_labels)
        db = pandas.read_csv(filename, skiprows=8, header=None, names=epw_labels)
        contents = {}

        for attr in db:
            dtype = set()
            for data in zip(db[attr]):
                for i in range(0, len(data)):
                    dtype.add(type(data[i]))
                    attributes[attr] = (data[0], dtype)

        contents['Sheet1'] = attributes
        print contents



    if file_type == 'tif':

        contents = {}


    db_info = (file_name, file_type, location, description, contents)
    locator_meta[locator_method] = db_info

lala = [2005,01,01,01,60,"*?*?*?*?*?*?*?*?*?*?*?*?*?*?*?*?*?*?*?*?*?*?",8.8,2.6,65,96189,0,0,310,0,0,0,0,0,0,9999,218,0.5,8,6,9999,99999,9,999999999,11,0.176,2,0,0.578,0.0,99.0]
epw_labels = ['year', 'month', 'day', 'hour', 'minute', 'datasource', 'drybulb_C', 'dewpoint_C', 'relhum_percent',
              'atmos_Pa', 'exthorrad_Whm2', 'extdirrad_Whm2', 'horirsky_Whm2', 'glohorrad_Whm2',
              'dirnorrad_Whm2', 'difhorrad_Whm2', 'glohorillum_lux', 'dirnorillum_lux', 'difhorillum_lux',
              'zenlum_lux', 'winddir_deg', 'windspd_ms', 'totskycvr_tenths', 'opaqskycvr_tenths', 'visibility_km',
              'ceiling_hgt_m', 'presweathobs', 'presweathcodes', 'precip_wtr_mm', 'aerosol_opt_thousandths',
              'snowdepth_cm', 'days_last_snow', 'Albedo', 'liq_precip_depth_mm', 'liq_precip_rate_Hour']
# print len(lala)
# print len(epw_labels)
nana = []
for i, label in enumerate(epw_labels):
    nana.append(str(label)+' (index = %s)' %i)

# epw_labels = ['year (index = i)', 'month (index = i)', 'day (index = i)', 'hour (index = i)', 'minute (index = i)', 'datasource (index = i)', 'drybulb_C (index = i)', 'dewpoint_C (index = i)', 'relhum_percent (index = i)', 'atmos_Pa (index = i)', 'exthorrad_Whm2 (index = i)', 'extdirrad_Whm2 (index = i)', 'horirsky_Whm2 (index = i)', 'glohorrad_Whm2 (index = i)', 'dirnorrad_Whm2 (index = i)', 'difhorrad_Whm2 (index = i)', 'glohorillum_lux (index = i)', 'dirnorillum_lux (index = i)', 'difhorillum_lux (index = i)', 'zenlum_lux (index = i)', 'winddir_deg (index = i)', 'windspd_ms (index = i)', 'totskycvr_tenths (index = i)', 'opaqskycvr_tenths (index = i)', 'visibility_km (index = i)', 'ceiling_hgt_m (index = i)', 'presweathobs (index = i)', 'presweathcodes (index = i)', 'precip_wtr_mm (index = i)', 'aerosol_opt_thousandths (index = i)', 'snowdepth_cm (index = i)', 'days_last_snow (index = i)', 'Albedo (index = i)', 'liq_precip_depth_mm (index = i)', 'liq_precip_rate_Hour (index = i)']

epw_labels = ['year (index = 0)', 'month (index = 1)', 'day (index = 2)', 'hour (index = 3)', 'minute (index = 4)', 'datasource (index = 5)', 'drybulb_C (index = 6)', 'dewpoint_C (index = 7)', 'relhum_percent (index = 8)', 'atmos_Pa (index = 9)', 'exthorrad_Whm2 (index = 10)', 'extdirrad_Whm2 (index = 11)', 'horirsky_Whm2 (index = 12)', 'glohorrad_Whm2 (index = 13)', 'dirnorrad_Whm2 (index = 14)', 'difhorrad_Whm2 (index = 15)', 'glohorillum_lux (index = 16)', 'dirnorillum_lux (index = 17)', 'difhorillum_lux (index = 18)', 'zenlum_lux (index = 19)', 'winddir_deg (index = 20)', 'windspd_ms (index = 21)', 'totskycvr_tenths (index = 22)', 'opaqskycvr_tenths (index = 23)', 'visibility_km (index = 24)', 'ceiling_hgt_m (index = 25)', 'presweathobs (index = 26)', 'presweathcodes (index = 27)', 'precip_wtr_mm (index = 28)', 'aerosol_opt_thousandths (index = 29)', 'snowdepth_cm (index = 30)', 'days_last_snow (index = 31)', 'Albedo (index = 32)', 'liq_precip_depth_mm (index = 33)', 'liq_precip_rate_Hour (index = 34)']




#
# for method in locator_meta.keys():
#     for content in zip(locator_meta[method])[4]:
#         print content.keys()
        #
        # for sheet in contents.keys():
        #     print sheet
            # for i in range(len(content[sheet])):
                # print zip(content[sheet])[i]











