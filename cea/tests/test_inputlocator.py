import unittest
import os
import cea.inputlocator

class TestInputLocator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.locator = cea.inputlocator.ReferenceCaseOpenLocator()

    def test_weather_names(self):
        self.assertTrue(len(self.locator.get_weather_names()) > 0)

    def test_weather(self):
        for weather in self.locator.get_weather_names():
            self.assertTrue(os.path.exists(self.locator.get_weather(weather)))

    def test_get_archetypes_properties(self):
        archetypes_properties = self.locator.get_archetypes_properties()
        self.assertTrue(os.path.exists(archetypes_properties))
        self.assertTrue(os.path.realpath(archetypes_properties).startswith(
            os.path.realpath(self.locator.scenario_path)), msg='Path not in scenario: %s' % archetypes_properties)

    def test_get_archetypes_schedules(self):
        archetypes_schedules = self.locator.get_archetypes_schedules()
        self.assertTrue(os.path.exists(archetypes_schedules))
        self.assertTrue(os.path.realpath(archetypes_schedules).startswith(
            os.path.realpath(self.locator.scenario_path)), msg='Path not in scenario: %s' % archetypes_schedules)

    def test_get_supply_systems_cost(self):
        supply_systems_cost = self.locator.get_supply_systems_cost()
        self.assertTrue(os.path.exists(supply_systems_cost))
        self.assertTrue(os.path.realpath(supply_systems_cost).startswith(
            os.path.realpath(self.locator.scenario_path)), msg='Path not in scenario: %s' % supply_systems_cost)

    def test_get_life_cycle_inventory_supply_systems(self):
        life_cycle_inventory_supply_systems = self.locator.get_life_cycle_inventory_supply_systems()
        self.assertTrue(os.path.exists(life_cycle_inventory_supply_systems))
        self.assertTrue(os.path.realpath(life_cycle_inventory_supply_systems).startswith(
            os.path.realpath(self.locator.scenario_path)),
            msg='Path not in scenario: %s' % life_cycle_inventory_supply_systems)
