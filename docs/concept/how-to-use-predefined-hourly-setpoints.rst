:orphan:

:Author: Sreepathi Bhargava Krishna
:Date: 26-February-2019

How to calculate demand using prefined-hourly-setpoints in CEA?
===============================================================

Step 1: In the `config` file, make the `demand.predefined-hourly-setpoints` as `True`

Step 2: Create `csv` files corresponding to `space-heating` and/or `space-cooling`. The files are to be named in the
`BuildingName_temperature.csv` format. The file content should be the values of time and the corresponding set point
temperature in the columns: `time` and `temperature`

Step 3: Run `cea\datamangement\data_helper.py`

Step 4: Run `cea\resources\radiation_daysim\radiation_main.py`

Step 5: Run `cea\demand\demand_main.py`

Step 6: Check the results in the outputs folder of the case study you are working on


How to get the predefined-hourly-setpoints?
===========================================

In place of having a single `setpoint temperature` and `setback temperature` combination, a building can be operated
dynamically, where in the set points can be varied based on the occupancy. This is an interaction which is tested in the
context of flexible buildings. There might be many ways for generating these hourly set points, of which a couple are
listed here

Approach 1: Manually use the set points of week days and week ends and fill the `csv` file

Approach 2: Use the MPC model developed in the CONCEPT project, which provides the temperatures of various zones
present in the building for every given hour, i.e. if a building has both office and residential spaces, both the
regions will have different set point temperatures for every given hour. Using these values, a single temperature
column is generated. For example, in space-cooling, if office space has a temperature of 23 and a residential space has
a temperature of 25, then the overall building temperature is set to be 23. This process is repeated for every given
hour and fed into the `csv` file. 


