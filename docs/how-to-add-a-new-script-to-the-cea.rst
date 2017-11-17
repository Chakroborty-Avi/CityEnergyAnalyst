How to add a new script to the CEA
==================================

So you want to extend the CEA with a new script? This guide will get you up and running!

The main steps you need to take are:

#. copy the template script and rename it
#. update the module-level documentation and credits
#. develop your script
#. update the ``cli.config`` file to link your script name to the module
#. update the ``cli.config`` file to specify the parameters your script requires
#. add a section to the ``default.config`` file for any parameters your script requires
#. add an ArcGIS interface to ``cea.interfaces.arcgis.CityEnergyAnalyst.py``


Step 1: Copy the template script and rename it
----------------------------------------------

Copy the file ``cea/examples/template.py`` to a location inside the ``cea`` folder hierarchy - check other scripts
for a good place to locate it. If you need to create a subfolder, make sure you add an (empty) file called
``__init__.py`` to that folder - this makes the folder a python package and is essential for referencing the script
later on.

Rename the copied file to a name that describes your script as good as possible. You should now be able to run the
script in PyCharm (or by hand with ``python -m cea.your_package_name.your_script_name``) and get the following
output::

    Running template with scenario = C:\reference-case-open\baseline
    Running template with archetypes = ['comfort', 'architecture', 'HVAC', 'internal-loads']

Inside the ``main`` function of your script, there is a section of ``print`` statements. It is a good idea to update
this list to print out the parameters actually used by your script.

The ``main`` function in the template calls a function ``template``, passing in an ``InputLocator`` object and unpacking
the ``config`` parameter. We call this the "core" function of your script. You should definitely change the name of
the core function - ideally to the name of the script / module it resides in. The ``InputLocator`` object (by convention
called ``locator``) is used by nearly every single CEA script.

The other parameters are much more dependant on the requirements of your script. If you find yourself adding more
than a few parameters, consider just passing in the ``config`` variable instead, as long parameter lists in functions
can make your code hard to read.

Step 2: update the module-level documentation and credits
---------------------------------------------------------

While you're at it:

- update the module-level documentation to reflect the _what_ and the _why_ of your script, including references to
  literature
- update the documentation of the core function of your script (the one called ``template`` in the template) to reflect
  the __how__ of your script
- update the credits section (near the top of the script) - be sure to change at least the following parts:
  - ``__author__`` (add your name!)
  - ``__credits__`` (add a list of names of colaborators)
  - ``__copyright__`` (update the year of the copyright for this script)


Step 3: Develop your script
---------------------------

Each script is unique. But to fit nicely into the CEA ecosystem, pay attention to the following points:

- spend some time to come up with good names for variables and functions

  - as a general rule, don't use abbreviations other than as loop indices (they're just hard to communicate later on)

    - beginners often think using short names and abreviations is "cool" - this is probably the fault of decades and
      decades of bad examples in code. There used to be a time when it mattered, but nobody uses those languages
      anymore. It's a lot easier to read real words.

  - try to use the same names for the same thing
  - make sure the names refer to the subject domain of your script (this makes the leap between literature and your
    code easier to make for anyone trying to figure out what your script does later on)
  - use plural for names referring to lists, tuples, sets and dictionaries
  - check for spelling errors (this also counts for comments) - HINT: PyCharm has a built-in automatic spellchecker much
    like the one in MS Word. If PyCharm marks any of your code in yellow or green, try to figure out why and fix it!

- don't hardcode paths! The CEA uses the ``cea.inputlocator.InputLocator`` class to define where files are. Follow this
  convention.

  - If you do need to manually create paths, use ``os.path.join(folder, ..., filename)`` instead of concatenating strings.

- if you think you need to use ``os.chdir``, you're doing it wrong!


Step 4: update the ``cli.config`` file to link your script name to the module
-----------------------------------------------------------------------------

The ``cli.config`` file (located in ``cea/interfaces/cli/``) tells the ``cea`` command line program

- the name of each script in the CEA
- the module path of the script to run
- the list of parameters that the script accepts

By adding your script to the ``cli.config`` file, your script becomes executable from the command line like this::

    $ cea your-script-name --scenario C:\reference-case-open\baseline --your-parameter 123



- config.scripts
  - list of script names (keys) and the module to call (values)
- script file follows a naming convention

  - module variable ``CEA_CONFIG_SECTIONS = ['general', 'demand']`` returns a list of configuration sections that are
    used by this script
  - module level function ``main`` is called to run script

- always call the scenario "scenario_path"??
- how to add a new option to the config file?
- purposes and principals
  - scripts should be runnable from the commandline with ``cea template --parameter value``
  - scripts should be runnable from PyCharm
  - all arguments to the scripts have a default value in ``default.config``
- place path names in double quotes when used as command lines
- parameter names should be unique throughout the template (create a unit test for this)
- print out parameters


Step N:
-------

Add such a script by appending to the ``cea/cli.config`` file like this:

::

    [scripts]
    template = cea.example.template
    template.sections = general:scenario general:region data-helper

In the above example, ``template`` is the name of the script (as in ``cea template``) and ``template.sections``
refers to the list of sections in the default.config file that this script uses as parameters. If you only need some
parameters from a section, you can use the form ``section:key`` to specify a specific parameter in a section.