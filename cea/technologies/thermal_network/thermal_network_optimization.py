"""
hydraulic network
"""

from __future__ import division
import cea.technologies.thermal_network.thermal_network_matrix as thermal_network_matrix
from cea.technologies.thermal_network.network_layout.main import network_layout as network_layout
import cea.optimization.distribution.network_opt_main as network_opt
import cea.technologies.pumps as pumps
from cea.optimization.prices import Prices as Prices
import cea.config
import cea.globalvar
import cea.inputlocator
import cea.technologies.cogeneration as chp
import cea.technologies.chiller_vapor_compression as VCCModel
from cea.optimization.constants import PUMP_ETA

import pandas as pd
import numpy as np
import time
import operator
import random

__author__ = "Lennart Rogenhofer"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Lennart Rogenhofer"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


class Optimize_Network(object):
    """
    Storage of information for the network currently being calculated.
    """

    def __init__(self, locator, config, network_type, gv):
        self.locator = locator
        self.config = config
        self.network_type = network_type

        self.network_name = ''
        self.cost_storage = None
        self.building_names = None
        self.number_of_buildings = 0
        self.gv = gv
        self.prices = None
        self.network_features = None
        self.layout = 0
        self.has_loops = None
        self.populations = {}
        self.all_individuals = None
        self.generation_number = 0
        self.building_index = []
        self.individual_number = 0
        self.disconnected_buildings_index = []

        self.full_heating_systems = ['ahu', 'aru', 'shu', 'ww']
        self.full_cooling_systems = ['ahu', 'aru',
                                     'scu']  # Todo: add 'data', 're' here once the are available disconnectedly


def calc_Ctot_pump_netw(optimal_network):
    """
    Computes the total pump investment and operational cost, slightly adapted version of original in optimization main script.
    :type optimal_network: class storing network information
    :returns Capex_aannulized pump capex
    :returns pumpCosts: pumping cost, operational
    """
    network_type = optimal_network.config.thermal_network.network_type

    # read in node mass flows
    df = pd.read_csv(optimal_network.locator.get_node_mass_flow_csv_file(network_type, ''), index_col=0)
    mdotA_kgpers = np.array(df)
    mdotnMax_kgpers = np.amax(mdotA_kgpers)  # find highest mass flow of all nodes at all timesteps (should be at plant)

    # read in total pressure loss in kW
    deltaP_kW = pd.read_csv(optimal_network.locator.get_ploss('', network_type))
    deltaP_kW = deltaP_kW['pressure_loss_total_kW'].sum()
    # calculate pumping coo pressure losses
    pumpCosts = deltaP_kW * optimal_network.prices.ELEC_PRICE

    if optimal_network.config.thermal_network.network_type == 'DH':
        deltaPmax = np.max(optimal_network.network_features.DeltaP_DHN)
    else:
        deltaPmax = np.max(optimal_network.network_features.DeltaP_DCN)

    Capex_a, Opex_fixed = pumps.calc_Cinv_pump(2 * deltaPmax, mdotnMax_kgpers, PUMP_ETA, optimal_network.config,
                                               optimal_network.locator, 'PU1')  # investment of Machinery
    pumpCosts += Opex_fixed

    return Capex_a, pumpCosts


