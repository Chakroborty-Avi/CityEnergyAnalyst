# coding=utf-8
"""
'sus_calibrator.py' script hosts the following functions:
    (1) calls
    (2) collect CEA outputs (demands)
    (3) add delay to time-sensitive inputs
    (4) return the input and target matrices
"""

import os
import multiprocessing as mp
import numpy as np
import pandas as pd
from cea.demand.metamodel.nn_generator.nn_trainer_estimate import input_prepare_estimate
from cea.demand.demand_main import properties_and_schedule
from cea.demand.metamodel.nn_generator.nn_settings import nn_delay, target_parameters, warmup_period
from cea.demand.metamodel.nn_generator.input_matrix import get_cea_inputs
from cea.demand.metamodel.nn_generator.nn_trainer_resume import nn_model_collector
import cea.inputlocator
import cea.globalvar
import cea.config
from cea.utilities import epwreader

__author__ = "Fazel Khayatian"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Fazel Khayatian","Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"



def ss_calibrator(number_samples_scaler,locator,list_building_names):
    scaler_inout_path = locator.get_minmaxscaler_folder()
    model, scalerT, scalerX = nn_model_collector(locator)
    for i in range(number_samples_scaler):
        file_path_inputs = os.path.join(scaler_inout_path, "input%(i)s.csv" % locals())
        urban_input_matrix = np.asarray(pd.read_csv(file_path_inputs))
        # reshape file to get a tensor of buildings, features, time.
        num_buildings = len(list_building_names)
        num_features = len(urban_input_matrix[0])
        num_outputs = len(target_parameters)
        matrix = np.empty([num_buildings, 8759 + warmup_period, num_outputs])
        reshaped_input_matrix = urban_input_matrix.reshape(num_buildings, 8759, num_features)
        # including warm up period
        warmup_period_input_matrix = reshaped_input_matrix[:, (8759 - warmup_period):, :]
        concat_input_matrix = np.hstack((warmup_period_input_matrix, reshaped_input_matrix))

        for i in range(8759 + warmup_period):
            one_hour_step = concat_input_matrix[:, i, :]
            if i < 1:
                first_hour_step = np.empty([num_buildings, num_outputs])
                first_hour_step = first_hour_step * 0
                one_hour_step[:, 36:41] = first_hour_step
                inputs_x = scalerX.transform(one_hour_step)
                model_estimates = model.predict(inputs_x)
                matrix[:, i, :] = scalerT.inverse_transform(model_estimates)
            else:
                other_hour_step = matrix[:, i - 1, :]
                one_hour_step[:, 36:41] = other_hour_step
                inputs_x = scalerX.transform(one_hour_step)
                model_estimates = model.predict(inputs_x)
                matrix[:, i, :] = scalerT.inverse_transform(model_estimates)

def main(config):
    gv = cea.globalvar.GlobalVariables()
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    weather_data = epwreader.epw_reader(config.weather)[['year', 'drybulb_C', 'wetbulb_C',
                                                         'relhum_percent', 'windspd_ms', 'skytemp_C']]
    year = weather_data['year'][0]
    region = config.region
    settings = config.demand
    use_daysim_radiation = settings.use_daysim_radiation
    building_properties, schedules_dict, date = properties_and_schedule(gv, locator, region, year, use_daysim_radiation)
    list_building_names = building_properties.list_building_names()
    ss_calibrator(number_samples_scaler=config.neural_network.number_samples_scaler,
                  locator=cea.inputlocator.InputLocator(scenario=config.scenario),
                  list_building_names=building_properties.list_building_names())


if __name__ == '__main__':
    main(cea.config.Configuration())