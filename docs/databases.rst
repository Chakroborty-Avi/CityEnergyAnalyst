
Input Databases
---------------
Primary: Zone Geometry
^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database consists of a shapefile storing the geometry of buildings in the zone of analysis. This database is useful to calculate the geometry and position of buildings, and as such, it is a key element in all CEA.

**Format/Naming**: shapefile / zone.shp

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building-geometry/zone.shp``

**Primary Interdependencies**: None

**Secondary Interdependencies**: None

+--------------------------+---------+------+---------------------------------------------------------+--------------+
| Column names /parameters | Type    | Unit | Description                                             | Valid Values |
+==========================+=========+======+=========================================================+==============+
| Name                     | string  | [-]  | UniqK2:K271ue building ID. It must start with a letter. | alphanumeric |
+--------------------------+---------+------+---------------------------------------------------------+--------------+
| Height_ag                | float   | [m]  | Building total height above ground                      | {0.1...n}    |
+--------------------------+---------+------+---------------------------------------------------------+--------------+
| Height_bg                | float   | [m]  | Building total height below ground                      | {1.0...n}    |
+--------------------------+---------+------+---------------------------------------------------------+--------------+
| Floor_ag                 | integer | [-]  | Number of building floors above ground                  | {0...n}      |
+--------------------------+---------+------+---------------------------------------------------------+--------------+
| Floor_bg                 | integer | [-]  | Number of building floors below ground                  | {0...n}      |
+--------------------------+---------+------+---------------------------------------------------------+--------------+

Primary: District Geometry
^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database consists of a shapefile storing the geometry of buildings in the surroundings of the zone of analysis. This database is useful to calculate the radiation reflected from surrounding buildings into the zone of analysis.

**Format/Naming**: shapefile / district.shp

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building-geometry/zone.shp``

**Primary Interdependencies**: None

**Secondary Interdependencies**: None

+--------------------------+---------+------+--------------------------------------------------+--------------+
| Column names /parameters | Type    | Unit | Description                                      | Valid Values |
+==========================+=========+======+==================================================+==============+
| Name                     | string  | [-]  | Unique building ID. It must start with a letter. | alphanumeric |
+--------------------------+---------+------+--------------------------------------------------+--------------+
| Height_ag                | float   | [m]  | Building total height above ground               | {0.1...n}    |
+--------------------------+---------+------+--------------------------------------------------+--------------+
| Height_bg                | float   | [m]  | Building total height below ground               | {1.0...n}    |
+--------------------------+---------+------+--------------------------------------------------+--------------+
| Floor_ag                 | integer | [-]  | Number of building floors above ground           | {0...n}      |
+--------------------------+---------+------+--------------------------------------------------+--------------+
| Floor_bg                 | integer | [-]  | Number of building floors below ground           | {0...n}      |
+--------------------------+---------+------+--------------------------------------------------+--------------+

Primary: Building Metering
^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: 

**Format/Naming**: csv / B01.csv

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building-geometry/zone.shp``

**Primary Interdependencies**: None

**Secondary Interdependencies**: None

