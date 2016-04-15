"""
inputlocator.py - locate input files by name based on the reference folder structure.
"""
import os
import tempfile


class InputLocator(object):
    """The InputLocator locates files and folders for input to the scripts. This works, because we
    have a convention for the folder structure of a scenario.
    It also provides locations of other files, such as those in the db folder (e.g. archetypes).
    """
    def __init__(self, scenario_path):
        self.scenario_path = scenario_path
        self.db_path = os.path.join(os.path.dirname(__file__), 'db')

    def get_archetypes_hvac_properties(self):
        """/cea/db/Archetypes/Archetypes_HVAC_properties.csv
        path to database of archetypes file Archetypes_HVAC_properties.csv"""
        return os.path.join(self.db_path, 'Archetypes', 'Archetypes_HVAC_properties.csv')

    def get_archetypes_embodied_emissions(self):
        """/cea/db/Archetypes/Archetypes_embodied_emissions.csv
        path to database of archetypes file Archetypes_embodied_emissions.csv"""
        return os.path.join(self.db_path, 'Archetypes', 'Archetypes_embodied_emissions.csv')

    def get_archetypes_embodied_energy(self):
        """/cea/db/Archetypes/Archetypes_embodied_energy.csv
        path to database of archetypes file Archetypes_embodied_energy.csv"""
        return os.path.join(self.db_path, 'Archetypes', 'Archetypes_embodied_energy.csv')

    def get_building_age(self):
        """scenario/1-inputs/1-buildings/building_age.shp"""
        return os.path.join(self.scenario_path, '1-inputs', '1-buildings', 'building_age.shp')

    def get_building_occupancy(self):
        """scenario/1-inputs/1-buildings/building_occupancy.shp"""
        return os.path.join(self.scenario_path, '1-inputs', '1-buildings', 'building_occupancy.shp')

    def get_building_geometry(self):
        """scenario/1-inputs/1-buildings/building_geometry.shp"""
        return os.path.join(self.scenario_path, '1-inputs', '1-buildings', 'building_geometry.shp')

    def get_building_supply(self):
        """scenario/1-inputs/1-buildings/building_supply.shp"""
        return os.path.join(self.scenario_path, '1-inputs', '1-buildings', 'building_supply.shp')

    def get_building_thermal(self):
        """scenario/1-inputs/1-buildings/building_thermal.shp"""
        return os.path.join(self.scenario_path, '1-inputs', '1-buildings', 'building_thermal.shp')

    def get_building_hvac(self):
        """scenario/1-inputs/1-buildings/building_HVAC.shp"""
        return os.path.join(self.scenario_path, '1-inputs', '1-buildings', 'building_HVAC.shp')

    def get_building_architecture(self):
        """scenario/1-inputs/1-buildings/building_architecture.shp"""
        return os.path.join(self.scenario_path, '1-inputs', '1-buildings', 'building_architecture.shp')

    def get_radiation(self):
        """scenario/2-results/1-radiation/1-timeseries/Radiation2000-2010.csv"""
        return os.path.join(self.scenario_path, '2-results', '1-radiation', '1-timeseries', 'radiation.csv')

    def get_weather_hourly(self):
        """scenario/1-inputs/3-weather/weather_hourly.csv"""
        return os.path.join(self.scenario_path, '1-inputs', '3-weather', 'weather_hourly.csv')

    def get_demand_results_folder(self):
        """scenario/2-results/2-demand/1-timeseries"""
        return os.path.join(self.scenario_path, '2-results', '2-demand', '1-timeseries')

    def get_total_demand(self):
        """scenario/2-results/2-demand/1-timeseries/Total_demand.csv"""
        return os.path.join(self.scenario_path, '2-results', '2-demand', '1-timeseries', 'Total_demand.csv')

    def get_schedule(self, schedule):
        """cea/db/Schedules/Occupancy_%SCHEDULE%.csv"""
        return os.path.join(self.db_path, 'Schedules', 'Occupancy_%s.csv' % schedule)

    def get_temporary_folder(self):
        """Temporary folder as returned by `tempfile`."""
        return tempfile.gettempdir()

    def get_temporary_file(self, filename):
        """Returns the path to a file in the temporary folder with the name `filename`"""
        return os.path.join(self.get_temporary_folder(), filename)