def network_cost_calculation(newMutadedGen, optimal_network):
    """
    Main function which calls the objective function and stores values
    :param newMutadedGen: List containg all individuals of this generation
    :param optimal_network: Object containing information of current network
    :return: List of sorted tuples, lowest cost first. Each tuple consits of the cost, followed by the individual as a string
    """
    # initialize datastorage and counter
    population_performance = {}
    optimal_network.individual_number = 0
    outputs = pd.DataFrame(np.zeros((optimal_network.config.thermal_network_optimization.number_of_individuals, 9)))
    outputs.columns = ['individual', 'capex', 'opex', 'total', 'plant_location', 'number_of_plants', 'supplied_loads',
                       'disconnected_buildings', 'has_loops']
    # iterate through all individuals
    for individual in newMutadedGen:
        # verify that we have not previously evaluated this individual, saves time!
        if not str(individual) in optimal_network.populations.keys():
            optimal_network.populations[str(individual)] = {}
            # output which buildings have plants in this individual
            optimal_network.building_index = [i for i, x in enumerate(individual[6:]) if x == 1]
            optimal_network.disconnected_buildings_index = [i for i, x in enumerate(individual[6:]) if x == 2]
            print 'Individual number: ', optimal_network.individual_number
            print 'Individual: ', individual
            print 'With ', int(individual[6:].count(1.0)), ' plant(s) at building(s): '
            building_plants = []
            for building in optimal_network.building_index:
                building_plants.append(optimal_network.building_names[building])
                print optimal_network.building_names[building]
            print 'With ', int(individual[6:].count(2.0)), ' disconnected building(s): '
            disconnected_buildings = []
            for building in optimal_network.disconnected_buildings_index:
                disconnected_buildings.append(optimal_network.building_names[building])
                print optimal_network.building_names[building]
            # check if we have loops or not
            if individual[5] == 1:
                optimal_network.has_loops = True
                print 'Network has loops.'
            else:
                optimal_network.has_loops = False
                print 'Network does not have loops.'
            if optimal_network.config.thermal_network_optimization.optimize_network_loads:
                # supplied demands
                heating_systems = []
                cooling_systems = []
                if optimal_network.config.thermal_network.network_type == 'DH':
                    heating_systems = optimal_network.config.thermal_network.substation_heating_systems  # placeholder until DH disconnected is available
                #    for index in range(5):
                #        if individual[int(index)] == 1:
                #            heating_systems.append(optimal_network.full_heating_systems[int(index)])
                else:  # DC mode
                    for index in range(5):
                        if individual[int(index)] == 1:
                            cooling_systems.append(optimal_network.full_cooling_systems[int(index)])
                optimal_network.config.thermal_network.substation_heating_systems = heating_systems
                optimal_network.config.thermal_network.substation_cooling_systems = cooling_systems
            # evaluate fitness function
            total_cost, capex, opex = fitness_func(optimal_network)
            # save total cost to dictionary
            population_performance[total_cost] = individual

            if optimal_network.config.thermal_network.network_type == 'DH':
                load_string = optimal_network.config.thermal_network.substation_heating_systems
            else:
                load_string = optimal_network.config.thermal_network.substation_cooling_systems
            # store values
            optimal_network.populations[str(individual)]['total'] = total_cost
            optimal_network.populations[str(individual)]['capex'] = capex
            optimal_network.populations[str(individual)]['opex'] = opex
            optimal_network.populations[str(individual)]['number_of_plants'] = individual[6:].count(1.0)
            optimal_network.populations[str(individual)]['has_loops'] = individual[5]
            optimal_network.populations[str(individual)]['plant_buildings'] = building_plants
            optimal_network.populations[str(individual)]['disconnected_buildings'] = disconnected_buildings
            optimal_network.populations[str(individual)]['supplied_loads'] = load_string
        else:
            # we have previously evaluated this individual so we can just read in the total cost
            total_cost = optimal_network.populations[str(individual)]['total']
            while total_cost in population_performance.keys(): #make sure we keep correct number of individuals in the extremely unlikely event that two individuals have the same cost
                total_cost = total_cost + 0.01
            population_performance[total_cost] = individual

        outputs.ix[optimal_network.individual_number]['capex'] = optimal_network.populations[str(individual)][
            'capex']
        outputs.ix[optimal_network.individual_number]['opex'] = optimal_network.populations[str(individual)]['opex']
        outputs.ix[optimal_network.individual_number]['total'] = optimal_network.populations[str(individual)][
            'total']
        outputs.ix[optimal_network.individual_number]['number_of_plants'] = individual[6:].count(1.0)
        outputs.ix[optimal_network.individual_number]['has_loops'] = individual[5]

        optimal_network.individual_number += 1

    # the following is a very tedious workaround that allows to store strings in the output dataframe.
    # Todo: find a better way
    individual_number = 0.0
    for individual in newMutadedGen:
        outputs.ix[individual_number]['individual'] = individual_number
        outputs.ix[individual_number]['supplied_loads'] = individual_number + 100.0
        outputs.ix[individual_number]['plant_location'] = individual_number + 200.0
        outputs.ix[individual_number]['disconnected_buildings'] = individual_number + 300.0
        individual_number += 1
    outputs['individual'] = outputs['individual'].astype(str)
    outputs['supplied_loads'] = outputs['supplied_loads'].astype(str)
    outputs['plant_location'] = outputs['plant_location'].astype(str)
    outputs['disconnected_buildings'] = outputs['disconnected_buildings'].astype(str)
    individual_number = 0.0
    for individual in newMutadedGen:
        outputs.replace(str(float(individual_number)), str(individual), inplace=True)
        outputs.replace(str(float(individual_number + 100)), str(''.join(optimal_network.populations[str(individual)]['supplied_loads'])), inplace=True)
        outputs.replace(str(float(individual_number + 200)), str(''.join(optimal_network.populations[str(individual)]['plant_buildings'])), inplace=True)
        outputs.replace(str(float(individual_number + 300)), str(''.join(optimal_network.populations[str(individual)]['disconnected_buildings'])), inplace=True)
        individual_number += 1
    # write cost storage to csv
    # output results file to csv
    outputs.to_csv(
        optimal_network.locator.get_optimization_network_generation_results_file(optimal_network.network_type,
                                                                                 optimal_network.generation_number))
    optimal_network.generation_number += 1
    return sorted(population_performance.items(), key=operator.itemgetter(0))


