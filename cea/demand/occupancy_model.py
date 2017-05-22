"""
Query schedules according to database
"""

# HISTORY
# J. Fonseca  script development          26.08.2015
# D. Thomas   documentation               10.08.2016

from __future__ import division
import pandas as pd
import numpy as np

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Daren Thomas", "Martin Mosteiro-Romero"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def calc_schedules(list_uses, archetype_schedules, bpr, archetype_values):
    """
    Given schedule data for archetypical building uses, `calc_schedule` calculates the schedule for a building
    with possibly a mixed schedule as defined in `building_uses` using a weighted average approach. The schedules are
    normalized such that the final demands and internal gains are calculated from the specified building properties and
    not the archetype values.

    The script generates the following scheduleS:
        'people': number of people per square meter at each hour (in p)
        've': ventilation demand (in p^-1 since the ventilation demand is then calculated as schedule * lpd)
        'Qs': sensible heat gain due to occupancy (in p^-1 since the heat gains are calculated as schedule * W/p)
        'X': moisture gain due to occupants (in p^-1 since the gains are calculated as schedule * ghp)
        'Ea': electricity demand for appliances at each hour (unitless)
        'El': electricity demand for lighting at each hour (unitless)
        'Epro': electricity demand for process at each hour (unitless)
        'Ere': electricity demand for refrigeration at each hour (unitless)
        'Ed': electricity demand for data centers at each hour (unitless)
        'Vww': domestic hot water demand at each hour (in p^-1 since the demand is calculated as schedule * lpd)
        'Vw': total water demand at each hour (in p^-1 since the demand is calculated as schedule * lpd)

    :param list_uses: The list of uses used in the project
    :type list_uses: list

    :param archetype_schedules: The list of schedules defined for the project - in the same order as `list_uses`
    :type archetype_schedules: list[ndarray[float]]

    :param bpr: 
    :type bpr: 

	:param archetype_values:
	:type archetype_values:

    :returns schedules: a dictionary containing the weighted average schedule for: occupancy; ventilation demand;
    sensible heat and moisture gains due to occupancy; electricity demand for appliances, lighting, processes,
    refrigeration and data centers; demand for water and domestic hot water
    :rtype: dict[array]
    """

    # set up schedules to be defined and empty dictionary
    schedule_labels = ['people', 've', 'Qs', 'X', 'Ea', 'El', 'Epro', 'Ere', 'Ed', 'Vww', 'Vw']
    schedules = {}

    # define the archetypical schedule type to be used for the creation of each schedule: 0 for occupancy, 1 for
    # electricity use, 2 for domestic hot water consumption, 3 for processes
    schedule_code_dict = {'people': 0, 've': 0, 'Qs': 0, 'X': 0, 'Ea': 1, 'El': 1, 'Ere': 1, 'Ed': 1, 'Vww': 2,
                          'Vw': 2, 'Epro': 3}

    # define function to calculated the weighted average of schedules
    def calc_average(last, current, share_of_use):
        return last + current * share_of_use

    for label in schedule_labels:
        # each schedule is defined as (sum of schedule[i]*X[i]*share_of_area[i])/(sum of X[i]*share_of_area[i]) for each
        # variable X and occupancy type i
        code = schedule_code_dict[label]
        current_schedule = np.zeros(8760)
        normalizing_value = 0
        current_archetype_values = archetype_values[label]
        for num in range(len(list_uses)):
            if current_archetype_values[num] != 0: # do not consider when the value is 0
                current_share_of_use = bpr.occupancy[list_uses[num]]
                # variables that depend on the number of people need to be adjusted by the number of people
                if label in ['ve','Qs','X','Vww','Vw']:
                    share_time_occupancy_density = (current_archetype_values[num] * archetype_values['people'][num]) * \
                                                   current_share_of_use
                else: share_time_occupancy_density = (current_archetype_values[num]) * current_share_of_use
                current_schedule = np.vectorize(calc_average)(current_schedule, archetype_schedules[num][code],
                                                              share_time_occupancy_density)
                normalizing_value += current_share_of_use * current_archetype_values[num]

        schedules[label] = current_schedule / normalizing_value

    return schedules