+--------------------------+---------+-----------------+----------------------------------------------------------------------+---------------------+
| Column names /parameters | Type    | Unit            | Description                                                          | Valid Values        |
+==========================+=========+=================+======================================================================+=====================+
| DATE                     | date    | [smalldatetime] | Time stamp for each day of the year ascending in hour intervals.     | YYYY-MM-DD hh:mm:ss |
+--------------------------+---------+-----------------+----------------------------------------------------------------------+---------------------+
| Name                     | string  | [-]             | Unique building ID. It must start with a letter.                     | alphanumeric        |
+--------------------------+---------+-----------------+----------------------------------------------------------------------+---------------------+
| E_sys_kWh                | integer | [# of people]   | Describes the occupancy in terms of pax for a given hour time stamp. | {0...n}             |
+--------------------------+---------+-----------------+----------------------------------------------------------------------+---------------------+
| Qhs_sys_kWh              | float   | [kWh]           | System heat demand                                                   | {0.0...n}           |
+--------------------------+---------+-----------------+----------------------------------------------------------------------+---------------------+
| Qww_sys_kWh              | float   | [kWh]           | Hot water heat demand                                                | {0.0...n}           |
+--------------------------+---------+-----------------+----------------------------------------------------------------------+---------------------+
| Qcs_sys_kWh              | float   | [kWh]           | System cool demand                                                   | {0.0...n}           |
+--------------------------+---------+-----------------+----------------------------------------------------------------------+---------------------+

Primary: Zone Age
^^^^^^^^^^^^^^^^^
**Description**: This database stores the age of construction and years of renovation of different architectural components in buildings in the zone of analysis.

**Format/Naming**: dataBase / age.dbf

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building_properties/age.dbf``

**Primary Interdependencies**: None

**Secondary Interdependencies**: None

+--------------------------+---------+------+--------------------------------------------------------------+--------------+
| Column names /parameters | Type    | Unit | Description                                                  | Valid Values |
+==========================+=========+======+==============================================================+==============+
| Name                     | string  | [-]  | Unique building ID. It must start with a letter.             | alphanumeric |
+--------------------------+---------+------+--------------------------------------------------------------+--------------+
| built                    | integer | [-]  | Construction year                                            | {0...n}      |
+--------------------------+---------+------+--------------------------------------------------------------+--------------+
| roof                     | integer | [-]  | Year of last retrofit of roof (0 if none)                    | {0...n}      |
+--------------------------+---------+------+--------------------------------------------------------------+--------------+
| windows                  | integer | [-]  | Year of last retrofit of windows (0 if none)                 | {0...n}      |
+--------------------------+---------+------+--------------------------------------------------------------+--------------+
| partitions               | integer | [-]  | Year of last retrofit of internal wall partitions(0 if none) | {0...n}      |
+--------------------------+---------+------+--------------------------------------------------------------+--------------+
| HVAC                     | integer | [-]  | Year of last retrofit of HVAC systems (0 if none)            | {0...n}      |
+--------------------------+---------+------+--------------------------------------------------------------+--------------+
| envelope                 | integer | [-]  | Year of last retrofit of building facades (0 if none)        | {0...n}      |
+--------------------------+---------+------+--------------------------------------------------------------+--------------+
| basement                 | integer | [-]  | Year of last retrofit of basement (0 if none)                | {0...n}      |
+--------------------------+---------+------+--------------------------------------------------------------+--------------+

Secondary: Zone Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores architectural properties of buildings in the zone of analysis.

**Format/Naming**: dataBase / architecture.dbf

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building_properties/architecture.dbf``

**Primary Interdependencies**: Default Databases

**Secondary Interdependencies**: None

+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit          | Description                                                                            | Valid Values |
+==========================+========+===============+========================================================================================+==============+
| Name                     | string | [-]           | Unique building ID. It must start with a letter.                                       | alphanumeric |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| void_deck                | float  | [floor/floor] | Share of floors with an open envelope (default = 0)                                    | {0.0...1}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| Hs                       | float  | [m2/m2]       | Fraction of gross floor area air-conditioned.                                          | {0.0...1}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| wwr_north                | float  | [m2/m2]       | Window to wall ratio in in facades facing north                                        | {0.0...1}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| wwr_south                | float  | [m2/m2]       | Window to wall ratio in in facades facing south                                        | {0.0...1}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| wwr_east                 | float  | [m2/m2]       | Window to wall ratio in in facades facing east                                         | {0.0...1}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| wwr_west                 | float  | [m2/m2]       | Window to wall ratio in in facades facing west                                         | {0.0...1}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| wwr_x                    | float  | [m2/m2]       | Average window-to-wall area ratio in the cardinal direction x                          | {0.0...1}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| n50                      | float  | [1/h]         | Air exchanges per hour at a pressure of 50 Pa.                                         | {0.0...10}   |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| type_roof                | string | [-]           | Roof construction type (relates to values in Default Database Construction Properties) | {T1...Tn}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| type_wall                | float  | [m2/m2]       | Wall construction type (relates to values in Default Database Construction Properties) | {T1...Tn}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| type_win                 | float  | [m2/m2]       | Window type (relates to values in Default Database Construction Properties)            | {T1...Tn}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+
| type_shade               | float  | [m2/m2]       | Shading system type (relates to values in Default Database Construction Properties)    | {T1...Tn}    |
+--------------------------+--------+---------------+----------------------------------------------------------------------------------------+--------------+

Secondary: Zone Indoor Comfort
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database consists of a .dbf file storing thresholds of thermal comfort necessary for buildings in the zone of analysis. This database is useful to set the upper and lower limits for heating or cooling a building, as such, it is a key element of CEA.

**Format/Naming**: dataBase / indoor_comfort.dbf

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building_properties/internal_loads.dbf``

**Primary Interdependencies**: Default Databases

**Secondary Interdependencies**: None

+--------------------------+--------+-------+--------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit  | Description                                                  | Valid Values |
+==========================+========+=======+==============================================================+==============+
| Name                     | string | [-]   | Unique building ID. It must start with a letter.             | alphanumeric |
+--------------------------+--------+-------+--------------------------------------------------------------+--------------+
| Ths_set_C                | float  | [C]   | Setpoint temperature for heating system                      | {0.0...n}    |
+--------------------------+--------+-------+--------------------------------------------------------------+--------------+
| Ths_setb_C               | float  | [C]   | Setback point of temperature for heating system              | {0.0...n}    |
+--------------------------+--------+-------+--------------------------------------------------------------+--------------+
| Tcs_set_C                | float  | [C]   | Setpoint temperature for cooling system                      | {0.0...n}    |
+--------------------------+--------+-------+--------------------------------------------------------------+--------------+
| Tcs_setb_C               | float  | [C]   | Setback point of temperature for cooling system              | {0.0...n}    |
+--------------------------+--------+-------+--------------------------------------------------------------+--------------+
| Ve_lps                   | float  | [l/s] | Indoor quality requirements of indoor ventilation per person | {0.0...n}    |
+--------------------------+--------+-------+--------------------------------------------------------------+--------------+
| rhum_min_p               | float  | [%]   | Minimum relative humidity threshold                          | {0.0...n}    |
+--------------------------+--------+-------+--------------------------------------------------------------+--------------+
| rhum_max_p               | float  | [%]   | Maximum relative humidity threshold                          | {0.0...n}    |
+--------------------------+--------+-------+--------------------------------------------------------------+--------------+

Secondary: Zone Internal Loads
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database consists of a .dbf file storing internal thermal loads in buildings in the zone of analysis. This database is useful to calculate the heat released inside the building due to the use of appliances, people moving etc, as such, it is a key element of CEA

**Format/Naming**: dataBase / internal_loads.dbf

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building_properties/internal_loads.dbf``

**Primary Interdependencies**: Default Databases

**Secondary Interdependencies**: None

+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit      | Description                                                         | Valid Values |
+==========================+========+===========+=====================================================================+==============+
| Name                     | string | [-]       | Unique building ID. It must start with a letter.                    | alphanumeric |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| X_ghp                    | float  | [gh/kg/p] | Moisture released by occupancy at peak conditions                   | {0.0...n}    |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| Ea_Wm2                   | float  | [W/m2]    | Peak specific electrical load due to computers and devices          | {0.0...n}    |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| El_Wm2                   | float  | [W/m2]    | Peak specific electrical load due to artificial lighting            | {0.0...n}    |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| Epro_Wm2                 | string | [W/m2]    | Peak specific electrical load due to industrial processes           | {0.0...n}    |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| Ere_Wm2                  | float  | [W/m2]    | Peak specific electrical load due to refrigeration                  | {0.0...n}    |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| Ed_Wm2                   | float  | [W/m2]    | Peak specific electrical load due to servers/data centres           | {0.0...n}    |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| Vww_lpd                  | float  | [lpd]     | Peak specific daily hot water consumption                           | {0.0...n}    |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| Vw_lpd                   | float  | [lpd]     | Peak specific fresh water consumption (includes cold and hot water) | {0.0...n}    |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+
| Qhpro_Wm2                | float  | [W/m2]    | Peak specific due to process heat                                   | {0.0...n}    |
+--------------------------+--------+-----------+---------------------------------------------------------------------+--------------+

Primary: Zone Occupancy Mix
^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database consists of a .dbf file storing shares of occupancy types in buildings in the zone of analysis. This database is useful to determine hourly patterns of occupancy of buildings in the area. CEA covers >15 different types of occupancy. Mix-use buildings are represented by different shares

**Format/Naming**: dataBase / occupancy.dbf

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building_properties/age.dbf``

**Primary Interdependencies**: None

**Secondary Interdependencies**: None

+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit    | Description                                                            | Valid Values |
+==========================+========+=========+========================================================================+==============+
| Name                     | string | [-]     | Unique building ID. It must start with a letter.                       | alphanumeric |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| HOTEL                    | float  | [m2/m2] | Share (fraction of gross floor area) of hospitality area               | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| COOLROOM                 | float  | [m2/m2] | Share (fraction of gross floor area) of coolrooms                      | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| PARKING                  | float  | [m2/m2] | Share (fraction of gross floor area) of parking area                   | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| SCHOOL                   | float  | [m2/m2] | Share (fraction of gross floor area) of school                         | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| OFFICE                   | float  | [m2/m2] | Share (fraction of gross floor area) of office space                   | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| GYM                      | float  | [m2/m2] | Share (fraction of gross floor area) of of gym space                   | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| HOSPITAL                 | float  | [m2/m2] | Share (fraction of gross floor area) of hospital area                  | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| INDUSTRIAL               | float  | [m2/m2] | Share (fraction of gross floor area) of industrial area                | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| RETAIL                   | float  | [m2/m2] | Share (fraction of gross floor area) of retail area                    | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| RESTAURANT               | float  | [m2/m2] | Share (fraction of gross floor area) of this occupancy in the building | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| SINGLE_RES               | float  | [m2/m2] | Share (fraction of gross floor area) of this occupancy in the building | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| MULTI-RES                | float  | [m2/m2] | Share (fraction of gross floor area) of this occupancy in the building | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| SERVERROOM               | float  | [m2/m2] | Share (fraction of gross floor area) of this occupancy in the building | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| SWIMMING                 | float  | [m2/m2] | Share (fraction of gross floor area) of this occupancy in the building | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| FOODSTORE                | float  | [m2/m2] | Share (fraction of gross floor area) of this occupancy in the building | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+
| LIBRARY                  | float  | [m2/m2] | Share (fraction of gross floor area) of this occupancy in the building | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------+--------------+

Secondary: Restrictions
^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores flags related to restrictions to the use of local resources in the zone of analysis.

**Format/Naming**: dataBase / restrictions.dbf

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building-properties/restrictions.dbf``

**Primary Interdependencies**: Default Databases

**Secondary Interdependencies**: None

+--------------------------+---------+------+---------------------------------------------------------------+--------------+
| Column names /parameters | Type    | Unit | Description                                                   | Valid Values |
+==========================+=========+======+===============================================================+==============+
| NAME                     | string  | [-]  | Unique building ID. It must start with a letter.              | alphanumeric |
+--------------------------+---------+------+---------------------------------------------------------------+--------------+
| SOLAR                    | float   | [-]  | share of solar rooftop area protected                         | {0.0...1}    |
+--------------------------+---------+------+---------------------------------------------------------------+--------------+
| GEOTHERMAL               | float   | [-]  | share of foot-print area protected for geothermal exploration | {0.0...1}    |
+--------------------------+---------+------+---------------------------------------------------------------+--------------+
| WATERBODY                | integer | [-]  | Use of water bodies is restricted in the area. 0 = no, 1, yes | {0, 1}       |
+--------------------------+---------+------+---------------------------------------------------------------+--------------+
| NATURALGAS               | integer | [-]  | Natural gas restricted in the area. 0 = no, 1, yes            | {0, 1}       |
+--------------------------+---------+------+---------------------------------------------------------------+--------------+
| BIOGAS                   | integer | [-]  | Biogas gas restricted in the area. 0 = no, 1, yes             | {0, 1}       |
+--------------------------+---------+------+---------------------------------------------------------------+--------------+

Primary: Supply Systems
^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database consists of a .dbf file storing the type of heating, cooling and electrical supply systems of buildings in the zone of analysis. This database is useful to calculate the emissions due to operation of buildings and their underlying infrastructure.

**Format/Naming**: dataBase / supply_systems.dbf

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building-properties/supply_systems.dbf``

**Primary Interdependencies**: None

**Secondary Interdependencies**: None

+--------------------------+--------+------+--------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit | Description                                      | Valid Values |
+==========================+========+======+==================================================+==============+
| Name                     | string | [-]  | Unique building ID. It must start with a letter. | alphanumeric |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| type_cs                  | string | [-]  | Type of cooling supply system                    | {T0...Tn}    |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| type_hs                  | string | [-]  | Type of heating supply system                    | {T0...Tn}    |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| type_dhw                 | string | [-]  | Type of hot water supply system                  | {T0...Tn}    |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| type_el                  | string | [-]  | Type of electrical supply system                 | {T0...Tn}    |
+--------------------------+--------+------+--------------------------------------------------+--------------+

Secondary: Zone HVAC
^^^^^^^^^^^^^^^^^^^^
**Description**: This database consists of a .dbf file storing information of HVAC systems in buildings. This database is useful to know which type of technical system the building is using. Depending on the system, the energy demand of the building can be supplied in different ways.

**Format/Naming**: dataBase / technical_systems.dbf

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/building_properties/technical_systems.dbf``

**Primary Interdependencies**: Default Databases

**Secondary Interdependencies**: 

+--------------------------+--------+---------+-----------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit    | Description                                                                                         | Valid Values |
+==========================+========+=========+=====================================================================================================+==============+
| Name                     | string | [-]     | Unique building ID. It must start with a letter.                                                    | alphanumeric |
+--------------------------+--------+---------+-----------------------------------------------------------------------------------------------------+--------------+
| type_cs                  | string | [-]     | Type of cooling system (relates to values in Default Database HVAC Properties)                      | {T1...Tn}    |
+--------------------------+--------+---------+-----------------------------------------------------------------------------------------------------+--------------+
| type_hs                  | string | [m2/m2] | Type of heating system (relates to values in Default Database HVAC Properties)                      | {T1...Tn}    |
+--------------------------+--------+---------+-----------------------------------------------------------------------------------------------------+--------------+
| type_dhw                 | string | [m2/m2] | Type of hot water system (relates to values in Default Database HVAC Properties)                    | {T1...Tn}    |
+--------------------------+--------+---------+-----------------------------------------------------------------------------------------------------+--------------+
| type_ctrl                | string | [m2/m2] | Type of heating and cooling control systems (relates to values in Default Database HVAC Properties) | {T1...Tn}    |
+--------------------------+--------+---------+-----------------------------------------------------------------------------------------------------+--------------+
| type_vent                | string | [m2/m2] | Type of ventilation strategy (relates to values in Default Database HVAC Properties)                | {T1...Tn}    |
+--------------------------+--------+---------+-----------------------------------------------------------------------------------------------------+--------------+

Primary: Streets
^^^^^^^^^^^^^^^^
**Description**: This database stores streets or pathways where a distritct heating, cooling or electrical network can be potentially built in the zone of analysis.

**Format/Naming**: Shapefile / streets.shp

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/networks/streets.shp ``

**Primary Interdependencies**: None

**Secondary Interdependencies**: None

+--------------------------+------+------+-------------------------------------------------+--------------+
| Column names /parameters | Type | Unit | Description                                     | Valid Values |
+==========================+======+======+=================================================+==============+
| streets                  | [-]  | [-]  | Geometry showing where the streets are located. | [-]          |
+--------------------------+------+------+-------------------------------------------------+--------------+

Intermediate: District Cooling Network
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores the geometry of district cooling networks in the zone of analysis.

**Format/Naming**: Shapefile / edges.shp, nodes.shp

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/networks/DC/edges.shp `` and `` ..cea/examples/reference-case-open/baseline/inputs/networks/DC/nodes.shp ``

**Primary Interdependencies**: 

**Secondary Interdependencies**: None

+--------------------------+------+------+--------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type | Unit | Description                                                                    | Valid Values |
+==========================+======+======+================================================================================+==============+
| edges /nodes             | [-]  | [-]  | Geometry showing where the pipes (edges) and buildings/plants (nodes) located. | [-]          |
+--------------------------+------+------+--------------------------------------------------------------------------------+--------------+

Intermediate: District Heating Network
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores the geometry of district heating networks in the zone of analysis.

**Format/Naming**: Shapefile / edges.shp, nodes.shp

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/networks/DH/edges.shp `` and `` ..cea/examples/reference-case-open/baseline/inputs/networks/DH/nodes.shp ``

**Primary Interdependencies**: 

**Secondary Interdependencies**: None

+--------------------------+------+------+--------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type | Unit | Description                                                                    | Valid Values |
+==========================+======+======+================================================================================+==============+
| edges/nodes              | [-]  | [-]  | Geometry showing where the pipes (edges) and buildings/plants (nodes) located. | [-]          |
+--------------------------+------+------+--------------------------------------------------------------------------------+--------------+

Primary: District Topography
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database consists in a raster image with cells of 5m X 5m of resolution storing the elevation of the topography in m.

**Format/Naming**: raster / terrain.tiff

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/inputs/topography/terrain.tiff ``

**Primary Interdependencies**: None

**Secondary Interdependencies**: None

+--------------------------+------+------+-------------+--------------+
| Column names /parameters | Type | Unit | Description | Valid Values |
+==========================+======+======+=============+==============+
| terrain.tiff             | [-]  | [-]  | [-]         | [-]          |
+--------------------------+------+------+-------------+--------------+

Primary: Zone Weather
^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores hourly data about the weather conditions of the zone of interest.

**Format/Naming**: eplus file / zurich.epw

**Location (example)**: `` ..cea/databases/CH/weather/zurich.epw``

**Primary Interdependencies**: None

**Secondary Interdependencies**: None

+--------------------------+------+------+-------------+--------------+
| Column names /parameters | Type | Unit | Description | Valid Values |
+==========================+======+======+=============+==============+
| <location>.epw           | [-]  | [-]  | [-]         | [-]          |
+--------------------------+------+------+-------------+--------------+


Default Databases
-----------------
Construction Properties_Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores building properties of the Swiss building stock. This database is useful to retrieve properties of buildings based on their construction year and age.

**Format/Naming**: excel file / construction.xlsx

**Location (example)**: `` cea/databases/CH/archetypes/construction_properties.xlsx ``

**Primary Interdependencies**: None

**Secondary Interdependencies**: Receives data from the primary input databases of ?age? and ?occupancy?. Serves to produce all secondary input databases.

+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Column names /parameters | Type   | Unit          | Description                                                                                                                     | Valid Values                   |
+==========================+========+===============+=================================================================================================================================+================================+
| Name                     | string | [-]           | Unique building ID. It must start with a letter.                                                                                | alphanumeric                   |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| building_use             | string | [-]           | Building use. It relates to the uses stored in the input database of Zone_occupancy                                             | Those stored in Zone_occupancy |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| year_start               | int    | [yr]          | Lower limit of year interval where the building properties apply                                                                | {0...n}                        |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| year_end                 | int    | [yr]          | Upper limit of year interval where the building properties apply                                                                | {0...n}                        |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| standard                 | string | [-]           | Letter representing whereas the field represent construction properties of a building as newly constructed, C, or renovated, R. | {C, R}                         |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Hs                       | float  | [-]           | Fraction of heated space in building archetype                                                                                  | {0.0...1}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| win_wall                 | float  | [-]           | Window to wall ratio in building archetype                                                                                      | {0.0...1}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| wwr_north                | float  | [-]           | Window to wall ratio in building archetype                                                                                      | {0.0...1}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| wwr_south                | float  | [-]           | Window to wall ratio in building archetype                                                                                      | {0.0...1}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| wwr_east                 | float  | [-]           | Window to wall ratio in building archetype                                                                                      | {0.0...1}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| wwr_west                 | float  | [-]           | Window to wall ratio in building archetype                                                                                      | {0.0...1}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_cons                | string | [-]           | Type of construction. It relates to the contents of the default database of Envelope Properties: construction                   | {T1...Tn}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_leak                | string | [-]           | Leakage level. It relates to the contents of the default database of Envelope Properties: leakage                               | {T1...Tn}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_win                 | string | [-]           | Window type. It relates to the contents of the default database of Envelope Properties: windows                                 | {T1...Tn}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_roof                | string | [-]           | Roof construction. It relates to the contents of the default database of Envelope Properties: roof                              | {T1...Tn}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_wall                | string | [-]           | Wall construction. It relates to the contents of the default database of Envelope Properties: walll                             | {T1...Tn}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_shade               | string | [-]           | Shading system type. It relates to the contents of the default database of Envelope Properties: shade                           | {T1...Tn}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| void_dek                 | float  | [floor/floor] | Share of floors with an open envelope (default = 0)                                                                             | {0.0...1}                      |
+--------------------------+--------+---------------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+

Construction Properties_Supply
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores building properties of the Swiss building stock. This database is useful to retrieve properties of buildings based on their construction year and age.

**Format/Naming**: excel file / construction.xlsx

**Location (example)**: `` cea/databases/CH/archetypes/construction_properties.xlsx ``

**Primary Interdependencies**: None

**Secondary Interdependencies**: Receives data from the primary input databases of ?age? and ?occupancy?. Serves to produce all secondary input databases.

+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Column names /parameters | Type   | Unit | Description                                                                                                                     | Valid Values                   |
+==========================+========+======+=================================================================================================================================+================================+
| building_use             | string | [-]  | Building use. It relates to the uses stored in the input database of Zone_occupancy                                             | Those stored in Zone_occupancy |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| year_start               | int    | [yr] | Lower limit of year interval where the building properties apply                                                                | {0...n}                        |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| year_end                 | int    | [yr] | Upper limit of year interval where the building properties apply                                                                | {0...n}                        |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| standard                 | string | [-]  | Letter representing whereas the field represent construction properties of a building as newly constructed, C, or renovated, R. | {C, R}                         |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_hs                  | string | [-]  | Type of heating supply system                                                                                                   | {T0...Tn}                      |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_dhw                 | string | [-]  | Type of hot water supply system                                                                                                 | {T0...Tn}                      |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_cs                  | string | [-]  | Type of cooling supply system                                                                                                   | {T0...Tn}                      |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| type_el                  | string | [-]  | Type of electrical supply system                                                                                                | {T0...Tn}                      |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+

Construction Properties_HVAC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores building properties of the Swiss building stock. This database is useful to retrieve properties of buildings based on their construction year and age.

**Format/Naming**: excel file / construction.xlsx

**Location (example)**: `` cea/databases/CH/archetypes/construction_properties.xlsx ``

**Primary Interdependencies**: None

**Secondary Interdependencies**: Receives data from the primary input databases of ?age? and ?occupancy?. Serves to produce all secondary input databases.

+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit | Description                                                                                                                     | Valid Values |
+==========================+========+======+=================================================================================================================================+==============+
| building_use             | string | [-]  | Building use. It relates to the uses stored in the input database of Zone_occupancy                                             | [-]          |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+
| year_start               | int    | [yr] | Lower limit of year interval where the building properties apply                                                                | {0...n}      |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+
| year_end                 | int    | [yr] | Upper limit of year interval where the building properties apply                                                                | {0...n}      |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+
| standard                 | string | [-]  | Letter representing whereas the field represent construction properties of a building as newly constructed, C, or renovated, R. | {C , R}      |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+
| type_hs                  | string | [-]  | Type of heating supply system                                                                                                   | {T0...Tn}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+
| type_cs                  | string | [-]  | Type of cooling supply system                                                                                                   | {T0...Tn}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+
| type_dhw                 | string | [-]  | Type of hot water supply system                                                                                                 | {T0...Tn}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+
| type_ctrl                | string | [-]  | Type of control system                                                                                                          | {T0...Tn}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+
| type_vent                | string | [-]  | Type of ventilation system                                                                                                      | {T0...Tn}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------+

Construction Properties_Indoor Comfort
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores building properties of the Swiss building stock. This database is useful to retrieve properties of buildings based on their construction year and age.

**Format/Naming**: excel file / construction.xlsx

**Location (example)**: `` cea/databases/CH/archetypes/construction_properties.xlsx ``

**Primary Interdependencies**: None

**Secondary Interdependencies**: Receives data from the primary input databases of ?age? and ?occupancy?. Serves to produce all secondary input databases.

+----------------------------------------------------------------------------+------+------+-------------+--------------+
| Column names /parameters                                                   | Type | Unit | Description | Valid Values |
+============================================================================+======+======+=============+==============+
| Same parameters as Zone Indoor Comfort plus additional Code (for Building) | [-]  | [-]  | [-]         | [-]          |
+----------------------------------------------------------------------------+------+------+-------------+--------------+

Construction Properties_Internal Loads
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores building properties of the Swiss building stock. This database is useful to retrieve properties of buildings based on their construction year and age.

**Format/Naming**: excel file / construction.xlsx

**Location (example)**: `` cea/databases/CH/archetypes/construction_properties.xlsx ``

**Primary Interdependencies**: None

**Secondary Interdependencies**: Receives data from the primary input databases of ?age? and ?occupancy?. Serves to produce all secondary input databases.

+-----------------------------------------------------------------------+------+------+-------------+--------------+
| Column names /parameters                                              | Type | Unit | Description | Valid Values |
+=======================================================================+======+======+=============+==============+
| Same parameters as Internal Loads plus additional Code (for Building) | [-]  | [-]  | [-]         | [-]          |
+-----------------------------------------------------------------------+------+------+-------------+--------------+

Occupancy Schedules
^^^^^^^^^^^^^^^^^^^
**Description**: This database in Excel stores information of schedules of occupancy, and use of hot water, lighting and other electrical appliances. Every tab in this excel file corresponds to a type of occupancy. This database is useful to calculate the demand of energy in buildings.

**Format/Naming**: excel file / occupancy_schedule.xlsx

**Location (example)**: `` cea/databases/CH/archetypes/occupancy_schedules.xlsx``

**Primary Interdependencies**: Relates detailed data to the primary input database of Zone occupancy.

**Secondary Interdependencies**: None

+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Column names /parameters   | Type   | Unit   | Description                                                          | Valid Values |
+============================+========+========+======================================================================+==============+
| Name                       | string | [-]    | Unique building ID. It must start with a letter.                     | alphanumeric |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Weekday_1                  | float  | [p/p]  | Probability of maximum occupancy per hour in a weekday               | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Saturday_1                 | float  | [p/p]  | Probability of maximum occupancy per hour on Saturday                | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Sunday_1                   | float  | [p/p]  | Probability of maximum occupancy per hour on Sunday                  | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Weekday_2                  | float  | [p/p]  | Probability of use of lighting and applicances (daily) for each hour | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Saturday_2                 | float  | [p/p]  | Probability of use of lighting and applicances (daily) for each hour | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Sunday_2                   | float  | [p/p]  | Probability of use of lighting and applicances (daily) for each hour | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Weekday_3                  | float  | [p/p]  | Probability of domestic hot water consumption (daily) for each hour  | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Saturday_3                 | float  | [p/p]  | Probability of domestic hot water consumption (daily) for each hour  | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Sunday_3                   | float  | [p/p]  | Probability of domestic hot water consumption (daily) for each hour  | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| probability of use monthly | float  | [p/p]  | Probability of use for the month                                     | {0.0...1}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+
| Occupancy density          | float  | [m2/p] | m2 per person                                                        | {0.0...n}    |
+----------------------------+--------+--------+----------------------------------------------------------------------+--------------+

System Controls
^^^^^^^^^^^^^^^
**Description**: This database in Excel stores information used to define the cooling and heating seasons for a given scenario.

**Format/Naming**: excel file / systems_controls.xlsx

**Location (example)**: `` cea/databases/CH/archetypes/systems_controls.xlsx ``

**Primary Interdependencies**: 

**Secondary Interdependencies**: Note: the heating and cooling seasons need to be non-overlapping and comprise the entire year.

+--------------------------+---------+------+----------------------------------------------------+---------------+
| Column names /parameters | Type    | Unit | Description                                        | Valid Values  |
+==========================+=========+======+====================================================+===============+
| has-heating-season       | Boolean | [-]  | Defines whether the scenario has a heating season. | {TRUE, FALSE} |
+--------------------------+---------+------+----------------------------------------------------+---------------+
| heating-season-start     | date    | [-]  | Day on which the heating season starts             | mm-dd         |
+--------------------------+---------+------+----------------------------------------------------+---------------+
| heating-season-end       | date    | [-]  | Last day of the heating season                     | mm-dd         |
+--------------------------+---------+------+----------------------------------------------------+---------------+
| has-cooling-season       | Boolean | [-]  | Defines whether the scenario has a cooling season. | {TRUE, FALSE} |
+--------------------------+---------+------+----------------------------------------------------+---------------+
| cooling-season-start     | date    | [-]  | Day on which the cooling season starts             | mm-dd         |
+--------------------------+---------+------+----------------------------------------------------+---------------+
| cooling-season-end       | date    | [-]  | Last day of the cooling season                     | mm-dd         |
+--------------------------+---------+------+----------------------------------------------------+---------------+

Benchmarks
^^^^^^^^^^
**Description**: This database in Excel stores information used to define the characteristics of a benchmark from which comparisons are made considering the modelled performance.

**Format/Naming**: excel file / benchmark_2000W.xlsx

**Location (example)**: `` cea/databases/CH/benchmarks/benchmark_2000W.xlsx ``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| Column names /parameters | Type   | Unit | Description                                                                         | Valid Values                   |
+==========================+========+======+=====================================================================================+================================+
| code                     | string | [-]  | Building use. It relates to the uses stored in the input database of Zone_occupancy | Those stored in Zone_occupancy |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| NRE_today                | float  | [-]  | Present non-renewable energy consumption                                            | {0.0...n}                      |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| CO2_today                | float  | [-]  | Present CO2 production                                                              | {0.0...n}                      |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| PEN_today                | float  | [-]  | Present primary energy demand                                                       | {0.0...n}                      |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| NRE_target_retrofit      | float  | [-]  | Target non-renewable energy consumption for retrofitted buildings                   | {0.0...n}                      |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| CO2_target_retrofit      | float  | [-]  | Target CO2 production for retrofitted buildings                                     | {0.0...n}                      |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| PEN_target_retrofit      | float  | [-]  | Target primary energy demand for retrofitted buildings                              | {0.0...n}                      |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| NRE_target_new           | float  | [-]  | Target non-renewable energy consumption for newly constructed buildings             | {0.0...n}                      |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| CO2_target_new           | float  | [-]  | Target CO2 production for newly constructed buildings                               | {0.0...n}                      |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| PEN_target_new           | float  | [-]  | Target primary energy demand for newly constructed buildings                        | {0.0...n}                      |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+
| Description              | string | [-]  | Describes the source of the benchmark standards.                                    | [-]                            |
+--------------------------+--------+------+-------------------------------------------------------------------------------------+--------------------------------+

Supply Systems
^^^^^^^^^^^^^^
**Description**: This database contains the schedule for various conduits, relating pipe nominal diameter (DN) to investment cost. This is helful for approximating the costs of hydraulic networks.

**Format/Naming**: excel file / supply_systems.xls

**Location (example)**: `` cea/databases/CH/economics/supply_systems.xls ``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+-------+--------------------------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit  | Description                                                                                                        | Valid Values |
+==========================+========+=======+====================================================================================================================+==============+
| Description              | string | [DN#] | Classifies nominal pipe diameters (DN) into typical bins. E.g. DN100 refers to pipes of approx. 100mm in diameter. | alphanumeric |
+--------------------------+--------+-------+--------------------------------------------------------------------------------------------------------------------+--------------+
| Diameter_max             | float  | [-]   | Defines the maximum pipe diameter tolerance for the nominal diameter (DN) bin.                                     | {0.0....n}   |
+--------------------------+--------+-------+--------------------------------------------------------------------------------------------------------------------+--------------+
| Diameter_min             | float  | [-]   | Defines the minimum pipe diameter tolerance for the nominal diameter (DN) bin.                                     | {0.0....n}   |
+--------------------------+--------+-------+--------------------------------------------------------------------------------------------------------------------+--------------+
| Unit                     | string | [mm]  | Defines the unit of measurement for the diameter values.                                                           | [-]          |
+--------------------------+--------+-------+--------------------------------------------------------------------------------------------------------------------+--------------+
| Investment               | float  | [$/m] | Typical cost of investment for a given pipe diameter.                                                              | {0.0....n}   |
+--------------------------+--------+-------+--------------------------------------------------------------------------------------------------------------------+--------------+
| Currency                 | string | [-]   | Defines the unit of currency used to create the cost estimations (year specific). E.g. USD-2015.                   | [-]          |
+--------------------------+--------+-------+--------------------------------------------------------------------------------------------------------------------+--------------+

LCA Buildings: EMBODIED_ENERGY
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information for the Life Cycle Analysis of buildings due to their construction and dismantling. This database is useful to calculate the embodied emissions and grey energy of buildings.

**Format/Naming**: excel file / LCA_buidlings.xlsx

**Location (example)**: `` cea/databases/CH/lifecycle/LCA_buildings.xlsx``

**Primary Interdependencies**: Relates detailed data to the primary input database of age and occupancy

**Secondary Interdependencies**: None

+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Column names /parameters | Type   | Unit | Description                                                                                                                     | Valid Values                   |
+==========================+========+======+=================================================================================================================================+================================+
| building_use             | string | [-]  | Building use. It relates to the uses stored in the input database of Zone_occupancy                                             | Those stored in Zone_occupancy |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| year_start               | int    | [-]  | Lower limit of year interval where the building properties apply                                                                | {0...n}                        |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| year_end                 | int    | [-]  | Upper limit of year interval where the building properties apply                                                                | {0...n}                        |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| standard                 | string | [-]  | Letter representing whereas the field represent construction properties of a building as newly constructed, C, or renovated, R. | {C, R}                         |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Wall_ext_ag              | float  | [GJ] | Typical embodied energy of the exterior above ground walls.                                                                     | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Wall_ext_bg              | float  | [GJ] | Typical embodied energy of the exterior below ground walls.                                                                     | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Floor_int                | float  | [GJ] | Typical embodied energy of the interior floor.                                                                                  | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Wall_int_sup             | float  | [GJ] |                                                                                                                                 | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Wall_int_nosup           | float  | [GJ] |                                                                                                                                 | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Roof                     | float  | [GJ] | Typical embodied energy of the roof.                                                                                            | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Floor_g                  | float  | [GJ] | Typical embodied energy of the ground floor.                                                                                    | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Services                 | float  | [GJ] | Typical embodied energy of the building services.                                                                               | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Win_ext                  | float  | [GJ] | Typical embodied energy of the external glazing.                                                                                | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Excavation               | float  | [GJ] | Typical embodied energy for site excavation.                                                                                    | {0.0....n}                     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+

LCA Buildings: EMBODIED_EMISSIONS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information for the Life Cycle Analysis of buildings due to their construction and dismantling. This database is useful to calculate the embodied emissions and grey energy of buildings.

**Format/Naming**: excel file / LCA_buidlings.xlsx

**Location (example)**: `` cea/databases/CH/lifecycle/LCA_buildings.xlsx``

**Primary Interdependencies**: Relates detailed data to the primary input database of age and occupancy

**Secondary Interdependencies**: None

+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Column names /parameters | Type   | Unit    | Description                                                                                                                     | Valid Values                   |
+==========================+========+=========+=================================================================================================================================+================================+
| building_use             | string | [-]     | Building use. It relates to the uses stored in the input database of Zone_occupancy                                             | Those stored in Zone_occupancy |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| year_start               | int    | [-]     | Lower limit of year interval where the building properties apply                                                                | {0...n}                        |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| year_end                 | int    | [-]     | Upper limit of year interval where the building properties apply                                                                | {0...n}                        |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| standard                 | string | [-]     | Letter representing whereas the field represent construction properties of a building as newly constructed, C, or renovated, R. | {C, R}                         |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Wall_ext_ag              | float  | [kgCO2] | Typical embodied CO2 equivalent emissions of the exterior above ground walls.                                                   | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Wall_ext_bg              | float  | [kgCO2] | Typical embodied CO2 equivalent emissions of the exterior below ground walls.                                                   | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Floor_int                | float  | [kgCO2] | Typical embodied CO2 equivalent emissions of the interior floor.                                                                | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Wall_int_sup             | float  | [kgCO2] |                                                                                                                                 | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Wall_int_nosup           | float  | [kgCO2] |                                                                                                                                 | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Roof                     | float  | [kgCO2] | Typical embodied CO2 equivalent emissions of the roof.                                                                          | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Floor_g                  | float  | [kgCO2] | Typical embodied CO2 equivalent emissions of the ground floor.                                                                  | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Services                 | float  | [kgCO2] | Typical embodied CO2 equivalent emissions of the building services.                                                             | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Win_ext                  | float  | [kgCO2] | Typical embodied CO2 equivalent emissions of the external glazing.                                                              | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+
| Excavation               | float  | [kgCO2] | Typical embodied CO2 equivalent emissions for site excavation.                                                                  | {0.0....n}                     |
+--------------------------+--------+---------+---------------------------------------------------------------------------------------------------------------------------------+--------------------------------+

LCA Infrastructure
^^^^^^^^^^^^^^^^^^
**Description**: This database stores information for the Life Cycle Analysis of energy infrastructure in buildings and districts. This database is useful to calculate the emissions and primary energy per unit of energy consumed in the area.

**Format/Naming**: excel file / LCA_infrastructure.xlsx

**Location (example)**: `` cea/databases/CH/lifecycle/LCA_infrastructure.xlsx``

**Primary Interdependencies**: Relates detailed data to the primary input database of supply_systems

**Secondary Interdependencies**: None

+--------------------------+--------+-----------+-------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit      | Description                                                                                     | Valid Values |
+==========================+========+===========+=================================================================================================+==============+
| Description              | string | [-]       | Description of the heating and cooling network (related to the code). E.g. heatpump -soil/water | [-]          |
+--------------------------+--------+-----------+-------------------------------------------------------------------------------------------------+--------------+
| code                     | string | [-]       | Unique ID of component of the heating and cooling network                                       | {T1..Tn}     |
+--------------------------+--------+-----------+-------------------------------------------------------------------------------------------------+--------------+
| PEN                      | float  | [kWh/kWh] | Refers to the amount of primary energy needed (PEN) to run the heating or cooling system.       | {0.0....n}   |
+--------------------------+--------+-----------+-------------------------------------------------------------------------------------------------+--------------+
| CO2                      | float  | [kg/kWh]  | Refers to the equivalent CO2 required to run the heating or cooling system.                     | {0.0....n}   |
+--------------------------+--------+-----------+-------------------------------------------------------------------------------------------------+--------------+
| costs_kWh                | float  | [$/kWh]   | Refers to the financial costs required to run the heating or cooling system.                    | {0.0....n}   |
+--------------------------+--------+-----------+-------------------------------------------------------------------------------------------------+--------------+

Emission Systems
^^^^^^^^^^^^^^^^
**Description**: This database stores information of HVAC systems in buildings. This database is useful to calculate the performance of different HVAC systems and control systems in buildings.

**Format/Naming**: excel file / emission_systems.xlsx

**Location (example)**: `` cea/databases/systems/emission_systems.xls``

**Primary Interdependencies**: Relates to the primary input database of Zone HVAC

**Secondary Interdependencies**: None

+--------------------------+--------+--------+-----------------------------------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit   | Description                                                                                                                 | Valid Values |
+==========================+========+========+=============================================================================================================================+==============+
| Description              | string | [-]    | Description of the typical supply and return temperatures related to HVAC, hot water and sanitation.                        | [-]          |
+--------------------------+--------+--------+-----------------------------------------------------------------------------------------------------------------------------+--------------+
| code                     | string | [-]    | Unique ID of component of the typical supply and return temperature bins.                                                   | {T1..Tn}     |
+--------------------------+--------+--------+-----------------------------------------------------------------------------------------------------------------------------+--------------+
| Tsww0_C                  | float  | [C]    | Typical supply water temperature.                                                                                           | {0.0....n}   |
+--------------------------+--------+--------+-----------------------------------------------------------------------------------------------------------------------------+--------------+
| Qwwmax_Wm2               | float  | [W/m2] | Maximum heat flow permitted by the distribution system per m2 of the exchange interface (e.g. floor/radiator heating area). | {0.0....n}   |
+--------------------------+--------+--------+-----------------------------------------------------------------------------------------------------------------------------+--------------+

Envelope Systems: Construction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information with detailed properties of components of the building envelope. This database is useful to calculate the thermal demand of energy in buildings.

**Format/Naming**: excel file / envelope_systems.xls

**Location (example)**: `` cea/databases/systems/envelope_systems.xlsx``

**Primary Interdependencies**: Relates to the primary input database of Zone architecture

**Secondary Interdependencies**: None

+--------------------------+--------+---------+------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit    | Description                                                                              | Valid Values |
+==========================+========+=========+==========================================================================================+==============+
| description              | string | [-]     | Description of component                                                                 | [-]          |
+--------------------------+--------+---------+------------------------------------------------------------------------------------------+--------------+
| code                     | string | [-]     | Unique ID of component in the construction category                                      | {T1..Tn}     |
+--------------------------+--------+---------+------------------------------------------------------------------------------------------+--------------+
| Cm_Af                    | float  | [J/Km2] | Internal heat capacity per unit of air conditioned area. Defined according to ISO 13790. | {0.0...1}    |
+--------------------------+--------+---------+------------------------------------------------------------------------------------------+--------------+

Envelope Systems: Leakage
^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information with detailed properties of components of the building envelope. This database is useful to calculate the thermal demand of energy in buildings.

**Format/Naming**: excel file / envelope_systems.xls

**Location (example)**: `` cea/databases/systems/envelope_systems.xlsx``

**Primary Interdependencies**: Relates to the primary input database of Zone architecture

**Secondary Interdependencies**: None

+--------------------------+--------+-------+------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit  | Description                                          | Valid Values |
+==========================+========+=======+======================================================+==============+
| description              | string | [-]   | Description of component                             | [-]          |
+--------------------------+--------+-------+------------------------------------------------------+--------------+
| code                     | string | [-]   | Unique ID of component in the leakage category       | {T1..Tn}     |
+--------------------------+--------+-------+------------------------------------------------------+--------------+
| n50                      | float  | [1/h] | Air exchanges due to leakage at a pressure of 50 Pa. | {0.0...n}    |
+--------------------------+--------+-------+------------------------------------------------------+--------------+

Envelope Systems: Window
^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information with detailed properties of components of the building envelope. This database is useful to calculate the thermal demand of energy in buildings.

**Format/Naming**: excel file / envelope_systems.xls

**Location (example)**: `` cea/databases/systems/envelope_systems.xlsx``

**Primary Interdependencies**: Relates to the primary input database of Zone architecture

**Secondary Interdependencies**: None

+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit | Description                                                                                      | Valid Values |
+==========================+========+======+==================================================================================================+==============+
| description              | string | [-]  | Description of component                                                                         | [-]          |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| code                     | string | [-]  | Unique ID of component in the window category                                                    | {T1..Tn}     |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| G_win                    | float  | [-]  | Solar heat gain coefficient. Defined according to ISO 13790.                                     | {0.0...1}    |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| e_win                    | float  | [-]  | Emissivity of external surface. Defined according to ISO 13790.                                  | {0.0...1}    |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| U_win                    | float  | [-]  | Thermal transmittance of windows including linear losses (+10%). Defined according to ISO 13790. | {0.1...n}    |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+

Envelope Systems: Roof
^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information with detailed properties of components of the building envelope. This database is useful to calculate the thermal demand of energy in buildings.

**Format/Naming**: excel file / envelope_systems.xls

**Location (example)**: `` cea/databases/systems/envelope_systems.xlsx``

**Primary Interdependencies**: Relates to the primary input database of Zone architecture

**Secondary Interdependencies**: 

+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit | Description                                                                                      | Valid Values |
+==========================+========+======+==================================================================================================+==============+
| description              | string | [-]  | Description of component                                                                         | [-]          |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| code                     | string | [-]  | Unique ID of component in the window category                                                    | {T1..Tn}     |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| a_roof                   | float  | [-]  | Solar absorption coefficient. Defined according to ISO 13790.                                    | {0.0...1}    |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| e_roof                   | float  | [-]  | Emissivity of external surface. Defined according to ISO 13790.                                  | {0.0...1}    |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| U_roof                   | float  | [-]  | Thermal transmittance of windows including linear losses (+10%). Defined according to ISO 13790. | {0.1...n}    |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+
| r_roof                   | float  | [-]  | Reflectance in the Red spectrum. Defined according Radiance. (long-wave)                         | {0.0...1}    |
+--------------------------+--------+------+--------------------------------------------------------------------------------------------------+--------------+

Envelope Systems: Wall
^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information with detailed properties of components of the building envelope. This database is useful to calculate the thermal demand of energy in buildings.

**Format/Naming**: excel file / envelope_systems.xls

**Location (example)**: `` cea/databases/systems/envelope_systems.xlsx``

**Primary Interdependencies**: Relates to the primary input database of Zone architecture

**Secondary Interdependencies**: 

+--------------------------+--------+------+---------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit | Description                                                                                       | Valid Values |
+==========================+========+======+===================================================================================================+==============+
| description              | string | [-]  | Description of component                                                                          | [-]          |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------+--------------+
| code                     | string | [-]  | Unique ID of component in the window category                                                     | {T1..Tn}     |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------+--------------+
| a_wall                   | float  | [-]  | Solar absorption coefficient. Defined according to ISO 13790.                                     | {0.0...1}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------+--------------+
| e_wall                   | float  | [-]  | Emissivity of external surface. Defined according to ISO 13790.                                   | {0.0...1}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------+--------------+
| U_wall                   | float  | [-]  | Thermal transmittance of windows including linear losses (+10%). Defined according to ISO 13790.  | {0.1...n}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------+--------------+
| r_wall                   | float  | [-]  | Reflectance in the Red spectrum. Defined according Radiance. (long-wave)                          | {0.0...1}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------+--------------+
| U_base                   | float  | [-]  | Thermal transmittance of basement including linear losses (+10%). Defined according to ISO 13790. | {0.0...1}    |
+--------------------------+--------+------+---------------------------------------------------------------------------------------------------+--------------+

Envelope Systems: Shading
^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information with detailed properties of components of the building envelope. This database is useful to calculate the thermal demand of energy in buildings.

**Format/Naming**: excel file / envelope_systems.xls

**Location (example)**: `` cea/databases/systems/envelope_systems.xlsx``

**Primary Interdependencies**: Relates to the primary input database of Zone architecture

**Secondary Interdependencies**: 

+--------------------------+--------+------+------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit | Description                                                                        | Valid Values |
+==========================+========+======+====================================================================================+==============+
| description              | string | [-]  | Description of component                                                           | [-]          |
+--------------------------+--------+------+------------------------------------------------------------------------------------+--------------+
| code                     | string | [-]  | Unique ID of component in the window category                                      | {T1...Tn}    |
+--------------------------+--------+------+------------------------------------------------------------------------------------+--------------+
| rf_sh                    | float  | [-]  | Shading coefficient when shading device is active. Defined according to ISO 13790. | {0.0...1}    |
+--------------------------+--------+------+------------------------------------------------------------------------------------+--------------+

Thermal Networks_Piping Catalog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information regarding the assumed pipe constraints, grouped into nominal diameter (DN) bins. The max/min volume flow rate is defined here, and provides limits for the permissable heat transmittance for the various heating and cooling systems.

**Format/Naming**: excel file / thermal_networks.xls

**Location (example)**: `` cea/databases/systems/thermal_networks.xls``

**Primary Interdependencies**: Relates to the demand and economic analysis.

**Secondary Interdependencies**: 

+--------------------------+--------+--------+--------------------------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit   | Description                                                                                                        | Valid Values |
+==========================+========+========+====================================================================================================================+==============+
| Pipe_DN                  | string | [DN#]  | Classifies nominal pipe diameters (DN) into typical bins. E.g. DN100 refers to pipes of approx. 100mm in diameter. | alphanumeric |
+--------------------------+--------+--------+--------------------------------------------------------------------------------------------------------------------+--------------+
| D_ext_m                  | float  | [m]    | Defines the maximum pipe diameter tolerance for the nominal diameter (DN) bin.                                     | {0.0...n}    |
+--------------------------+--------+--------+--------------------------------------------------------------------------------------------------------------------+--------------+
| D_int_m                  | float  | [m]    | Defines the minimum pipe diameter tolerance for the nominal diameter (DN) bin.                                     | {0.0...n}    |
+--------------------------+--------+--------+--------------------------------------------------------------------------------------------------------------------+--------------+
| D_ins_m                  | float  | [m]    | Defines the pipe insulation diameter for the nominal diameter (DN) bin.                                            | {0.0...n}    |
+--------------------------+--------+--------+--------------------------------------------------------------------------------------------------------------------+--------------+
| Vdot_min_m3s             | float  | [m3/s] | Minimum volume flow rate for the nominal diameter (DN) bin.                                                        | {0.0...n}    |
+--------------------------+--------+--------+--------------------------------------------------------------------------------------------------------------------+--------------+
| Vdot_max_m3s             | float  | [m3/s] | Maximum volume flow rate for the nominal diameter (DN) bin.                                                        | {0.0...n}    |
+--------------------------+--------+--------+--------------------------------------------------------------------------------------------------------------------+--------------+

Thermal Networks_Material Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores the information used when calculating financial and thermal properties of the districts thermal network.

**Format/Naming**: excel file / thermal_networks.xls

**Location (example)**: `` cea/databases/systems/thermal_networks.xls``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+---------+-------------------------------------------+--------------+
| Column names /parameters | Type   | Unit    | Description                               | Valid Values |
+==========================+========+=========+===========================================+==============+
| Material                 | string | [-]     | Material                                  | [-]          |
+--------------------------+--------+---------+-------------------------------------------+--------------+
| Code                     | string | [-]     | Unique code for the material of the pipe. | [-]          |
+--------------------------+--------+---------+-------------------------------------------+--------------+
| lambda_WmK               | float  | [W/mK]  | Thermal conductivity                      | {0.0...n}    |
+--------------------------+--------+---------+-------------------------------------------+--------------+
| rho_kgm3                 | float  | [kg/m3] | Density of transmission fluid.            | {0.0...n}    |
+--------------------------+--------+---------+-------------------------------------------+--------------+
| Cp_JkgK                  | float  | [J/kgK] | Heat capacity of transmission fluid.      | {0.0...n}    |
+--------------------------+--------+---------+-------------------------------------------+--------------+

Uncertainty Distributions
^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores information of probability density functions of several input parameters of the CEA tool. This database is useful to perform a sensitivity analysis of input parameters and to calibrate to measured data.

**Format/Naming**: excel file / uncertainty_distributions.xlsx

**Location (example)**: `` .../cea/databases/uncertainty/uncertainty_distributions.xlsx``

**Primary Interdependencies**: Relates detailed data to the secondary input database of architecture through the contents of the default database of envelope_systems. It also relates detailed data to the secondary input databases of internal_loads and indoor_comfort

**Secondary Interdependencies**: None

+--------------------------+--------+------+--------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit | Description                                      | Valid Values |
+==========================+========+======+==================================================+==============+
| name                     | string | [-]  | Unique building ID. It must start with a letter. | alphanumeric |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| distribution             | string | [-]  | Type of distribution                             | {0.0...n}    |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| mu                       | float  | [-]  | Mu value                                         | {0.0...n}    |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| stdv                     | float  | [-]  | Standard Deviation                               | {0.0...n}    |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| min                      | float  | [-]  | Minimum                                          | {0.0...n}    |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| max                      | float  | [-]  | Maximum                                          | {0.0...n}    |
+--------------------------+--------+------+--------------------------------------------------+--------------+
| reference                | string | [-]  |                                                  |              |
+--------------------------+--------+------+--------------------------------------------------+--------------+


Output Databases
----------------
Demand: Zone
^^^^^^^^^^^^
**Description**: These databases store the heating/cooling demand and various operating temperatures for each building in hourly time stamps. Each group of variables is calculated using a specific modules from ``cea\demand`` and is stored within the scenario directory using demand_writer.

**Format/Naming**: csv file / B01.csv

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/demand/B01.csv``

**Primary Interdependencies**: Calculated using the demand modules which get data from the primary input and default.

**Secondary Interdependencies**: Relates to the operating costs for the LCA as well as costs vs CO2 and network optimisations.

+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Column names /parameters | Type   | Unit            | Description                                                      | Valid Values        |
+==========================+========+=================+==================================================================+=====================+
| COAL_hs_kWh              | float  | [kWh]           | Coal consumption due to space heating                            | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| COAL_ww_kWh              | float  | [kWh]           | Coal consumption due to hotwater                                 | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| DATE                     | date   | [smalldatetime] | Time stamp for each day of the year ascending in hour intervals. | YYYY-MM-DD hh:mm:ss |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| DC_cdata_kWh             | float  | [kWh]           | District cooling for data center cooling demand                  | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| DC_cre_kWh               | float  | [kWh]           | District cooling for refrigeration demand                        | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| DC_cs_kWh                | float  | [kWh]           | District cooling for space cooling demand                        | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| DH_hs_kWh                | float  | [kWh]           | District heating for space heating demand                        | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| DH_ww_kWh                | float  | [kWh]           | District heating for hotwater demand                             | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| E_cdata_kWh              | float  | [kWh]           | Data centre cooling specific electricity consumption.            | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| E_cre_kWh                | float  | [kWh]           | Refridgeration system electricity consumption.                   | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| E_cs_kWh                 | float  | [kWh]           | Cooling system electricity consumption.                          | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| E_hs_kWh                 | float  | [kWh]           | Heating system electricity consumption.                          | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| E_sys_kWh                | float  | [kWh]           | End-use electricity demand                                       | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| E_ww_kWh                 | float  | [kWh]           | Hot water electricity consumption.                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Eal_kWh                  | float  | [kWh]           | Total net electricity for all sources and sinks ??               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Eaux_kWh                 | float  | [kWh]           | Auxiliary electricity consumption.                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Edata_kWh                | float  | [kWh]           | Data centre electricity consumption.                             | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Epro_kWh                 | float  | [kWh]           | Electricity production.                                          | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| GRID_kWh                 | float  | [kWh]           | Grid electricity consumption                                     | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| I_rad_kWh                | float  | [kWh]           | Radiative heat loss                                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| I_sol_and_I_rad_kWh      | float  | [kWh]           | Combined solar heat gain and radiative heat loss                 | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| I_sol_kWh                | float  | [kWh]           | Solar heat gain                                                  | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcpcdata_sys_kWperC      | float  | [kW/Cap]        | Cooling power delivered to the data centre.                      | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcpcre_sys_kWperC        | float  | [kW/Cap]        | Cooling power delivered to the refridgeration system             | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcpcs_sys_ahu_kWperC     | float  | [kW/Cap]        | Cooling power delivered via the AHU                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcpcs_sys_aru_kWperC     | float  | [kW/Cap]        | Cooling power delivered via the ARU                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcpcs_sys_kWperC         | float  | [kW/Cap]        | system cooling power delivered via all cooling system            | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcpcs_sys_scu_kWperC     | float  | [kW/Cap]        | Cooling power delivered via the SCU                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcphs_sys_ahu_kWperC     | float  | [kW/Cap]        | Heating power delivered via the AHU                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcphs_sys_aru_kWperC     | float  | [kW/Cap]        | Heating power delivered via the ARU                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcphs_sys_kWperC         | float  | [kW/Cap]        | system heating power delivered via all heating system            | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcphs_sys_shu_kWperC     | float  | [kW/Cap]        | Heating power delivered via the SCU                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcptw_kWperC             | float  | [kW/Cap]        | Heating power delivered via the domestic hot water channels ??   | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| mcpww_sys_kWperC         | float  | [kW/Cap]        | Heating power delivered via the DWH channels ??                  | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Name                     | string | [-]             | Unique building ID. It must start with a letter.                 | alphanumeric        |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| NG_hs_kWh                | float  | [kWh]           | NG consumption due to space heating                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| NG_ww_kWh                | float  | [kWh]           | NG consumption due to hotwater                                   | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| OIL_hs_kWh               | float  | [kWh]           | OIL consumption due to space heating                             | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| OIL_ww_kWh               | float  | [kWh]           | OIL consumption due to hotwater                                  | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| people                   | int    | [people]        | Predicted occupancy                                              | {0...n}             |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| PV_kWh                   | float  | [kWh]           | PV electricity consumption                                       | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_lat_peop_kWh      | float  | [kWh]           | Latent heat gain from people                                     | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_app_kWh       | float  | [kWh]           | Sensible heat gain from appliances                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_base_kWh      | float  | [kWh]           | Sensible heat gain from transmission through the base            | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_data_kWh      | float  | [kWh]           | Sensible heat gain from data centres                             | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_light_kWh     | float  | [kWh]           | Sensible heat gain from lighting                                 | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_peop_kWh      | float  | [kWh]           | Sensible heat gain from people                                   | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_pro_kWh       | float  | [kWh]           |                                                                  | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_roof_kWh      | float  | [kWh]           | Sensible heat gain from transmission through the roof            | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_vent_kWh      | float  | [kWh]           | Sensible heat gain from ventilation and infiltration             | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_wall_kWh      | float  | [kWh]           | Sensible heat gain from transmission through the walls           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_gain_sen_wind_kWh      | float  | [kWh]           | Sensible heat gain from transmission through the windows         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Q_loss_sen_ref_kWh       | float  | [kWh]           | Sensible heat loss from refrigeration systems                    | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| QC_sys_kWh               | float  | [kWh]           | Total cool consumption                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcdata_kWh               | float  | [kWh]           | Data centre space cooling demand                                 | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcdata_sys_kWh           | float  | [kWh]           | End-use data center cooling demand                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcre_kWh                 | float  | [kWh]           | Refirdgeration space cooling demand                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcre_sys_kWh             | float  | [kWh]           | End-use refrigeration demand                                     | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_dis_ls_kWh           | float  | [kWh]           | Heat distribution losses                                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_em_ls_kWh            | float  | [kWh]           | Heat emission losses                                             | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_kWh                  | float  | [kWh]           | Specific cool demand                                             | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_lat_ahu_kWh          | float  | [kWh]           | AHU latent cool demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_lat_aru_kWh          | float  | [kWh]           | ARU latent cool demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_lat_sys_kWh          | float  | [kWh]           | Total latent cool demand for all systems                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_sen_ahu_kWh          | float  | [kWh]           | AHU sensible cool demand                                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_sen_aru_kWh          | float  | [kWh]           | ARU sensible cool demand                                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_sen_scu_kWh          | float  | [kWh]           | SHU sensible cool demand                                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_sen_sys_kWh          | float  | [kWh]           | Total sensible cool demand for all systems                       | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_sys_ahu_kWh          | float  | [kWh]           | AHU system cool demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_sys_aru_kWh          | float  | [kWh]           | ARU system cool demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_sys_kWh              | float  | [kWh]           | End-use space cooling demand                                     | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qcs_sys_scu_kWh          | float  | [kWh]           | SCU system cool demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| QH_sys_kWh               | float  | [kWh]           | Total heat consumption                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhpro_sys_kWh            | float  | [kWh]           |                                                                  | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_dis_ls_kWh           | float  | [kWh]           | Heat distribution losses                                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_em_ls_kWh            | float  | [kWh]           | Heat emission losses                                             | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_kWh                  | float  | [kWh]           | Sensible heating system demand                                   | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_lat_ahu_kWh          | float  | [kWh]           | AHU latent heat demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_lat_aru_kWh          | float  | [kWh]           | ARU latent heat demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_lat_sys_kWh          | float  | [kWh]           | Total latent heat demand for all systems                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_sen_ahu_kWh          | float  | [kWh]           | AHU sensible heat demand                                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_sen_aru_kWh          | float  | [kWh]           | ARU sensible heat demand                                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_sen_shu_kWh          | float  | [kWh]           | SHU sensible heat demand                                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_sen_sys_kWh          | float  | [kWh]           | Total sensible heat demand for all systems                       | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_sys_ahu_kWh          | float  | [kWh]           | AHU system heat demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_sys_aru_kWh          | float  | [kWh]           | ARU system heat demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_sys_kWh              | float  | [kWh]           | End-use space heating demand                                     | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qhs_sys_shu_kWh          | float  | [kWh]           | SHU system heat demand                                           | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qww_kWh                  | float  | [kWh]           | Hot water specific heat demand                                   | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Qww_sys_kWh              | float  | [kWh]           | End-use hotwater demand                                          | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| SOLAR_hs_kWh             | float  | [kWh]           | Solar energy consumption due to space heating                    | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| SOLAR_ww_kWh             | float  | [kWh]           | Solar energy consumption due to hotwater                         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| T_ext_C                  | float  | [C]             | Outdoor temperature                                              | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| T_int_C                  | float  | [C]             | Indoor temperature                                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcdata_sys_re_C          | float  | [C]             | Cooling supply temperature of the data centre                    | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcdata_sys_sup_C         | float  | [C]             | Cooling return temperature of the data centre                    | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcre_sys_re_C            | float  | [C]             | Cooling return temperature of the refridgeration system.         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcre_sys_sup_C           | float  | [C]             | Cooling supply temperature of the refridgeration system.         | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcs_sys_re_ahu_C         | float  | [C]             | Return temperature cooling system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcs_sys_re_aru_C         | float  | [C]             | Return temperature cooling system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcs_sys_re_C             | float  | [C]             | System cooling return temperature.                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcs_sys_re_scu_C         | float  | [C]             | Return temperature cooling system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcs_sys_sup_ahu_C        | float  | [C]             | Supply temperature cooling system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcs_sys_sup_aru_C        | float  | [C]             | Supply temperature cooling system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcs_sys_sup_C            | float  | [C]             | System cooling supply temperature.                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tcs_sys_sup_scu_C        | float  | [C]             | Supply temperature cooling system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| theta_o_C                | float  | [C]             |                                                                  | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Ths_sys_re_ahu_C         | float  | [C]             | Return temperature heating system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Ths_sys_re_aru_C         | float  | [C]             | Return temperature heating system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Ths_sys_re_C             | float  | [C]             | System heating return temperature.                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Ths_sys_re_shu_C         | float  | [C]             | Return temperature heating system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Ths_sys_sup_ahu_C        | float  | [C]             | Supply temperature heating system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Ths_sys_sup_aru_C        | float  | [C]             | Supply temperature heating system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Ths_sys_sup_C            | float  | [C]             | System heating supply temperature.                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Ths_sys_sup_shu_C        | float  | [C]             | Supply temperature heating system                                | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tww_sys_re_C             | float  | [C]             | Return temperature hotwater system                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| Tww_sys_sup_C            | float  | [C]             | Supply temperature hotwater system                               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| WOOD_hs_kWh              | float  | [kWh]           | WOOD consumption due to space heating                            | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| WOOD_ww_kWh              | float  | [kWh]           | WOOD consumption due to hotwater                                 | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+
| x_int                    | float  | [kg/kg]         | Internal mass fraction of humidity (vapor/dry air)               | {0.0...n}           |
+--------------------------+--------+-----------------+------------------------------------------------------------------+---------------------+

Demand: District
^^^^^^^^^^^^^^^^
**Description**: This database stores the gross floor, conditioned floor and roof areas as well as the heating/cooling demand and occupancy of the district (aggregated for each building). Each group of variables is calculated using a specific module from ``cea\demand`` and is stored within the scenario directory using demand_writer module. Note: Any variable which contains a zero, is derived from the baseline scenario.

**Format/Naming**: csv file / B01.csv

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/demand/B01.csv``

**Primary Interdependencies**: Calculated using the demand modules which get data from the input databases.

**Secondary Interdependencies**: Relates to the operating costs for the LCA as well as costs vs CO2 and network optimisations.

+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit       | Description                                                   | Valid Values |
+==========================+========+============+===============================================================+==============+
| Af_m2                    | float  | [m2]       | Conditioned floor area (heated/cooled)                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Aroof_m2                 | float  | [m2]       | Roof area                                                     | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| COAL_hs_MWhyr            | float  | [MWh/year] | Coal consumption due to space heating                         | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| COAL_hs0_kW              | float  | [kW/year]  | Nominal Coal consumption due to space heating                 | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| COAL_ww_MWhyr            | float  | [MWh/year] | Coal consumption due to hotwater                              | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| COAL_ww0_kW              | float  | [kW/year]  | Nominal Coal consumption due to hotwater                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DC_cdata_MWhyr           | float  | [MWh/year] | District cooling for data center cooling demand               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DC_cdata0_kW             | float  | [kW/year]  | Nominal district cooling for final data center cooling demand | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DC_cre_MWhyr             | float  | [MWh/year] | District cooling for refrigeration demand                     | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DC_cre0_kW               | float  | [kW/year]  | Nominal district cooling for refrigeration demand             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DC_cs_MWhyr              | float  | [MWh/year] | District cooling for space cooling demand                     | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DC_cs0_kW                | float  | [kW/year]  | Nominal district cooling for space cooling demand             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DH_hs_MWhyr              | float  | [MWh/year] | District heating for space heating demand                     | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DH_hs0_kW                | float  | [kW/year]  | Nominal district heating for space heating demand             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DH_ww_MWhyr              | float  | [MWh/year] | District heating for hotwater demand                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| DH_ww0_kW                | float  | [kW/year]  | Nominal district heating for hotwater demand                  | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_cdata_MWhyr            | float  | [MWh/year] | Data centre cooling specific electricity consumption.         | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_cdata0_kW              | float  | [kW/year]  | Nominal Data centre cooling specific electricity consumption. | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_cre_MWhyr              | float  | [MWh/year] | Refridgeration system electricity consumption.                | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_cre0_kW                | float  | [kW/year]  | Nominal Refridgeration system electricity consumption.        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_cs_MWhyr               | float  | [MWh/year] | Cooling system electricity consumption.                       | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_cs0_kW                 | float  | [kW/year]  | Nominal Cooling system electricity consumption.               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_hs_MWhyr               | float  | [MWh/year] | Heating system electricity consumption.                       | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_hs0_kW                 | float  | [kW/year]  | Nominal Heating system electricity consumption.               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_sys_MWhyr              | float  | [MWh/year] | End-use electricity demand                                    | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_sys0_kW                | float  | [kW/year]  | Nominal end-use electricity demand                            | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_ww_MWhyr               | float  | [MWh/year] | Domestic hot water electricity consumption.                   | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| E_ww0_kW                 | float  | [kW/year]  | Nominal Domestic hot water electricity consumption.           | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Eal_MWhyr                | float  | [MWh/year] | Total net electricity for all sources and sinks               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Eal0_kW                  | float  | [kW/year]  | Nominal Total net electricity for all sources and sinks.      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Eaux_MWhyr               | float  | [MWh/year] | Auxiliary electricity consumption.                            | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Eaux0_kW                 | float  | [kW/year]  | Nominal Auxiliary electricity consumption.                    | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Edata_MWhyr              | float  | [MWh/year] | Data centre electricity consumption.                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Edata0_kW                | float  | [kW/year]  | Nominal Data centre electricity consumption.                  | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Epro_MWhyr               | float  | [MWh/year] | Electricity production.                                       | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Epro0_kW                 | float  | [kW/year]  | Nominal Electricity production.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| GFA_m2                   | float  | [m2]       | Gross floor area                                              | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| GRID_MWhyr               | float  | [MWh/year] | Grid electricity consumption                                  | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| GRID0_kW                 | float  | [kW/year]  | Nominal Grid electricity consumption                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Name                     | string | [-]        | Unique building ID. It must start with a letter.              | alphanumeric |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| NG_hs_MWhyr              | float  | [MWh/year] | NG consumption due to space heating                           | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| NG_hs0_kW                | float  | [kW/year]  | Nominal NG consumption due to space heating                   | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| NG_ww_MWhyr              | float  | [MWh/year] | NG consumption due to hotwater                                | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| NG_ww0_kW                | float  | [kW/year]  | Nominal NG consumption due to hotwater                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| OIL_hs_MWhyr             | float  | [MWh/year] | OIL consumption due to space heating                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| OIL_hs0_kW               | float  | [kW/year]  | Nominal OIL consumption due to space heating                  | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| OIL_ww_MWhyr             | float  | [MWh/year] | OIL consumption due to hotwater                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| OIL_ww0_kW               | float  | [kW/year]  | Nominal OIL consumption due to hotwater                       | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| people0                  | int    | [people]   | Predicted occupancy                                           | {0...n}      |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| PV_MWhyr                 | float  | [MWh/year] | PV electricity consumption                                    | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| PV0_kW                   | float  | [kW/year]  | Nominal PV electricity consumption                            | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| QC_sys_MWhyr             | float  | [MWh/year] | Total system cooling demand                                   | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| QC_sys0_kW               | float  | [kW/year]  | Nominal Total system cooling demand.                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcdata_MWhyr             | float  | [MWh/year] | Data centre cooling demand                                    | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcdata_sys_MWhyr         | float  | [MWh/year] | End-use data center cooling demand                            | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcdata_sys0_kW           | float  | [kW/year]  | Nominal end-use data center cooling demand                    | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcdata0_kW               | float  | [kW/year]  | Nominal Data centre cooling demand.                           | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcre_MWhyr               | float  | [MWh/year] | Refridgeration cooling demand for the system                  | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcre_sys_MWhyr           | float  | [MWh/year] | End-use refrigeration demand                                  | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcre_sys0_kW             | float  | [kW/year]  | Nominal refrigeration cooling demand                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcre0_kW                 | float  | [kW/year]  | Nominal Refridgeration cooling demand.                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_dis_ls_MWhyr         | float  | [MWh/year] | Cool distribution losses                                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_dis_ls0_kW           | float  | [kW/year]  | Nominal Cool distribution losses.                             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_em_ls_MWhyr          | float  | [MWh/year] | Cool emission losses                                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_em_ls0_kW            | float  | [kW/year]  | Nominal Cool emission losses.                                 | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_lat_ahu_MWhyr        | float  | [MWh/year] | AHU latent cool demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_lat_ahu0_kW          | float  | [kW/year]  | Nominal AHU latent cool demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_lat_aru_MWhyr        | float  | [MWh/year] | ARU latent cool demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_lat_aru0_kW          | float  | [kW/year]  | Nominal ARU latent cool demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_lat_sys_MWhyr        | float  | [MWh/year] | System latent cool demand                                     | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_lat_sys0_kW          | float  | [kW/year]  | Nominal System latent cool demand.                            | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_MWhyr                | float  | [MWh/year] | Total cool demand                                             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sen_ahu_MWhyr        | float  | [MWh/year] | AHU system cool demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sen_ahu0_kW          | float  | [kW/year]  | Nominal AHU system cool demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sen_aru_MWhyr        | float  | [MWh/year] | ARU system cool demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sen_aru0_kW          | float  | [kW/year]  | Nominal ARU system cool demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sen_scu_MWhyr        | float  | [MWh/year] | SCU system cool demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sen_scu0_kW          | float  | [kW/year]  | Nominal SCU system cool demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sen_sys_MWhyr        | float  | [MWh/year] | Sensible system cool demand                                   | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sen_sys0_kW          | float  | [kW/year]  | Nominal Sensible system cool demand.                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sys_ahu_MWhyr        | float  | [MWh/year] | AHU system cool demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sys_ahu0_kW          | float  | [kW/year]  | Nominal AHU system cool demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sys_aru_MWhyr        | float  | [MWh/year] | ARU system cool demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sys_aru0_kW          | float  | [kW/year]  | Nominal ARU system cool demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sys_MWhyr            | float  | [MWh/year] | End-use space cooling demand                                  | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sys_scu_MWhyr        | float  | [MWh/year] | SCU system cool demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sys_scu0_kW          | float  | [kW/year]  | Nominal SCU system cool demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs_sys0_kW              | float  | [kW/year]  | Nominal end-use space cooling demand                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qcs0_kW                  | float  | [kW/year]  | Nominal Total cooling demand.                                 | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| QH_sys_MWhyr             | float  | [MWh/year] | District system heating demand                                | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| QH_sys0_kW               | float  | [kW/year]  | Nominal District system heating demand.                       | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhpro_sys_MWhyr          | float  | [MWh/year] | System heat production                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhpro_sys0_kW            | float  | [kW/year]  | Nominal System heat production.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_dis_ls_MWhyr         | float  | [MWh/year] | Heat distribution losses                                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_dis_ls0_kW           | float  | [kW/year]  | Nominal Heat distribution losses.                             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_em_ls_MWhyr          | float  | [MWh/year] | Heat emission losses                                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_em_ls0_kW            | float  | [kW/year]  | Nominal Heat emission losses.                                 | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_lat_ahu_MWhyr        | float  | [MWh/year] | AHU latent heat demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_lat_ahu0_kW          | float  | [kW/year]  | Nominal AHU latent heat demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_lat_aru_MWhyr        | float  | [MWh/year] | ARU latent heat demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_lat_aru0_kW          | float  | [kW/year]  | Nominal ARU latent heat demand.                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_lat_sys_MWhyr        | float  | [MWh/year] | System latent heat demand                                     | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_lat_sys0_kW          | float  | [kW/year]  | Nominal System latent heat demand.                            | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_MWhyr                | float  | [MWh/year] | Total heating demand                                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sen_ahu_MWhyr        | float  | [MWh/year] | AHU sensible heat demand                                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sen_ahu0_kW          | float  | [kW/year]  | Nominal AHU sensible heat demand.                             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sen_aru_MWhyr        | float  | [MWh/year] | ARU sensible heat demand                                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sen_aru0_kW          | float  | [kW/year]  | ARU sensible heat demand                                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sen_shu_MWhyr        | float  | [MWh/year] | SHU sensible heat demand                                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sen_shu0_kW          | float  | [kW/year]  | Nominal SHU sensible heat demand.                             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sen_sys_MWhyr        | float  | [MWh/year] | SHU sensible heat demand                                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sen_sys0_kW          | float  | [kW/year]  | Nominal HVAC systems sensible heat demand.                    | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sys_ahu_MWhyr        | float  | [MWh/year] | AHU system heat demand                                        | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sys_ahu0_kW          | float  | [kW/year]  | Nominal AHU sensible heat demand.                             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sys_aru_MWhyr        | float  | [MWh/year] | ARU sensible heat demand                                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sys_aru0_kW          | float  | [kW/year]  | Nominal ARU sensible heat demand.                             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sys_MWhyr            | float  | [MWh/year] | End-use space heating demand                                  | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sys_shu_MWhyr        | float  | [MWh/year] | SHU sensible heat demand                                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sys_shu0_kW          | float  | [kW/year]  | Nominal SHU sensible heat demand.                             | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs_sys0_kW              | float  | [kW/year]  | Nominal end-use space heating demand                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qhs0_kW                  | float  | [kW/year]  | Nominal Total heating demand.                                 | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qww_MWhyr                | float  | [MWh/year] | Hot waterheat demand                                          | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qww_sys_MWhyr            | float  | [MWh/year] | End-use hotwater demand                                       | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qww_sys0_kW              | float  | [kW/year]  | Nominal end-use hotwater demand                               | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| Qww0_kW                  | float  | [kW/year]  | Nominal hot water heat demand.                                | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| SOLAR_hs_MWhyr           | float  | [MWh/year] | Solar energy consumption due to space heating                 | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| SOLAR_hs0_kW             | float  | [kW/year]  | Nominal solar energy consumption due to space heating         | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| SOLAR_ww_MWhyr           | float  | [MWh/year] | Solar energy consumption due to hotwater                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| SOLAR_ww0_kW             | float  | [kW/year]  | Nominal solar energy consumption due to hotwater              | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| WOOD_hs_MWhyr            | float  | [MWh/year] | WOOD consumption due to space heating                         | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| WOOD_hs0_kW              | float  | [kW/year]  | Nominal WOOD consumption due to space heating                 | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| WOOD_ww_MWhyr            | float  | [MWh/year] | WOOD consumption due to hotwater                              | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+
| WOOD_ww0_kW              | float  | [kW/year]  | Nominal WOOD consumption due to hotwater                      | {0.0...n}    |
+--------------------------+--------+------------+---------------------------------------------------------------+--------------+

Solar Radiation: geometry
^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: 

**Format/Naming**: 

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/solar-radiation/B01.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| Column names /parameters | Type   | Unit | Description                                                  | Valid Values            |
+==========================+========+======+==============================================================+=========================+
| AREA_m2                  | float  | [m2] | Surface area.                                                | {0.0...n}               |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| BUILDING                 | string | [-]  | Unique building ID. It must start with a letter.             | alphanumeric            |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| SURFACE                  | string | [-]  | Unique surface ID for each building exterior surface.        | {srf0...srfn}           |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| TYPE                     | string | [-]  | Surface typology.                                            | {walls, windows, roofs} |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| Xcoor                    | float  | [-]  | Describes the position of the x vector.                      | {0.0...n}               |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| Xdir                     | float  | [-]  | Directional scalar of the x vector.                          | {-1...1}                |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| Ycoor                    | float  | [-]  | Describes the position of the y vector.                      | {0.0...n}               |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| Ydir                     | float  | [-]  | Directional scalar of the y vector.                          | {-1...1}                |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| Zcoor                    | float  | [-]  | Describes the position of the z vector.                      | {0.0...n}               |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| Zdir                     | int    | [-]  | Directional scalar of the z vector.                          | {-1...1}                |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+
| orientation              | string | [-]  | Orientation of the surface (north, east, south, west or top) | {north...}              |
+--------------------------+--------+------+--------------------------------------------------------------+-------------------------+

Solar Radiation: surface_properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores the aggregated and averaged geometric properties of the north, east, south and west walls for each building. Therefore, each building has four dedicated rows attibuted each variable listed.

**Format/Naming**: csv file / properties_surfaces.csv

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/solar-radiation/properties_surfaces.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+---------+-------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit    | Description                                                 | Valid Values |
+==========================+========+=========+=============================================================+==============+
| Name                     | string | [-]     | Unique building ID. It must start with a letter.            | alphanumeric |
+--------------------------+--------+---------+-------------------------------------------------------------+--------------+
| Freeheight               | float  | [m]     | Surface height exposed to the sun                           | {0.0...n}    |
+--------------------------+--------+---------+-------------------------------------------------------------+--------------+
| FactorShade              | float  | [ratio] | Defines whether surface is facing the sun (1) or not (0)    | {0.0...1}    |
+--------------------------+--------+---------+-------------------------------------------------------------+--------------+
| height_ag                | float  | [m]     | Aggregated height of the walls.                             | {0.0...n}    |
+--------------------------+--------+---------+-------------------------------------------------------------+--------------+
| Shape_Leng               | float  | [m]     | Surface length                                              | {0.0...n}    |
+--------------------------+--------+---------+-------------------------------------------------------------+--------------+
| Awall_all                | float  | [m2]    | Total aggregated height of the walls, inclusive of windows. | {0.0...n}    |
+--------------------------+--------+---------+-------------------------------------------------------------+--------------+

Solar Radiation: radiation
^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: This database stores the total solar insolation for each building for each time step.

**Format/Naming**: csv file / radiation.csv

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/solar-radiation/radiation.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+---------+--------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit    | Description                                      | Valid Values |
+==========================+========+=========+==================================================+==============+
| Name                     | string | [-]     | Unique building ID. It must start with a letter. | alphanumeric |
+--------------------------+--------+---------+--------------------------------------------------+--------------+
| T1...T8760               | float  | [Wh/m2] | Solar insolation for each hourly time step.      | {0.01...n}   |
+--------------------------+--------+---------+--------------------------------------------------+--------------+

Total_LCA_embodied
^^^^^^^^^^^^^^^^^^
**Description**: 

**Format/Naming**: 

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/data/emissions/Total_LCA_embodied.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+-------------+-----------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit        | Description                                                                       | Valid Values |
+==========================+========+=============+===================================================================================+==============+
| Name                     | string | [-]         | Unique building ID. It must start with a letter.                                  | alphanumeric |
+--------------------------+--------+-------------+-----------------------------------------------------------------------------------+--------------+
| GFA_m2                   | float  | [m2]        | Gross floor area                                                                  | {0.0...n}    |
+--------------------------+--------+-------------+-----------------------------------------------------------------------------------+--------------+
| E_nre_pen_GJ             | float  | [GJ/yr]     | Embodied primary energy demand (no-renewable )                                    | {0.0...n}    |
+--------------------------+--------+-------------+-----------------------------------------------------------------------------------+--------------+
| E_nre_pen_MJm2           | float  | [MJ/m2-yr]  | Embodied primary energy dmeand per unit of conditioned floor area (non-renewable) | {0.0...n}    |
+--------------------------+--------+-------------+-----------------------------------------------------------------------------------+--------------+
| E_ghg_ton                | float  | [ton/yr]    | Emissions due to Embodied energy                                                  | {0.0...n}    |
+--------------------------+--------+-------------+-----------------------------------------------------------------------------------+--------------+
| E_ghg_kgm2               | float  | [kg/m2 -yr] | Emissions due to Embodied energy per unit of conditioned floor area               | {0.0...n}    |
+--------------------------+--------+-------------+-----------------------------------------------------------------------------------+--------------+

Total_LCA_mobility
^^^^^^^^^^^^^^^^^^
**Description**: 

**Format/Naming**: 

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/data/emissions/Total_LCA_mobility.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+-------------+---------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit        | Description                                                                           | Valid Values |
+==========================+========+=============+=======================================================================================+==============+
| Name                     | string | [-]         | Unique building ID. It must start with a letter.                                      | alphanumeric |
+--------------------------+--------+-------------+---------------------------------------------------------------------------------------+--------------+
| GFA_m2                   | float  | [m2]        | Gross floor area                                                                      | {0.0...n}    |
+--------------------------+--------+-------------+---------------------------------------------------------------------------------------+--------------+
| M_nre_pen_GJ             | float  | [GJ/yr]     | Primary energy demand (non-renewable) for mobility                                    | {0.0...n}    |
+--------------------------+--------+-------------+---------------------------------------------------------------------------------------+--------------+
| M_nre_pen_MJm2           | float  | [MJ/m2-yr]  | Primary energy demand for mobility per unit of conditioned floor area (non-renewable) | {0.0...n}    |
+--------------------------+--------+-------------+---------------------------------------------------------------------------------------+--------------+
| M_ghg_ton                | float  | [ton/yr]    | Emissions due to energy for mobility                                                  | {0.0...n}    |
+--------------------------+--------+-------------+---------------------------------------------------------------------------------------+--------------+
| M_ghg_kgm2               | float  | [kg/m2 -yr] | Emissions due to energy for mobility per unti of conditioned floor area               | {0.0...n}    |
+--------------------------+--------+-------------+---------------------------------------------------------------------------------------+--------------+

Total_LCA_Operation
^^^^^^^^^^^^^^^^^^^
**Description**: 

**Format/Naming**: 

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/data/emissions/Total_LCA_operation.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| Column names /parameters | Type   | Unit        | Description                                                                                                                   | Valid Values |
+==========================+========+=============+===============================================================================================================================+==============+
| Name                     | string | [-]         | Unique building ID. It must start with a letter.                                                                              | alphanumeric |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| GFA_m2                   | float  | [m2]        | Gross floor area                                                                                                              | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| PV_ghg_ton               | float  | [ton/yr]    | Emissions due to operational energy of the PV-System                                                                          | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| PV_ghg_kgm2              | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area for PV-System                                          | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| PV_nre_pen_GJ            | float  | [GJ/yr]     | Primary energy demand (non-renewable) for PV-System                                                                           | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| PV_nre_pen_MJm2          | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) for PV System                                        | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| GRID_nre_pen_GJ          | float  | [GJ/yr]     | Primary energy demand (non-renewable) grid                                                                                    | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| GRID_ghg_ton             | float  | [ton/yr]    | Emissions due to operational energy of the electrictiy from the grid                                                          | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| GRID_nre_pen_MJm2        | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) from grid electricity                                | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| GRID_ghg_kgm2            | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area from grid electricity                                  | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cs_nre_pen_GJ         | float  | [GJ/yr]     | Primary energy demand (non-renewable) for district cooling system                                                             | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cs_ghg_ton            | float  | [ton/yr]    | Emissions due to operational energy of the district cooling                                                                   | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cs_nre_pen_MJm2       | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the district cooling                              | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cs_ghg_kgm2           | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the district cooling                                | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cdata_nre_pen_GJ      | float  | [GJ/yr]     | Primary energy demand (non-renewable) for district cooling system of the data center                                          | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cdata_ghg_ton         | float  | [ton/yr]    | Emissions due to operational energy of the district cooling for the data center                                               | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cdata_nre_pen_MJm2    | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the dstrict cooling for the data center           | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cdata_ghg_kgm2        | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the district cooling for the data center            | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cre_nre_pen_GJ        | float  | [GJ/yr]     | Primary energy demand (non-renewable) for district cooling system for cooling and refrigeration                               | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cre_ghg_ton           | float  | [ton/yr]    | Emissions due to operational energy of the district cooling for the cooling and refrigeration                                 | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cre_nre_pen_MJm2      | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the dstrict cooling for cooling and refrigeration | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DC_cre_ghg_kgm2          | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the district cooling for cooling and refrigeration  | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DH_hs_nre_pen_GJ         | float  | [GJ/yr]     | Primary energy demand (non-renewable) for district heating system                                                             | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DH_hs_ghg_ton            | float  | [ton/yr]    | Emissions due to operational energy of the district heating system                                                            | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DH_hs_nre_pen_MJm2       | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the district heating system                       | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DH_hs_ghg_kgm2           | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the district heating system                         | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| SOLAR_hs_nre_pen_GJ      | float  | [GJ/yr]     | Primary energy demand (non-renewable) of the solar powered heating system                                                     | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| SOLAR_hs_ghg_ton         | float  | [ton/yr]    | Emissions due to operational energy of the solar powered heating system                                                       | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| SOLAR_hs_nre_pen_MJm2    | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the solar powered heating system                  | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| SOLAR_hs_ghg_kgm2        | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the solar powered heating system                    | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| NG_hs_nre_pen_GJ         | float  | [GJ/yr]     | Primary energy demand (non-renewable) for natural gas powered heating system                                                  | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| NG_hs_ghg_ton            | float  | [ton/yr]    | Emissions due to operational energy of the natural gas powered heating system                                                 | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| NG_hs_nre_pen_MJm2       | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the natural gas powered heating system            | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| NG_hs_ghg_kgm2           | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the natural gas powered heating system              | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| COAL_hs_nre_pen_GJ       | float  | [GJ/yr]     | Primary energy demand (non-renewable) for coal powered heating system                                                         | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| COAL_hs_ghg_ton          | float  | [ton/yr]    | Emissions due to operational energy of the coal powered heating system                                                        | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| COAL_hs_nre_pen_MJm2     | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the coal powered heating system                   | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| COAL_hs_ghg_kgm2         | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the coal powererd heating system                    | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| OIL_hs_nre_pen_GJ        | float  | [GJ/yr]     | Primary energy demand (non-renewable) for oil powered heating system                                                          | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| OIL_hs_ghg_ton           | float  | [ton/yr]    | Emissions due to operational energy of the oil powered heating system                                                         | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| OIL_hs_nre_pen_MJm2      | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the oil powered heating system                    | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| OIL_hs_ghg_kgm2          | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the oil powered heating system                      | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| WOOD_hs_nre_pen_GJ       | float  | [GJ/yr]     | Primary energy demand (non-renewable) for wood powered heating system                                                         | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| WOOD_hs_ghg_ton          | float  | [ton/yr]    | Emissions due to operational energy of the wood powered heating system                                                        | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| WOOD_hs_nre_pen_MJm2     | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the wood powered heating system                   | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| WOOD_hs_ghg_kgm2         | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the wood powered heating system                     | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DH_ww_nre_pen_GJ         | float  | [GJ/yr]     | Primary energy demand (non-renewable) for district heating powered hot water system                                           | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DH_ww_ghg_ton            | float  | [ton/yr]    | Emissions due to operational energy of the district heating powered hot water system                                          | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DH_ww_nre_pen_MJm2       | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the district heating hot water system             | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| DH_ww_ghg_kgm2           | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the district heating hot water system               | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| SOLAR_ww_nre_pen_GJ      | float  | [GJ/yr]     | Primary energy demand (non-renewable) for solar powered hot water system                                                      | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| SOLAR_ww_ghg_ton         | float  | [ton/yr]    | Emissions due to operational energy of the solar powered hot water system                                                     | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| SOLAR_ww_nre_pen_MJm2    | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the solar poweed hot water system                 | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| SOLAR_ww_ghg_kgm2        | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the solar powered hot water system                  | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| NG_ww_nre_pen_GJ         | float  | [GJ/yr]     | Primary energy demand (non-renewable) for natural gas powered hot water system                                                | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| NG_ww_ghg_ton            | float  | [ton/yr]    | Emissions due to operational energy of the solar powered hot water system                                                     | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| NG_ww_nre_pen_MJm2       | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the natural gas powered hot water system          | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| NG_ww_ghg_kgm2           | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the gas powered hot water system                    | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| COAL_ww_nre_pen_GJ       | float  | [GJ/yr]     | Primary energy demand (non-renewable) for coal powered hot water system                                                       | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| COAL_ww_ghg_ton          | float  | [ton/yr]    | Emissions due to operational energy of the coal powered hot water system                                                      | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| COAL_ww_nre_pen_MJm2     | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the coal powered hot water system                 | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| COAL_ww_ghg_kgm2         | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditionend floor area of the coal powered hot water system                  | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| OIL_ww_nre_pen_GJ        | float  | [GJ/yr]     | Primary energy demand (non-renewable) for oil powered hot water system                                                        | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| OIL_ww_ghg_ton           | float  | [ton/yr]    | Emissions due to operational energy of the oil powered hot water system                                                       | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| OIL_ww_nre_pen_MJm2      | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the oil powered hot water system                  | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| OIL_ww_ghg_kgm2          | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the oil powered hot water system                    | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| WOOD_ww_nre_pen_GJ       | float  | [GJ/yr]     | Primary energy demand (non-renewable) for wood powered hot water system                                                       | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| WOOD_ww_ghg_ton          | float  | [ton/yr]    | Emissions due to operational energy of the wood powered hot water system                                                      | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| WOOD_ww_nre_pen_MJm2     | float  | [MJ/m2-yr]  | Primary energy demand per unit of conditioned floor area (non-renewable) of the wood powered hot water system                 | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| WOOD_ww_ghg_kgm2         | float  | [kg/m2 -yr] | Emissions due to operational energy per unit of conditioned floor area of the wood powered hot water system                   | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| Name                     | string | [-]         | Unique building ID. It must start with a letter.                                                                              | alphanumeric |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| GFA_m2                   | float  | [m2]        | Gross floor area                                                                                                              | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| O_ghg_ton                | float  | [ton/yr]    | Total emissions due to operational energy                                                                                     | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| O_ghg_kgm2               | float  | [kg/m2 -yr] | Total emissions due to operational energy per unit of conditioned floor area                                                  | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| O_nre_pen_GJ             | float  | [GJ/yr]     | Total operational primary energy demand (non renewable)                                                                       | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+
| O_nre_pen_MJm2           | float  | [MJ/m2-yr]  | Total Operational primary energy demand per unit of conditioned floor area (non renewable)                                    | {0.0...n}    |
+--------------------------+--------+-------------+-------------------------------------------------------------------------------------------------------------------------------+--------------+

Optimization_disconnected (District Optimized Heating)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: 

**Format/Naming**: 

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/data/optimization/disconnected/DiscOp_B01_result_heating.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| Column names /parameters        | Type    | Unit        | Description                                                                     | Valid Values |
+=================================+=========+=============+=================================================================================+==============+
| Annualized Investment Costs     | float   | [CHF]       | Annualized investment cost                                                      | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| Best configuration              | integer | [-]         | Weighted performance indicator for the best configuration                       | {-1...1}     |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| BoilerBG Share                  | float   | [-]         | Share of biogas                                                                 | {0...1}      |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| BoilerNG Share                  | float   | [-]         | Share of natural gas                                                            | {0...1}      |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| CO2 Emissions                   | float   | [kgCO2-eq]  | CO2-emissions                                                                   | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| EforGHP                         | float   | [W]         | Electricity consumption of the ground source heat pump                          | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| FC Share                        | float   | [-]         | Share of flatplate collectors                                                   | {0...1}      |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| GHP Share                       | float   | [-]         | Share of ground source heat pump                                                | {0...1}      |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| Nominal Power                   | float   | [W]         | Nomial Power of the system.                                                     | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| Operation Costs                 | float   | [CHF]       | Operations Cost                                                                 | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| Primary Energy Needs [MJoil-eq] | float   | [MJ oil-eq] | Primary energy needs in MJ oil equivalents                                      | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| QfromBG                         | float   | [W]         | District heat from biogas                                                       | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| QfromGHP                        | float   | [W]         | District heat from groundsource heatpump                                        | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| QfromNG                         | float   | [W]         | District heat from natural gas                                                  | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+
| Total Costs                     | float   | [CHF]       | Total cost of the district system (annualized investment cost + operation cost) | {0.0...n}    |
+---------------------------------+---------+-------------+---------------------------------------------------------------------------------+--------------+

Optimization_Substations
^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: 

**Format/Naming**: 

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/data/optimization/substations/BO1_results.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| Column names /parameters                                         | Type  | Unit   | Description                                                                | Valid Values |
+==================================================================+=======+========+============================================================================+==============+
| A_hex_cs                                                         | float | [m2]   | Area heat exchanger for the cooling system                                 | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| A_hex_cs_space_cooling_data_center_and_refrigeration             | float | [m2]   | Area heat exchanger for the cooling system data center and refrigeration   | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| A_hex_dhw_design_m2                                              | float | [m2]   | Area heat exchanger Domestic Hot Water system                              | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| A_hex_heating_design_m2                                          | float | [m2]   | Area heat exchanger for the cooling system data center and refrigeration   | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| Electr_array_all_flat_W                                          | float | [W]    | Electric consumption flat plate collector                                  | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| Q_dhw_W                                                          | float | [W]    | Heat demand domestic hot water system                                      | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| Q_heating_W                                                      | float | [W]    | Heat demand space cooling and refrigeration                                | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| Q_space_cooling_and_refrigeration_W                              | float | [W]    | Heat demand space cooling and refrigeration                                | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| Q_space_cooling_data_center_and_refrigeration_W                  | float | [W]    | Heat demand space cooling data center and refrigeration                    | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| T_heating_max_all_buildings_intern_K                             | float | [K]    | Maximum setpoint temperature for data center and refrigeration             | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| T_hotwater_max_all_buildings_intern_K                            | float | [K]    | Maximum setpoint temperature for domestic hot water all buildings          | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| T_return_DC_space_cooling_and_refrigeration_result_K             | float | [K]    | Temperature of return district space cooling and refrigeration             | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| T_return_DC_space_cooling_data_center_and_refrigeration_result_K | float | [K]    | Temperature of return district space cooling data center and refrigeration | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| T_return_DH_result_K                                             | float | [K]    | Temperature of return district heating system                              | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| T_supply_DC_space_cooling_and_refrigeration_result_K             | float | [K]    | Temperature of supply district space cooling and regrigeration             | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| T_supply_DC_space_cooling_data_center_and_refrigeration_result_K | float | [K]    | Temperature of supply district space cooling data center and refrigeration | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| T_supply_DH_result_K                                             | float | [K]    | Temperature of supply district heating                                     | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| T_total_supply_max_all_buildings_intern_K                        | float | [K]    | Temperature of supply for all buildings                                    | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| mdot_DH_result_kgpers                                            | float | [kg/s] | Flow rate domestic heating                                                 | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| mdot_space_cooling_and_refrigeration_result_kgpers               | float | [kg/s] | Flow rate space cooling and refrigeration                                  | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+
| mdot_space_cooling_data_center_and_refrigeration_result_kgpers   | float | [kg/s] | Flow rate space cooling data center and refrigeration                      | {0.0...n}    |
+------------------------------------------------------------------+-------+--------+----------------------------------------------------------------------------+--------------+

Potentials: solar: Building_<tech>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: These databases are somewhat generic for each solar collector technologies investigated. Irrelevant fields are not written depending on the type of technology (e.g. B01_PV.csv will not contain any thermodynamic variables).

**Format/Naming**: csv file / B01_<collector>.csv

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/potentials/solar/B01_PVT.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| Column names /parameters | Type  | Unit       | Description                                                | Valid Values            |
+==========================+=======+============+============================================================+=========================+
| Date                     | date  | [datetime] | Date and time in hourly steps.                             | {yyyy-mm-dd hh:mm:ss-Z} |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_south_Q_kWh | float | [kWh]      | Heat production from <tech> panels on south facades        | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_south_E_kWh | float | [kWh]      | Electricity production from <tech> panels on south facades | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_south_m2    | float | [kWh]      | South facing wall <tech> surface area.                     | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_north_Q_kWh | float | [kWh]      | Heat production from <tech> panels on north facades        | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_north_E_kWh | float | [kWh]      | Electricity production from <tech> panels on north facades | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_north_m2    | float | [kWh]      | North facing wall <tech> surface area.                     | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_roofs_top_Q_kWh   | float | [kWh]      | Heat production from <tech> panels on roof tops            | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_roofs_top_E_kWh   | float | [kWh]      | Electricity production from <tech> panels on roof tops     | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_roofs_top_m2      | float | [kWh]      | Top facing roof <tech> surface area.                       | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_east_Q_kWh  | float | [kWh]      | Heat production from <tech> panels on east facades         | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_east_E_kWh  | float | [kWh]      | Electricity production from <tech> panels on east facades  | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_east_m2     | float | [kWh]      | East facing wall <tech> surface area.                      | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_west_Q_kWh  | float | [kWh]      | Heat production from <tech> panels on west facades         | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_west_E_kWh  | float | [kWh]      | Electricity production from <tech> panels on west facades  | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| <tech>_walls_west_m2     | float | [kWh]      | West facing wall <tech> surface area.                      | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| Area_<tech>_m2           | float | [m2]       | Total area of investigated <tech>.                         | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| radiation_kWh            | float | [kWh]      | Total radiatiative potential.                              | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| E_<tech>_gen_kWh         | float | [kWh]      | Total electricity generated by the <tech>.                 | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| Q_<tech>_gen_kWh         | float | [kWh]      | Total heat generated by the <tech>.                        | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| mcp_<tech>_kWperC        | float | [kW/Cap]   | Permissable heating power delivered via the <tech>.        | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| Eaux_<tech>_kWh          | float | [kWh]      | Auxiliary electricity consumed by the <tech>.              | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| Q_<tech>_l_kWh           | float | [kWh]      | <tech> heat loss.                                          | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| T_<tech>_sup_C           | float | [C]        | <tech> heating supply temperature.                         | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+
| T_<tech>_re_C            | float | [C]        | <tech> heating supply temperature.                         | {0.0...n}               |
+--------------------------+-------+------------+------------------------------------------------------------+-------------------------+

Potentials: solar: Building_<tech>_sensors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Description**: These databases are generic for all solar collector technologies investigated. They describe the position of all the sensoral nodes and assumed build characteristics of installed solar arrays.

**Format/Naming**: csv file / B01_<collector>_sensors.csv

**Location (example)**: `` ..cea/examples/reference-case-open/baseline/outputs/potentials/solar/B01_PVT_sensors.csv``

**Primary Interdependencies**: 

**Secondary Interdependencies**: 

+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| Column names /parameters | Type   | Unit    | Description                                                                          | Valid Values            |
+==========================+========+=========+======================================================================================+=========================+
| SURFACE                  | string | [-]     | Unique surface ID for each building exterior surface.                                | {srf0...srfn}           |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| AREA_m2                  | float  | [m2]    | Area of the unique surface for each building.                                        | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| BUILDING                 | string | [-]     | Unique building ID. It must start with a letter.                                     | alphanumeric            |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| TYPE                     | string | [-]     | Surface typology.                                                                    | {walls, windows, roofs} |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| Xcoor                    | float  | [-]     | Describes the position of the x vector, used to define the location of the sensor.   | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| Xdir                     | float  | [-]     | Directional scalar of the x vector.                                                  | {-1...1}                |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| Ycoor                    | float  | [-]     | Describes the position of the y vector, , used to define the location of the sensor. | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| Ydir                     | float  | [-]     | Directional scalar of the y vector.                                                  | {-1...1}                |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| Zcoor                    | float  | [-]     | Describes the position of the z vector, , used to define the location of the sensor. | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| Zdir                     | float  | [-]     | Directional scalar of the z vector.                                                  | {-1...1}                |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| orientation              | string | [-]     | Orientation of the surface (north, east, south, west or top)                         | {north...}              |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| total_rad_Whm2           | float  | [Wh/m2] | Total radiatiative potential of a given surfaces area.                               | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| tilt_deg                 | float  | [deg]   | Solar panel tilt angle, measured from the surface to the back of the array.          | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| B_deg                    | float  | [deg]   |                                                                                      | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| array_spacing_m          | float  | [m]     | Spacing between solar arrays.                                                        | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| surface_azimuth_deg      | float  | [deg]   | Solar azimuth with reference to the surface.                                         | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| area_installed_module_m2 | float  | [m2]    | Effective area of solar arrays.                                                      | {0.0...n}               |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| CATteta_z                | int    | [-]     |                                                                                      | {0...n}                 |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| CATB                     | int    | [-]     |                                                                                      | {0...n}                 |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| CATGB                    | int    | [-]     |                                                                                      | {0...n}                 |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| type_orientation         | string | [-]     | Concatenated surface type and orientation.                                           | {type_orientation}      |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+
| surface                  | string | [-]     | Unique surface ID for each building exterior surface.                                | {srf0...srfn}           |
+--------------------------+--------+---------+--------------------------------------------------------------------------------------+-------------------------+