def fitness_func(optimal_network):
    """
    Calculates the cost of the given individual.
    :param optimal_network: Object storing network information.
    :return: total cost, opex and capex of my individual
    """
    # convert indices into building names
    building_names = []
    disconnected_building_names = []
    for building in optimal_network.building_index:
        building_names.append(optimal_network.building_names[building])
    if optimal_network.config.thermal_network_optimization.optimize_building_connections:
        for building in optimal_network.disconnected_buildings_index:
            disconnected_building_names.append(optimal_network.building_names[building])
    # if we want to optimize whether or not we will use loops, we need to overwrite this flag of the config file
    if optimal_network.config.thermal_network_optimization.optimize_loop_branch:
        if optimal_network.has_loops:
            optimal_network.config.network_layout.allow_looped_networks = True
        else:
            optimal_network.config.network_layout.allow_looped_networks = False
    optimal_network.config.thermal_network.disconnected_buildings = disconnected_building_names
    # create the network specified by the individual
    network_layout(optimal_network.config, optimal_network.locator, building_names,
                   optimization_flag=True)
    # run the thermal_network_matrix
    thermal_network_matrix.main(optimal_network.config)

    ## Cost calculations
    optimal_network.prices = Prices(optimal_network.locator, optimal_network.config)
    optimal_network.network_features = network_opt.network_opt_main(optimal_network.config,
                                                                    optimal_network.locator)
    # calculate Network costs
    # maintenance of network neglected, see Documentation Master Thesis Lennart Rogenhofer
    if optimal_network.network_type == 'DH':
        Capex_a_netw = optimal_network.network_features.pipesCosts_DHN
    else:
        Capex_a_netw = optimal_network.network_features.pipesCosts_DCN
    # calculate Pressure loss and Pump costs
    Capex_a_pump, Opex_fixed_pump = calc_Ctot_pump_netw(optimal_network)
    # read in plant heat requirement
    plant_heat_kWh = pd.read_csv(optimal_network.locator.get_optimization_network_layout_plant_heat_requirement_file(
        optimal_network.network_type, optimal_network.network_name))
    plant_heat_kWh = sum(
        plant_heat_kWh.abs().sum().values)  # looks horrible but basically just makes sure we sum over both axis for the case of several plants

    if plant_heat_kWh > 0:
        # calculate Heat loss costs
        if optimal_network.network_type == 'DH':
            # Assume a COP of 1.5 e.g. in CHP plant
            Opex_heat = (plant_heat_kWh) / 1.5 * optimal_network.prices.ELEC_PRICE
            Capex_a_heat, Opex_a_plant = chp.calc_Cinv_CCGT(plant_heat_kWh, optimal_network.locator,
                                                            optimal_network.config, technology=0)
        else:
            # Assume a COp of 4 e.g. brine centrifugal chiller @ Marina Bay
            # [1] Hida Y, Shibutani S, Amano M, Maehara N. District Cooling Plant with High Efficiency Chiller and Ice
            # Storage System. Mitsubishi Heavy Ind Ltd Tech Rev 2008;45:37 to 44.
            Opex_heat = (plant_heat_kWh) / 3.3 * optimal_network.prices.ELEC_PRICE
            Capex_a_heat, Opex_a_plant = VCCModel.calc_Cinv_VCC(plant_heat_kWh, optimal_network.locator,
                                                                optimal_network.config, 'CH3')

    if optimal_network.config.thermal_network_optimization.optimize_network_loads:
        dis_total, dis_opex, dis_capex = disconnected_loads_cost(optimal_network)
    else:
        dis_capex = 0.0
        dis_opex = 0.0
        dis_total = 0.0

    if optimal_network.config.thermal_network_optimization.optimize_building_connections:
        dis_build_total, dis_build_opex, dis_build_capex = disconnected_buildings_cost(optimal_network)
    else:
        dis_build_capex = 0.0
        dis_build_opex = 0.0
        dis_build_total = 0.0

    # store results
    optimal_network.cost_storage.ix['capex'][
        optimal_network.individual_number] = Capex_a_netw + Capex_a_pump + dis_capex + dis_build_capex + Capex_a_heat
    optimal_network.cost_storage.ix['opex'][
        optimal_network.individual_number] = Opex_fixed_pump + Opex_heat + dis_opex + dis_build_opex + Opex_a_plant
    optimal_network.cost_storage.ix['total'][
        optimal_network.individual_number] = Capex_a_netw + Capex_a_pump + Capex_a_heat + \
                                             Opex_fixed_pump + Opex_heat + dis_total + dis_build_total + Opex_a_plant

    print 'Annualized Capex network: ', Capex_a_netw
    print 'Annualized Capex pump: ', Capex_a_pump
    print 'Annualized Capex disconnected loads: ', dis_capex
    print 'Annualized Capex disconnected buildings: ', dis_build_opex
    print 'Annualized Capex plant: ', Capex_a_heat

    print 'Annualized Opex heat: ', Opex_heat
    print 'Annualized Opex pump: ', Opex_fixed_pump
    print 'Annualized Opex disconnected loads: ', dis_opex
    print 'Annualized Opex disconnected building: ', dis_build_opex
    print 'Annualized Opex plant: ', Opex_a_plant

    return optimal_network.cost_storage.ix['total'][optimal_network.individual_number], \
           optimal_network.cost_storage.ix['capex'][optimal_network.individual_number], \
           optimal_network.cost_storage.ix['opex'][optimal_network.individual_number]