# read schedules from excel file
def schedule_maker(dates, locator, list_uses):
    """
    Reads schedules from the archetype schedule Excel file along with the corresponding internal loads and ventilation
    demands.

    :param dates: dates and times throughout the year
    :type dates: DatetimeIndex
    :param locator: an instance of InputLocator set to the scenario
    :type locator: InputLocator
    :param list_uses: list of occupancy types used in the scenario
    :type list_uses: list

    :return schedules: yearly schedule for each occupancy type used in the project
    :type schedules: list[tuple]
    :return occ_densities: occupant density in people per square meter for each occupancy type used in the project
    :type occ_densities: list[float]
    :return internal_loads: dictionary containing the internal loads for each occupancy type used in the project
    :type internal_loads: dict[list[float]]
    :return ventilation: ventilation demand for each occupancy type used in the project
    :type ventilation: list[float]
    """

    def get_yearly_vectors(dates, occ_schedules, el_schedules, dhw_schedules, pro_schedules, month_schedule):
        """
        For a given use type, this script generates yearly schedules for occupancy, electricity demand,
        hot water demand, process electricity demand based on the daily and monthly schedules obtained from the
        archetype database.

        :param dates: dates and times throughout the year
        :type dates: DatetimeIndex
        :param occ_schedules: occupancy schedules for a weekdays, Saturdays and Sundays from the archetype database
        :type occ_schedules: list[array]
        :param el_schedules: electricity schedules for a weekdays, Saturdays and Sundays from the archetype database
        :type el_schedules: list[array]
        :param dhw_schedules: domestic hot water schedules for a weekdays, Saturdays and Sundays from the archetype
        database
        :type dhw_schedules: list[array]
        :param pro_schedules: process electricity schedules for a weekdays, Saturdays and Sundays from the archetype
        database
        :type pro_schedules: list[array]
        :param month_schedule: monthly schedules from the archetype database
        :type month_schedule: ndarray

        :return occ: occupancy schedule for each hour of the year
        :type occ: list[float]
        :return el: electricity schedule for each hour of the year
        :type el: list[float]
        :return dhw: domestic hot water schedule for each hour of the year
        :type dhw: list[float]
        :return pro: process electricity schedule for each hour of the year
        :type pro: list[float]

        """

        occ = []
        el = []
        dhw = []
        pro = []

        if dhw_schedules[0].sum() != 0:
            dhw_weekday_max = dhw_schedules[0].sum() ** -1
        else: dhw_weekday_max = 0

        if dhw_schedules[1].sum() != 0:
            dhw_sat_max = dhw_schedules[1].sum() ** -1
        else: dhw_sat_max = 0

        if dhw_schedules[2].sum() != 0:
            dhw_sun_max = dhw_schedules[2].sum() ** -1
        else: dhw_sun_max = 0

        for date in dates:
            month_year = month_schedule[date.month - 1]
            hour_day = date.hour
            dayofweek = date.dayofweek
            if 0 <= dayofweek < 5:  # weekday
                occ.append(occ_schedules[0][hour_day] * month_year)
                el.append(el_schedules[0][hour_day] * month_year)
                dhw.append(dhw_schedules[0][hour_day] * month_year * dhw_weekday_max) # normalized dhw demand flow rates
                pro.append(pro_schedules[0][hour_day] * month_year)
            elif dayofweek is 5:  # saturday
                occ.append(occ_schedules[1][hour_day] * month_year)
                el.append(el_schedules[1][hour_day] * month_year)
                dhw.append(dhw_schedules[1][hour_day] * month_year * dhw_sat_max) # normalized dhw demand flow rates
                pro.append(pro_schedules[1][hour_day] * month_year)
            else:  # sunday
                occ.append(occ_schedules[2][hour_day] * month_year)
                el.append(el_schedules[2][hour_day] * month_year)
                dhw.append(dhw_schedules[2][hour_day] * month_year * dhw_sun_max) # normalized dhw demand flow rates
                pro.append(pro_schedules[2][hour_day] * month_year)

        return occ, el, dhw, pro

    schedules = []
    occ_densities = []
    archetypes_internal_loads = pd.read_excel(locator.get_archetypes_properties(), 'INTERNAL_LOADS').set_index('Code')
    Qs_Wm2 = []
    X_ghm2 = []
    Ea_Wm2 = []
    El_Wm2 = []
    Epro_Wm2 = []
    Ere_Wm2 = []
    Ed_Wm2 = []
    Vww_ldm2 = []
    Vw_ldm2 = []
    archetypes_indoor_comfort = pd.read_excel(locator.get_archetypes_properties(), 'INDOOR_COMFORT').set_index('Code')
    Ve_lsm2 = []
    for use in list_uses:
        # Read from archetypes_schedules and properties
        archetypes_schedules = pd.read_excel(locator.get_archetypes_schedules(), use).T

        # read lists of every daily profile
        occ_schedules, el_schedules, dhw_schedules, pro_schedules, month_schedule, \
        area_per_occupant = read_schedules(use, archetypes_schedules)

        # get occupancy density per schedule in a list
        if area_per_occupant != 0:
            occ_densities.append(1/area_per_occupant)
        else: occ_densities.append(area_per_occupant)

        # get internal loads per schedule in a list
        Ea_Wm2.append(archetypes_internal_loads['Ea_Wm2'][use])
        El_Wm2.append(archetypes_internal_loads['El_Wm2'][use])
        Epro_Wm2.append(archetypes_internal_loads['Epro_Wm2'][use])
        Ere_Wm2.append(archetypes_internal_loads['Ere_Wm2'][use])
        Ed_Wm2.append(archetypes_internal_loads['Ed_Wm2'][use])
        ## variables that were defined per person are converted to per square meter occupied, the occupancy effect is
        ## accounted for when multiplying by the occupancy schedule later on
        if area_per_occupant > 0:   # do not consider if occupant density is 0
            Qs_Wm2.append(archetypes_internal_loads['Qs_Wp'][use] / area_per_occupant)
            X_ghm2.append(archetypes_internal_loads['X_ghp'][use] / area_per_occupant)
            Vww_ldm2.append(archetypes_internal_loads['Vww_lpd'][use] / area_per_occupant)
            Vw_ldm2.append(archetypes_internal_loads['Vw_lpd'][use] / area_per_occupant)
        else:
            Qs_Wm2.append(0)
            X_ghm2.append(0)
            Vww_ldm2.append(0)
            Vw_ldm2.append(0)

        # get ventilation required per schedule in a list
        if area_per_occupant > 0:   # do not consider if occupant density is 0
            Ve_lsm2.append(archetypes_indoor_comfort['Ve_lps'][use] / area_per_occupant)
        else: Ve_lsm2.append(0)

        # get yearly schedules in a list
        schedule = get_yearly_vectors(dates, occ_schedules, el_schedules, dhw_schedules, pro_schedules, month_schedule)
        schedules.append(schedule)

    archetype_values = {'people': occ_densities, 'Qs': Qs_Wm2, 'X': X_ghm2, 'Ea': Ea_Wm2, 'El': El_Wm2,
                        'Epro': Epro_Wm2, 'Ere': Ere_Wm2, 'Ed': Ed_Wm2, 'Vww': Vww_ldm2,
                        'Vw': Vw_ldm2, 've': Ve_lsm2}

    return schedules, archetype_values

