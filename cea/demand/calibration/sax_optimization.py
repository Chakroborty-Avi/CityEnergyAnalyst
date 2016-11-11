"""
===========================
Optimization of wordsize and alphabtsize for Symbolic Aggregate approXimation in python.
===========================

"""
from __future__ import division

import math

import numpy as np
from numpy import random
from cea.demand.calibration.sax import SAX
from deap import base, creator, tools
from deap.benchmarks.tools import diversity, convergence, hypervolume
from sklearn.metrics import silhouette_score
from sklearn import metrics
import pickle

import matplotlib.pyplot as plt

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"



def SAX_opt(locator, data, time_series_len, BOUND_LOW, BOUND_UP, NGEN, MU, CXPB, start_gen):
    """
    A multi-objective problem set for three objectives to maximize using the DEAP library and NSGAII algorithm:
    1. Compound function of accurracy, complexity and compression based on the work of
    D. Garcia-Lopez1 and H. Acosta-Mesa 2009
    2. Classic Shiluette and
    3. Carlinski indicators of clustering.

    The variables to maximize are wordsize and alphabet size.

    :param data: list of lists containing the real values of the discretized timeseries (hourly values for every day).
    :param time_series_len: length of discretized timeseries.
    :param BOUND_LOW: lower bound
    :param BOUND_UP: upper bound
    :param NGEN: maximum number of generation
    :param MU: initial number of individuals (it has to be a multiple of 4 for this problem)
    :param CXPB: confidence
    :return: Plot with pareto front
    """
    # set-up deap library for optimization with 1 objective to minimize and 2 objectives to be maximized
    creator.create("Fitness", base.Fitness, weights=(1.0, 1.0))  # maximize shilluette and calinski
    creator.create("Individual", list, fitness=creator.Fitness)

    # set-up problem
    NDIM = 2

    def discrete_uniform(low, up, size=None):
        """
        This function creates a random distribution of the individuals
        :param low: low bound
        :param up: up bound
        :param size: none
        :return: vector with random generation of the individuals
        """
        try:
            return [random.randint(a, b) for a, b in zip(low, up)]
        except TypeError:
            return [random.randint(a, b) for a, b in zip([low] * size, [up] * size)]

    toolbox = base.Toolbox()
    toolbox.register("attr_float", discrete_uniform, BOUND_LOW, BOUND_UP, NDIM)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluation(ind):
        """
        Evaluation Function for optimization
        :param ind: individual
        :return: resulting fitness value for the three objectives of the analysis.
        """
        s = SAX(ind[0], ind[1])
        sax = [s.to_letter_rep(array)[0] for array in data]
        accurracy = calc_gain(sax)
        complexity = calc_complexity(sax)
        compression = calc_num_cutpoints(ind[0], time_series_len)
        f1 = 0.7*accurracy - 0.2*complexity - 0.1*compression
        f2 = silhouette_score(data, sax) #metrics.calinski_harabaz_score(data, sax)
        return f1, f2

    toolbox.register("evaluate", evaluation)
    toolbox.register("mate", tools.cxTwoPoint)#tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)#
    toolbox.register("mutate", tools.mutUniformInt ,low=BOUND_LOW, up=BOUND_UP, indpb=1.0/NDIM)#tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM)#
    toolbox.register("select", tools.selNSGA2)

    # run optimization
    pop, halloffame, paretofrontier, stats = main_opt(locator, toolbox, NGEN, MU, CXPB, start_gen)

    return pop, halloffame, paretofrontier, stats


#++++++++++++++++++++++++++
#Printing option
#++++++++++++++++++++++++++


def print_pareto(pop, paretofrontier):
    """
    plot front and pareto-optimal forntier
    :param pop: population of generation to check
    :param paretoprontier:
    :return:
    """
    #forntiers
    front = np.array([list(ind.fitness.values) for ind in pop])
    optimal_front = np.array([list(ind.fitness.values) for ind in paretofrontier])

    # text
    n = [str(ind) for ind in paretofrontier]
    fig, ax = plt.subplots()
    ax.scatter(optimal_front[:, 0], optimal_front[:, 1], c="r")
    ax.scatter(front[:,0], front[:,1], c="b")
    for i, txt in enumerate(n):
        ax.annotate(txt, (optimal_front[i][0], optimal_front[i][1]))
    plt.axis("tight")
    plt.show()
    return

#++++++++++++++++++++++++++++
# Main optimizaiton routine
# ++++++++++++++++++++++++++++