def disconnected_loads_cost(optimal_network):
    disconnected_systems = []
    ## Calculate disconnected heat load costs
    dis_opex = 0
    dis_capex = 0
    # if optimal_network.network_type == 'DH':
    # information not yet available
    '''
        for system in optimal_network.full_heating_systems:
            if system not in optimal_network.config.thermal_network.substation_heating_systems:
                disconnected_systems.append(system)
        # Make sure files to read in exist
        for system in disconnected_systems:
            for building in optimal_network.building_names:
                assert optimal_network.locator.get_optimization_disconnected_folder_building_result_heating(building), "Missing diconnected building files. Please run disconnected_buildings_heating first."
            # Read in disconnected cost of all buildings
                disconnected_cost = optimal_network.locator.get_optimization_disconnected_folder_building_result_heating(building)
    '''
    if optimal_network.network_type == 'DC':
        for system in optimal_network.full_cooling_systems:
            if system not in optimal_network.config.thermal_network.substation_cooling_systems:
                disconnected_systems.append(system)
        if len(disconnected_systems) > 0:
            # Make sure files to read in exist
            system_string = find_systems_string(disconnected_systems)
            for building_index, building in enumerate(optimal_network.building_names):
                if building_index not in optimal_network.disconnected_buildings_index:  # disconnected building, will be handeled seperately
                    assert optimal_network.locator.get_optimization_disconnected_folder_building_result_cooling(
                        building,
                        system_string), "Missing diconnected building files. Please run disconnected_buildings_cooling first."
                    # Read in disconnected cost of all buildings
                    disconnected_cost = pd.read_csv(
                        optimal_network.locator.get_optimization_disconnected_folder_building_result_cooling(building,
                                                                                                             system_string))
                    opex_index = int(np.where(disconnected_cost['Best configuration'] == 1)[0])
                    opex = disconnected_cost['Operation Costs [CHF]'][opex_index]
                    capex = disconnected_cost['Annualized Investment Costs [CHF]'][opex_index]
                    dis_opex += opex
                    dis_capex += capex

    dis_total = dis_opex + dis_capex
    return dis_total, dis_opex, dis_capex


def disconnected_buildings_cost(optimal_network):
    disconnected_systems = []
    ## Calculate disconnected heat load costs
    dis_opex = 0
    dis_capex = 0
    # if optimal_network.network_type == 'DH':
    # information not yet available
    if len(optimal_network.disconnected_buildings_index) > 0:
        # Make sure files to read in exist
        for building_index, building in enumerate(optimal_network.building_names):
            if building_index not in optimal_network.disconnected_buildings_index:  # disconnected building, will be handeled seperately
                if optimal_network.network_type == 'DC':
                    system_string = 'AHU_ARU_SCU'
                    assert optimal_network.locator.get_optimization_disconnected_folder_building_result_cooling(
                        building,
                        system_string), "Missing diconnected building files. Please run disconnected_buildings_cooling first."
                    # Read in disconnected cost of all buildings
                    disconnected_cost = pd.read_csv(
                        optimal_network.locator.get_optimization_disconnected_folder_building_result_cooling(building,
                                                                                                             system_string))
                else:  # todo: update this once disaggregated DH loads available
                    assert optimal_network.locator.get_optimization_disconnected_folder_building_result_heating(
                        building), "Missing diconnected building files. Please run disconnected_buildings_heating first."
                    # Read in disconnected cost of all buildings
                    disconnected_cost = pd.read_csv(
                        optimal_network.locator.get_optimization_disconnected_folder_building_result_heating(
                            building))
                opex_index = int(np.where(disconnected_cost['Best configuration'] == 1)[0])
                opex = disconnected_cost['Operation Costs [CHF]'][opex_index]
                capex = disconnected_cost['Annualized Investment Costs [CHF]'][opex_index]
                dis_opex += opex
                dis_capex += capex

    dis_total = dis_opex + dis_capex
    return dis_total, dis_opex, dis_capex


def find_systems_string(disconnected_systems):
    system_string_options = ['AHU', 'ARU', 'SCU', 'AHU_ARU', 'AHU_SCU', 'ARU_SCU', 'AHU_ARU_SCU']
    if len(disconnected_systems) == 3:
        system_string = system_string_options[6]
    elif len(disconnected_systems) == 2:
        if 'ahu' in disconnected_systems:
            if 'aru' in disconnected_systems:
                system_string = system_string_options[3]
            else:
                system_string = system_string_options[4]
        else:
            system_string = system_string_options[5]
    elif len(disconnected_systems) == 1:
        if 'ahu' in disconnected_systems:
            system_string = system_string_options[0]
        elif 'aru' in disconnected_systems:
            system_string = system_string_options[1]
        else:
            system_string = system_string_options[2]
    elif len(disconnected_systems) == 0:
        system_string = ''
    else:
        print 'Error in disconnected buildings list. invalid number of elements.'
        print disconnected_systems
        print len(disconnected_systems)
        system_string = []
    return system_string


def selectFromPrevPop(sortedPrevPop, optimal_network):
    """
    Selects individuals from the previous generation for breeding and adds a predefined number of new "lucky" individuals.
    :param sortedPrevPop: List of tuples of individuals from previous generation, sorted by increasing cost
    :param optimal_network: Object storing network information.
    :return: list of individuals to breed
    """
    next_Generation = []
    # pick the individuals with the lowest cost
    for i in range(0,
                   (optimal_network.config.thermal_network_optimization.number_of_individuals - optimal_network.config.thermal_network_optimization.lucky_few)):
        print i
        print sortedPrevPop[i]
        print sortedPrevPop[i][1]
        next_Generation.append(sortedPrevPop[i][1])
    # add a predefined amount of 'fresh' individuals to the mix
    while len(next_Generation) < optimal_network.config.thermal_network_optimization.number_of_individuals:
        lucky_individual = random.choice(generateInitialPopulation(optimal_network))
        # make sure we don't have duplicates
        if lucky_individual not in next_Generation:
            next_Generation.append(lucky_individual)
    # randomize order before breeding
    random.shuffle(next_Generation)
    return next_Generation


