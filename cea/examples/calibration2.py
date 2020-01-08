"""
This tool calibrates a set of inputs from CEA to reduce the error between model outputs (predicted) and measured data (observed)
"""
from __future__ import division
from __future__ import print_function

import os
import cea.config
import cea.inputlocator
from cea.utilities.dbf import dbf_to_dataframe, dataframe_to_dbf
from cea.demand import demand_main
from cea.demand.schedule_maker import schedule_maker
from cea.examples import validation
import numpy as np
from scipy.optimize import minimize
from hyperopt import hp
from collections import OrderedDict
from sklearn.linear_model import LogisticRegression
import hyperopt.pyll
from hyperopt.pyll import scope
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt
from cea.constants import MONTHS_IN_YEAR, MONTHS_IN_YEAR_NAMES

__author__ = "Luis Santos"
__copyright__ = "Copyright 2018, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Luis Santos, Jimeno Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

# define a search space
SPACE = OrderedDict([('Es', hp.uniform('Es', 0.6, 1.0)),
                     ('Ns', hp.uniform('subsample', 0.7, 1.0)),
                     ('Occ_m2pax', hp.uniform('Occ_m2pax', 30.0, 60.0)),
                     ('Vww_lpdpax', hp.uniform('Vww_lpdpax', 20.0, 40.0)),
                     ('Ea_Wm2', hp.uniform('Ea_Wm2', 1.0, 5.0)),
                    ('El_Wm2', hp.uniform('El_Wm2', 1.0, 5.0))
                    ])

SPACE2 = hp.choice('classifier_type', [

                    ('Es', hp.uniform('Es', 0.6, 1.0)),
                     ('Ns', hp.uniform('subsample', 0.7, 1.0)),
                     ('Occ_m2pax', hp.uniform('Occ_m2pax', 30.0, 60.0)),
                     ('Vww_lpdpax', hp.uniform('Vww_lpdpax', 20.0, 40.0)),
                     ('Ea_Wm2', hp.uniform('Ea_Wm2', 1.0, 5.0)),
                    ('El_Wm2', hp.uniform('El_Wm2', 1.0, 5.0))
                    ])

space = hp.choice('classifier',[
                      {
                       'model': LogisticRegression,
                       'param':
                         {
                             'hyper_param_groups' :hp.choice('hyper_param_groups',
                                             [
                                                {
                                                 'penalty':hp.choice('penalty_block1', ['l2']),
                                                 'solver':hp.choice('solver_block1', ['newton-cg', 'sag', 'saga', 'lbfgs']),
                                                 'multi_class':hp.choice('multi_class', ['ovr', 'multinomial']),
                                                },
                                                {
                                                 'penalty':hp.choice('penalty_block2', ['l2']),
                                                 'solver':hp.choice('solver_block2', ['liblinear']),
                                                 'multi_class':hp.choice('multi_class_block2', ['ovr']),
                                                },
                                                {
                                                 'penalty':hp.choice('penalty_block3', ['l1']),
                                                 'solver':hp.choice('solver_block3', ['saga']),
                                                 'multi_class':hp.choice('multi_class_block3', ['ovr', 'multinomial']),
                                                },
                                             ]),
                            'dual':hp.choice('dual', [False]),
                            'class_weight':hp.choice('class_weight', ['balanced', None]),
                            'random_state':hp.choice('random_state', [10,267]),
                            'max_iter':hp.choice('max_iter', [100,500]),
                            'verbose':hp.choice('verbose', [0])
                         }
                      }])

def calibration(locator, config):
    """
    This tool reduces the error between observed (real life measured data) and predicted (output of the model data) values by changing some of CEA inputs.
    Annual data is compared in terms of MBE and monthly data in terms of NMBE and CvRMSE (follwing ASHRAE Guideline 14-2002).
    A new input folder with measurements has to be created, with a csv each for monthly and annual data provided as input for this tool.
    A new output csv is generated providing for each building (if measured data is available): building ID | ZIP Code | Measured data (observed) | Modelled data (predicted) | Model errors
    """

    ## define set of CEA inputs to be calibrated and initial guess values
    Es = 0.7
    Ns = 0.8
    Hs_ag = 0
    Occ_m2pax = 50
    Vww_lpdpax = 30
    Ea_Wm2 = 4
    El_Wm2 = 2
    Tcs_set_C = 40
    Tcs_setb_C = 40


    ## overwrite inputs with corresponding initial values
    df_arch = dbf_to_dataframe(locator.get_building_architecture())
    df_arch.Es = Es
    df_arch.Ns = Ns
    df_arch.Hs_ag = Hs_ag
    df_arch = dataframe_to_dbf(df_arch, locator.get_building_architecture())

    df_intload = dbf_to_dataframe(locator.get_building_internal())
    df_intload.Occ_m2pax = Occ_m2pax
    df_intload.Vww_lpdpax = Vww_lpdpax
    df_intload.Ea_Wm2 = Ea_Wm2
    df_intload.El_Wm2 = El_Wm2
    df_intload = dataframe_to_dbf(df_intload, locator.get_building_internal())

    df_comfort = dbf_to_dataframe(locator.get_building_comfort())
    df_comfort.Tcs_set_C = Tcs_set_C
    df_comfort.Tcs_setb_C = Tcs_setb_C
    df_comfort = dataframe_to_dbf(df_comfort, locator.get_building_comfort())

    ## run building schedules and energy demand (first run)
    schedule_maker.schedule_maker_main(locator, config, building=None)
    demand_main.demand_calculation(locator, config)
    validation.validation(locator)

    ## define function to be minimized

    # def objective(params):
    #     all_params = {**params, **STATIC_PARAMS}
    #     score = -1.0 * train_evaluate(X, y, all_params)
    #     monitor_callback(params, score)
    #     return score


    pass


def main(config):
    """
    This is the main entry point to your script. Any parameters used by your script must be present in the ``config``
    parameter. The CLI will call this ``main`` function passing in a ``config`` object after adjusting the configuration
    to reflect parameters passed on the command line - this is how the ArcGIS interface interacts with the scripts
    BTW.

    :param config:
    :type config: cea.config.Configuration
    :return:
    """
    assert os.path.exists(config.scenario), 'Scenario not found: %s' % config.scenario
    locator = cea.inputlocator.InputLocator(config.scenario)

    calibration(locator, config)


if __name__ == '__main__':
    main(cea.config.Configuration())