def main_opt(locator, toolbox, NGEN = 100, MU = 100, CXPB = 0.9, start_gen=None, seed = None):
    """
    main optimization call which provides the cross-over and mutation generation after generation
    this script is based on the example of the library DEAP of python and the algortighm NSGA-II
    :param toolbox: toolbox generated with evaluation, selection, mutation and crossover functions
    :param NGEN: number of maximum generations
    :param MU: number of initial individuals
    :param CXPB: level of confidence
    :param seed: seed.
    :return: pop = population with fitness values and individuals, stats = statistics of the population for the last
                    generation
    """
    random.seed(seed)
    if start_gen:
        print start_gen
        # A file name has been given, then load the data from the file
        with open(locator.get_calibration_cluster_opt_checkpoint(start_gen), "rb") as cp_file:
            cp = pickle.load(cp_file)
            pop = cp["population"]
            start_gen = cp["generation"]
            halloffame = cp["halloffame"]
            paretofrontier = cp["paretofrontier"]
            logbook = cp["logbook"]
            random.set_state(cp["rndstate"])
    else:
        # Start a new evolution
        pop = toolbox.population(n=MU)
        start_gen = 1
        halloffame = tools.HallOfFame(maxsize=3)
        paretofrontier = tools.ParetoFront()
        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))

    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(start_gen, NGEN+1):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # update the hall of fame and pareto
        halloffame.update(pop)
        paretofrontier.update(pop)

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

        FREQ = 1 # frequence of storage
        if gen % FREQ == 0:

            # Fill the dictionary using the dict(key=value[, ...]) constructor
            cp = dict(population=pop, generation=gen, halloffame=halloffame, paretofrontier=paretofrontier,
                      logbook=logbook, rndstate=random.get_state())

            with open(locator.get_calibration_cluster_opt_checkpoint(gen), "wb") as cp_file:
                pickle.dump(cp, cp_file)

        print("hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))
        print("Convergence: ", convergence(pop, paretofrontier))
        print("Diversity: ", diversity(pop, paretofrontier[0], paretofrontier[-1]))

    return pop, halloffame, paretofrontier, stats



#++++++++++++++++++++++++++++
# Evaluation functions
# ++++++++++++++++++++++++++++


def calc_complexity(clusters_names):
    """
    Calculated according to 'Application of time series discretization using evolutionary programming for classification
    of precancerous cervical lesions' by H. Acosta-Mesa et al., 2014
    :param clusters_names: list containing a word which clusters the time series. e.g., ['abcffs', dddddd'...'svfdab']
    :return: level of complexity which penalizes the objective function
    """
    single_words_length = len(set(clusters_names))
    m = len(clusters_names) # number of observations
    C = 1 # number of classes is 1
    result = (single_words_length - C)/ (m+ C)
    return result

def calc_num_cutpoints(wordSize, time_series_len=24):
    """
    Calculated according to 'Application of time series discretization using evolutionary programming for classification
    of precancerous cervical lesions' by H. Acosta-Mesa et al., 2014
    :param wordSize: wordsize chossen for the SAX algorithm. integer.
    :param time_series_len: length of time_series group. integer
    :return: level of compression which penalizes the objective function
    """
    result = wordSize/(2*time_series_len) # 24 hours
    return result

def calc_entropy(clusters_names):
    """
    Calculated according to 'Application of time series discretization using evolutionary programming for classification
    of precancerous cervical lesions' by H. Acosta-Mesa et al., 2014
    :param clusters_names: list containing a word which clusters the time series. e.g., ['abcffs', dddddd'...'svfdab']
    :return:
    """
    single_words = list(set(clusters_names))
    n_clusters = len(clusters_names)
    entropy = 0
    for single_word in single_words:
        pi = clusters_names.count(single_word)/n_clusters
        entropy += -pi*math.log(pi, 2)
    return entropy

def calc_gain(clusters_names):
    """
    Calculated according to the value of information gain of "Discretization of Time Series Dataset
    with a Genetic Search' by D. Garcia-Lopez1 and H. Acosta-Mesa 2009.
    :param clusters_names: list containing a word which clusters the time series. e.g., ['abcffs', dddddd'...'svfdab']
    :return: gain = information gain [real]
    """
    single_words = list(set(clusters_names))
    n_clusters = len(clusters_names)
    entropy = 0

    for single_word in single_words:
        pi = clusters_names.count(single_word)/n_clusters
        entropy += -pi*math.log(pi, 2)

    entropy_values = 0
    all_values = ''.join(clusters_names)
    all_values_len = len(all_values)
    single_letters = list(set(all_values))

    for value in single_letters:
        value_in_clusters = len([s for s in clusters_names if value in s])
        pi = all_values.count(value)/ all_values_len
        entropy_values +=  value_in_clusters/n_clusters * -pi*math.log(pi, 2)
    gain = entropy - entropy_values
    return gain