def breedNewGeneration(selectedInd, optimal_network):
    """
    Breeds new generation for genetic algorithm. Here we don't assure that each parent is chosen at least once, but the epected value
    is that each parent should be chosen twice.
    E.g. ew have N indivduals. The chance of being parent 1 is 1/N, the chance of being parent 2 is (1-1/N)*1/(N-1).
    So the probability of being one of the two parents of any child is 1/N + (1-1/N)*1/(N-1) = 2/N. Since there are N children,
    the expected value is 2.
    :param selectedInd: list of individuals to breed
    :param optimal_network: Object sotring network information
    :return: newly breeded generation
    """
    newGeneration = []
    # make sure we have the correct amount of individuals
    while len(newGeneration) < optimal_network.config.thermal_network_optimization.number_of_individuals:
        # choose random parents
        first_parent = random.choice(selectedInd)
        second_parent = random.choice(selectedInd)
        # assure that both parents are not the same individual
        while second_parent == first_parent:
            second_parent = random.choice(selectedInd)
        # setup storage for child
        child = np.zeros(len(first_parent))
        # iterate through parent individuals
        for j in range(len(first_parent)):
            # if both parents have the same value, it is passed on to the child
            if int(first_parent[j]) == int(second_parent[j]):
                child[j] = float(first_parent[j])
            else:
                # we randomly chose from which parent we inherit
                which_parent = np.random.random_integers(low=0, high=1)
                if which_parent == 0:
                    child[j] = float(first_parent[j])
                else:
                    child[j] = float(second_parent[j])
        # make sure that we do not have too many plants now
        while list(child[6:]).count(1.0) > optimal_network.config.thermal_network_optimization.max_number_of_plants:
            # find all plant indeces
            plant_indices = np.where(child == 1)[0]
            # chose a random one
            random_plant = random.choice(list(plant_indices))
            # make sure we are not overwriting the values of network layout information
            while random_plant < 6:
                random_plant = random.choice(list(plant_indices))
            if optimal_network.config.thermal_network_optimization.optimize_building_connections:
                random_choice = np.random.random_integers(low=0, high=1)
            else:
                random_choice = 0
            if random_choice == 0:
                child[int(random_plant)] = 0.0
            else:
                child[int(random_plant)] = 2.0
        # make sure we still have a non-zero amount of plants
        while list(child[6:]).count(1.0) < optimal_network.config.thermal_network_optimization.min_number_of_plants:
            # Add one plant
            # find all non plant indices
            if optimal_network.config.thermal_network_optimization.optimize_building_connections:
                random_choice = np.random.random_integers(low=0, high=1)
            else:
                random_choice = 0
            if random_choice == 0:
                indices = [i for i, x in enumerate(child) if x == 0]
            else:
                indices = [i for i, x in enumerate(child) if x == 2]
            if len(indices) > 0:
                index = int(random.choice(indices))
                while index < 6:
                    index = random.choice(list(indices))
                child[index] = 1.0
        # make sure we don't have duplicates
        if list(child) not in newGeneration:
            newGeneration.append(list(child))
    return newGeneration


def generate_plants(optimal_network, new_plants):
    """
    Generates the number of plants given in the config files at random, permissible, building locations.
    :param optimal_network: Object containing network information.
    :return: list of plant locations
    """

    # return an index at which to place plant
    # we sutract a value because here our list only contains plant/no plant information.
    # This function returns the index inside the individual, which stores more information.
    random_index = admissible_plant_location(optimal_network) - 6
    new_plants[random_index] = 1.0
    # check how many more plants we need to add (we already added one)
    number_of_plants_to_add = np.random.random_integers(
        low=optimal_network.config.thermal_network_optimization.min_number_of_plants - 1, high=(
                optimal_network.config.thermal_network_optimization.max_number_of_plants - 1))
    while list(new_plants).count(1.0) < number_of_plants_to_add + 1:
        random_index = admissible_plant_location(optimal_network) - 6
        new_plants[random_index] = 1.0
    return list(new_plants)


def disconnect_buildings(optimal_network):
    """
    Disconnects a random amount of buildings from the network. Setting the value '2' means the buliding is disconnected.
    :param optimal_network: Object containing network information.
    :param new_plants: list of plants.
    :return: list of plant locations
    """
    new_plants = np.zeros(optimal_network.number_of_buildings)
    # choose random amount, choose random locations, start disconnecting buildings
    random_amount = np.random.random_integers(low=0, high=(optimal_network.number_of_buildings - 1))
    for i in range(random_amount):
        random_index = np.random.random_integers(low=0, high=(optimal_network.number_of_buildings - 1))
        while new_plants[random_index] == 2.0:
            random_index = np.random.random_integers(low=0, high=(optimal_network.number_of_buildings - 1))
        new_plants[random_index] = 2.0
    return list(new_plants)


