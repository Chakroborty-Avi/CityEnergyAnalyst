"""
===========================
Bayesian calibration routine
##check this for timeseries calculation https://arxiv.org/abs/1206.5015
##https: // www.ncbi.nlm.nih.gov / pubmed / 10985202
#http://www.map.ox.ac.uk/media/PDF/Patil_et_al_2010.pdf
===========================
J. Fonseca  script development          27.10.16


"""
from __future__ import division

import pandas as pd
import numpy as np
import pymc3 as pm
import theano.tensor as tt
import theano
from cea.demand import demand_main

import cea.globalvar as gv
gv = gv.GlobalVariables()
import cea.inputlocator as inputlocator
scenario_path = gv.scenario_reference
locator = inputlocator.InputLocator(scenario_path=scenario_path)
weather_path = locator.get_default_weather()


__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def calibration_main(group_var, building_name, building_load):

    #import arguments of probability density functions (PDF) of variables and create priors:
    pdf_arg = pd.concat([pd.read_excel(locator.get_uncertainty_db(), group, axis=1) for group in group_var]).set_index('name')
    var_names = pdf_arg.index

    #import measured data for building and building load:
    obs_data = pd.read_csv(locator.get_demand_results_file(building_name))[building_load].values

    # create funcitionf of demand calaculation and send to theano
    @theano.compile.ops.as_op(itypes=[tt.dscalar, tt.dscalar, tt.dscalar, tt.dscalar], otypes=[tt.dvector])
    def demand_calculation(phi, err, u_win, u_wall):
        gv.samples = {'U_win':u_win,'U_wall':u_wall}
        gv.multiprocessing = False
        demand_main.demand_calculation(locator, weather_path, gv) # simulation
        result = pd.read_csv(locator.get_demand_results_file(building_name), usecols=[building_load])*(1 + phi + err)
        out = result[building_load].values
        return out

    with pm.Model() as basic_model:

        # get priors for the input variables of the model assuming they are all uniform
        #priors = [pm.Uniform(name, lower=a, upper=b) for name, a, b in zip(var_names, pdf_arg['min'].values,
        #                                                                   pdf_arg['max'].values)]

        u_win = pm.Uniform('u_win', lower=0.9, upper=3.1)
        u_wall = pm.Uniform('u_wall', lower=0.11, upper=1.5)
        # get priors for the model inaquacy and the measurement errors.
        phi = pm.Uniform('phi', lower=0, upper=0.01)
        err = pm.Uniform('err', lower=0, upper=0.02)
        sigma = pm.HalfNormal('sigma', sd=1)

        # expected value of outcome
        mu = pm.Deterministic('mu',demand_calculation(phi, err, u_win, u_wall))

        # Likelihood (sampling distribution) of observations
        y_obs = pm.Normal('y_obs', mu=mu, sd=sigma, observed=obs_data)

    with basic_model:
        #call NUTS - MCMC process:
        # the start point:
        #mu, sds, elbo = pm.variational.advi(n=100000)
        #import scipy
        #start = pm.find_MAP(fmin=scipy.optimize.fmin_powell)

        # the step
        step = pm.Metropolis()#pm.NUTS(scaling = basic_model.dict_to_array(sds)**2,is_cov=True)

        # the traces
        trace = pm.sample(100, step=step)#pm.sample(10, step, start = mu, progressbar=True)

    pm.traceplot(trace)

    return



def run_as_script():
    group_var = ['THERMAL']
    building_name = 'B01'
    building_load = 'Qhsf_kWh'
    calibration_main(group_var, building_name, building_load )

if __name__ == '__main__':
    run_as_script()