def read_schedules(use, x):
    """
    This function reads the occupancy, electricity, domestic hot water, process electricity and monthly schedules for a
    given use type from the schedules database.

    :param use: occupancy type (e.g. 'SCHOOL')
    :type use: str
    :param x: Excel worksheet containing the schedule database for a given occupancy type from the archetypes database
    :type x: DataFrame

    :return occ: the daily occupancy schedule for the given occupancy type
    :type occ: list[array]
    :return el: the daily electricity schedule for the given occupancy type
    :type el: list[array]
    :return dhw: the daily domestic hot water schedule for the given occupancy type
    :type dhw: list[array]
    :return pro: the daily process electricity schedule for the given occupancy type
    :type pro: list[array]
    :return month: the monthly schedule for the given occupancy type
    :type month: ndarray
    :return occ_density: the occupants per square meter for the given occupancy type
    :type occ_density: int
    :return internal_loads: the internal loads and ventilation needs for the given occupancy types
    :type internal_loads: list

    """
    # read schedules from excel file
    occ = [x['Weekday_1'].values[:24], x['Saturday_1'].values[:24], x['Sunday_1'].values[:24]]
    el = [x['Weekday_2'].values[:24], x['Saturday_2'].values[:24], x['Sunday_2'].values[:24]]
    dhw = [x['Weekday_3'].values[:24], x['Saturday_3'].values[:24], x['Sunday_3'].values[:24]]
    month = x['month'].values[:12]

    if use is "INDUSTRIAL":
        pro = [x['Weekday_4'].values[:24], x['Saturday_4'].values[:24], x['Sunday_4'].values[:24]]
    else:
        pro = [np.zeros(24), np.zeros(24), np.zeros(24)]

    # read occupancy density
    occ_density = x['density'].values[:1][0]
    # read occupant loads
    Qs_Wp = x['Qs_Wp'].values[:1][0]
    X_ghp = x['X_ghp'].values[:1][0]
    # read electricity demands
    Ea_Wm2 = x['Ea_Wm2'].values[:1][0]
    El_Wm2 = x['El_Wm2'].values[:1][0]
    Epro_Wm2 = x['Epro_Wm2'].values[:1][0]
    Ere_Wm2 = x['Ere_Wm2'].values[:1][0]
    Ed_Wm2 = x['Ed_Wm2'].values[:1][0]
    # read water demands
    Vww_lpd = x['Vww_lpd'].values[:1][0]
    Vw_lpd = x['Vw_lpd'].values[:1][0]
    # read ventilation demand
    Ve_lps = x['Ve_lps'].values[:1][0]

    # # get internal loads and ventilation in a list
    # internal_loads = [Qs_Wp, X_ghp, Ea_Wm2, El_Wm2, Epro_Wm2, Ere_Wm2, Ed_Wm2, Vww_lpd, Vw_lpd, Ve_lps]

    return occ, el, dhw, pro, month, occ_density # , Qs_Wp, X_ghp, Ea_Wm2, El_Wm2, Epro_Wm2, Ere_Wm2, Ed_Wm2, Vww_lpd, Vw_lpd, Ve_lps