def admissible_plant_location(optimal_network):
    """
    This function returns a random index within the individual at which a plant is permissible.
    :param optimal_network: Object storing network information
    :return: permissible index of plant within an individual
    """
    admissible_plant_location = False
    while not admissible_plant_location:
        # generate a random index within our individual
        random_index = np.random.random_integers(low=6, high=(optimal_network.number_of_buildings + 5))
        # check if the building at this index is in our permitted building list
        if optimal_network.building_names[
            random_index - 6] in optimal_network.config.thermal_network_optimization.possible_plant_sites:
            admissible_plant_location = True
    return random_index


def generateInitialPopulation(optimal_network):
    """
    Generates the initial population for network optimization.
    :param optimal_network: Object storing network information
    :return: returns list of individuals as initial population for genetic algorithm
    """
    initialPop = []
    while len(
            initialPop) < optimal_network.config.thermal_network_optimization.number_of_individuals:  # assure we have the correct amount of individuals
        # generate list of where our plants are
        if optimal_network.config.thermal_network_optimization.optimize_building_connections:
            new_plants = disconnect_buildings(optimal_network)
        else:
            new_plants = np.zeros(optimal_network.number_of_buildings)
        new_plants = generate_plants(optimal_network, new_plants)
        if optimal_network.config.thermal_network_optimization.optimize_loop_branch:
            loop_no_loop_binary = np.random.random_integers(low=0, high=1)  # 1 means loops, 0 means no loops
        else:  # we are not optimizing this, so read from config file input
            if optimal_network.config.network_layout.allow_looped_networks:  # allow loop networks
                loop_no_loop_binary = 1.0
            else:  # branched networks only
                loop_no_loop_binary = 0.0
        # for DH: ahu, aru, shu, ww, 0.0
        # for DC: ahu, aru, scu, data, re
        if optimal_network.config.thermal_network_optimization.optimize_network_loads:
            load_type = []
            for i in range(3):
                load_type.append(float(np.random.random_integers(low=0,
                                                                 high=1)))  # create a random list of 0 or 1, indicating if heat load is supplied by network or not
                # make sure we supply at least one load, otherwise we don't have a network
                if sum(load_type) == 0:
                    random_index = np.random.random_integers(low=0, high=2)
                    load_type[random_index] = 1.0
            if optimal_network.config.thermal_network.network_type == 'DC':
                load_type[3] = 0.0  # force this to 0 since we don't have disconnected cost information for data cooling
                load_type[4] = 0.0  # force this to 0 since we don't have disconnected cost information for re cooling
            else:
                print 'Load optimization currently unavailable for DH.'
                load_type = [0.0, 0.0, 0.0, 0.0, 0.0]  # placeholder, we are not optimizing this
        else:
            load_type = [0.0, 0.0, 0.0, 0.0, 0.0]  # placeholder, we are not optimizing this
        # create individual
        new_individual = load_type + [float(loop_no_loop_binary)] + new_plants
        if new_individual not in initialPop:  # add individual to list, avoid duplicates
            initialPop.append(new_individual)
    return list(initialPop)


def mutateConnections(individual):
    """
    Mutates an individuals plant location and number of plants, making sure not to violate any constraints.
    :param individual: List containing individual information
    :param optimal_network: Object storing network information
    :return: list of mutated individual information
    """
    # make sure we have a list type
    individual = list(individual)
    # we only have one plant so we will muate this
    add_or_remove = np.random.randint(low=0, high=1)
    building_individual = individual[6:]
    other_individual = individual[0:6]
    if add_or_remove == 0:  # disconnect a building
        random_int = np.random.randint(low=0, high=1)
        index = [i for i, x in enumerate(building_individual) if x == random_int]
        if len(index) > 0:
            random_index = np.random.randint(low=0, high=len(index) - 1)
            building_individual[random_index] = 2.0
    else:  # connect a disconnected building
        index = [i for i, x in enumerate(building_individual) if x == 2]
        if len(index) > 0:
            random_index = np.random.randint(low=0, high=len(index) - 1)
            building_individual[random_index] = 0.0
    individual = other_individual + building_individual
    return list(individual)


