What are the CEA Scripts?
=========================
CEA relies on a number of scripts which may share dependencies.
This section aims to clarify the databases created or used by each script, along with the methods used
to access this data. Scripts can be run via the command line interface (cli) by calling: ``cea script-name``.

Core
----
Currently, the CEA operates using a core set of scripts whose outputs are necessary for the function of
other scripts. They should be run in the following order:

    #.   ``data-helper`` : creates secondary input databases from the default within cea/databases
         (only needs to be run once for each scenario).
    #.   ``radiation-daysim`` : creates the solar insolation data for each building using daysim.
    #.   ``demand`` : creates a demand approximation for each building.

.. graphviz::

    digraph trace_inputlocator {
        rankdir="LR";
        node [shape=box, style=filled, fillcolor=peachpuff]
        graph [overlap = false];
        "data-helper"[style=filled, fillcolor=darkorange];
        "demand"[style=filled, fillcolor=darkorange];
        "radiation-daysim"[style=filled, fillcolor=darkorange];
        "databases/CH/archetypes" -> "data-helper"
        "inputs/building-properties" -> "data-helper"
        "databases/CH/archetypes" -> "demand"
        "inputs/building-properties" -> "demand"
        "databases/CH/systems" -> "demand"
        "databases/CH/lifecycle" -> "demand"
        "outputs/data/solar-radiation" -> "demand"
        "databases/CH/systems" -> "demand"
        "../../users/jack/documents/github/cityenergyanalyst/cea/databases/weather" -> "demand"
        "inputs/building-geometry" -> "demand"
        "inputs/building-properties" -> "radiation-daysim"
        "inputs/building-geometry" -> "radiation-daysim"
        "databases/CH/systems" -> "radiation-daysim"
        "inputs/topography" -> "radiation-daysim"
        "../../users/jack/documents/github/cityenergyanalyst/cea/databases/weather" -> "radiation-daysim"
        "inputs/building-geometry" -> "radiation-daysim"
        "data-helper" -> "inputs/building-properties"
        "demand" -> "outputs/data/demand"
        "radiation-daysim" -> "outputs/data/solar-radiation"
        }

{% for script, underline, digraph in dependencies%}
{{script}}
{{underline}}
.. graphviz::

    {{digraph}}
{% endfor %}