def mutateLocation(individual, optimal_network):
    """
    Mutates an individuals plant location and number of plants, making sure not to violate any constraints.
    :param individual: List containing individual information
    :param optimal_network: Object storing network information
    :return: list of mutated individual information
    """
    # make sure we have a list type
    individual = list(individual)
    # if we only have one plant, we need mutation to behave differently
    if optimal_network.config.thermal_network_optimization.max_number_of_plants != 1:
        # check if we have too many plants
        if list(individual[6:]).count(
                1.0) >= optimal_network.config.thermal_network_optimization.max_number_of_plants:
            # remove one random plant
            indices = [i for i, x in enumerate(individual) if x == 1]
            index = int(random.choice(indices))
            # make sure we don't overwrite values that don't store plant location information
            while index < 6:
                index = int(random.choice(indices))
            individual[index] = 0.0
        # check if we have too few plants
        elif list(individual[6:]).count(
                1.0) <= optimal_network.config.thermal_network_optimization.min_number_of_plants:
            while list(individual[6:]).count(
                    1.0) <= optimal_network.config.thermal_network_optimization.min_number_of_plants:
                # Add one plant
                index = admissible_plant_location(optimal_network)
                individual[index] = 1.0
        else:
            # add or remove a plant, choose randomly
            add_or_remove = np.random.random_integers(low=0, high=1)
            if add_or_remove == 0:  # remove a plant
                indices = [i for i, x in enumerate(individual) if x == 1]
                index = int(random.choice(indices))
                # make sure we don't overwrite values that don't store plant location information
                while index < 6:
                    index = int(random.choice(indices))
                individual[index] = 0.0
            else:  # add a plant
                original_sum = sum(individual[6:])
                while sum(individual[
                          6:]) == original_sum:  # make sure we actually add a new one and don't just overwrite an existing plant
                    index = admissible_plant_location(optimal_network)
                    individual[index] = 1.0
    else:
        # we only have one plant so we will muate this
        # remove the plant
        plant_individual = individual[6:]
        other_individual = individual[0:6]
        index = [i for i, x in enumerate(plant_individual) if x == 1]
        plant_individual[int(index[0])] = 0.0
        individual = other_individual + plant_individual
        # add a new one
        index = admissible_plant_location(optimal_network)
        individual[index] = 1.0
    return list(individual)


def mutateLoad(individual, optimal_network):
    """
    Mutates an individuals type of heat loads covered by the network, making sure not to violate any constraints.
    :param individual: List containing individual information
    :param optimal_network: Object storing network information
    :return: list of mutated individual information
    """
    # make sure we have a list type
    individual = list(individual)
    # invert one random byte
    if optimal_network.network_type == 'DH':
        random_choice = np.random.random_integers(low=0, high=0)  # no disconnected cost information available
    else:
        random_choice = np.random.random_integers(low=0,
                                                  high=2)  # once disconnected cost information for data and re available increase to 4
    if individual[random_choice] == 1.0:
        individual[random_choice] = 0.0
    else:
        individual[random_choice] = 1.0
    # make sure we supply at least one load
    if sum(individual[0:5]) == 0:
        random_choice = np.random.random_integers(low=0, high=2)
        individual[random_choice] = 1.0
    return list(individual)


def mutateLoop(individual):
    """
    Mutates an individuals loop/branch information, making sure not to violate any constraints.
    :param individual: List containing individual information
    :return: list of mutated individual information
    """
    # make sure we have a list type
    individual = list(individual)
    # keep our loop or not
    keep_or_remove = np.random.random_integers(low=0, high=1)
    if keep_or_remove == 1:  # switch value
        if individual[5] == 1.0:  # loops are activated
            individual[5] = 0.0  # turn off
        else:  # branches only
            individual[5] = 1.0  # turn on loops
    return list(individual)


def mutateGeneration(newGen, optimal_network):
    """
    Checks if an individual should be mutated and calls the corresponding functions.
    :param newGen: Generation to mutate
    :param optimal_network: Object storing network information
    :return: Mutated generation
    """
    # iterate through individuals of this generation
    for i in range(len(newGen)):
        random.seed()
        # check if we should mutate
        if random.random() * 100 < optimal_network.config.thermal_network_optimization.chance_of_mutation:
            mutated_element_flag = False
            while not mutated_element_flag:
                mutated_individual = list(newGen[i])
                # apply mutation to plant location
                if optimal_network.config.thermal_network_optimization.optimize_building_connections:
                    mutated_individual = list(mutateConnections(mutated_individual))
                mutated_individual = list(
                    mutateLocation(mutated_individual, optimal_network))
                # if we optimize loop/branch layout, apply mutation here
                if optimal_network.config.thermal_network_optimization.optimize_loop_branch:
                    mutated_individual = list(mutateLoop(mutated_individual))
                if optimal_network.config.thermal_network_optimization.optimize_network_loads:
                    mutated_individual = list(mutateLoad(mutated_individual, optimal_network))
                # overwrite old individual with mutated one
                if mutated_individual not in newGen:
                    mutated_element_flag = True
                    newGen[i] = mutated_individual
    return newGen


# ============================
# test
# ============================


def main(config):
    """
    runs an optimization calculation for the plant location in the thermal network.
    """
    # output configuration information
    print('Running thermal_network optimization for scenario %s' % config.scenario)
    print 'Number of individuals: ', config.thermal_network_optimization.number_of_individuals
    print 'Number of generations: ', config.thermal_network_optimization.number_of_generations
    print 'Number of lucky few individuals: ', config.thermal_network_optimization.lucky_few
    print 'Percentage chance of mutation: ', config.thermal_network_optimization.chance_of_mutation
    print 'Number of plants between ', config.thermal_network_optimization.min_number_of_plants, ' and ', config.thermal_network_optimization.max_number_of_plants
    if config.thermal_network_optimization.possible_plant_sites:
        print 'Possible plant locations: ', config.thermal_network_optimization.possible_plant_sites
    else:
        print 'Possible plant locations: all'
    print 'Optimize loop / no loops is set to: ', config.thermal_network_optimization.optimize_loop_branch
    print 'Optimize supplied thermal loads is set to: ', config.thermal_network_optimization.optimize_network_loads
    print 'Optimize which buildings are connected is set to: ', config.thermal_network_optimization.optimize_building_connections

    start = time.time()
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    gv = cea.globalvar.GlobalVariables()
    network_type = config.thermal_network.network_type
    # overwrite network layout file to make it matc the network type
    config.network_layout.network_type = network_type
    # initialize object
    optimal_network = Optimize_Network(locator, config, network_type, gv)
    # readin basic information and save to object
    total_demand = pd.read_csv(locator.get_total_demand())
    optimal_network.building_names = total_demand.Name.values
    optimal_network.number_of_buildings = total_demand.Name.count()

    # list of possible plant location sites
    if not config.thermal_network_optimization.possible_plant_sites:
        config.thermal_network_optimization.possible_plant_sites = optimal_network.building_names

    # initialize data storage
    optimal_network.cost_storage = pd.DataFrame(
        np.zeros((3, optimal_network.config.thermal_network_optimization.number_of_individuals)))
    optimal_network.cost_storage.index = ['capex', 'opex', 'total']

    # load initial population
    print 'Creating initial population.'
    newMutadedGen = generateInitialPopulation(optimal_network)
    # iterate through number of generations
    for generation_number in range(optimal_network.config.thermal_network_optimization.number_of_generations):
        print 'Running optimization for generation number ', generation_number
        # calculate network cost for each individual and sort by increasing cost
        sortedPop = network_cost_calculation(newMutadedGen, optimal_network)
        print 'Lowest cost individual: ', sortedPop[0], '\n'
        print len(sortedPop)
        # setup next generation
        if generation_number < optimal_network.config.thermal_network_optimization.number_of_generations - 1:
            # select individuals for next generation
            selectedPop = selectFromPrevPop(sortedPop, optimal_network)
            # breed next generation
            newGen = breedNewGeneration(selectedPop, optimal_network)
            # add mutations
            newMutadedGen = mutateGeneration(newGen, optimal_network)

    # write values into storage dataframe and ouput results
    # setup data frame with generations, individual, opex, capex and total cost
    optimal_network.all_individuals = pd.DataFrame(np.zeros((
        len(optimal_network.populations.keys()), 9)))
    optimal_network.all_individuals.columns = ['individual', 'opex', 'capex', 'total cost', 'plant_buildings',
                                               'number_of_plants', 'supplied_loads', 'disconnected_buildings', 'has_loops']
    row_number = 0
    for individual in optimal_network.populations.keys():
        optimal_network.all_individuals.ix[row_number]['opex'] = optimal_network.populations[str(individual)][
            'opex']
        optimal_network.all_individuals.ix[row_number]['capex'] = optimal_network.populations[str(individual)][
            'capex']
        optimal_network.all_individuals.ix[row_number]['total cost'] = \
            optimal_network.populations[str(individual)]['total']
        optimal_network.all_individuals.ix[row_number]['number_of_plants'] = \
        optimal_network.populations[str(individual)][
            'number_of_plants']
        optimal_network.all_individuals.ix[row_number]['has_loops'] = \
        optimal_network.populations[str(individual)][
            'has_loops']
        row_number += 1
    # the following is a tedious workaround necessary to write string values into the dataframe and to csv..
    # todo: improve this
    row_number = 0
    for individual in optimal_network.populations.keys():
        optimal_network.all_individuals.ix[row_number]['individual'] = row_number
        optimal_network.all_individuals.ix[row_number]['plant_buildings'] = row_number + 100.0
        optimal_network.all_individuals.ix[row_number]['disconnected_buildings'] = row_number + 200.0
        optimal_network.all_individuals.ix[row_number]['supplied_loads'] = row_number + 300.0
        row_number += 1
    row_number = 0
    optimal_network.all_individuals['individual'] = \
        optimal_network.all_individuals['individual'].astype(str)
    optimal_network.all_individuals['plant_buildings'] = \
        optimal_network.all_individuals['plant_buildings'].astype(str)
    optimal_network.all_individuals['disconnected_buildings']= \
        optimal_network.all_individuals['disconnected_buildings'].astype(str)
    optimal_network.all_individuals['supplied_loads'] = \
        optimal_network.all_individuals['supplied_loads'].astype(str)
    for individual in optimal_network.populations.keys():
        optimal_network.all_individuals.replace(str(float(row_number + 100)),
                                               ''.join(optimal_network.populations[str(individual)][
                                                        'plant_buildings']), inplace=True)
        optimal_network.all_individuals.replace(str(float(row_number + 200)),
                                                ''.join(optimal_network.populations[str(individual)][
                                                        'disconnected_buildings']), inplace=True)
        optimal_network.all_individuals.replace(str(float(row_number + 300)),
                                                ''.join(optimal_network.populations[str(individual)][
                                                        'supplied_loads']), inplace=True)
        optimal_network.all_individuals.replace(str(float(row_number)), str(individual), inplace=True)
        row_number += 1

    optimal_network.all_individuals.to_csv(
        optimal_network.locator.get_optimization_network_all_individuals_results_file(optimal_network.network_type),
        index='False')

    print('thermal_network_optimization_main() succeeded')
    print('total time: ', time.time() - start)


if __name__ == '__main__':
    main(cea.config.Configuration())
