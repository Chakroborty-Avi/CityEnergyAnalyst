:orphan:

Installation guide for Windows
==============================

Follow these instructions to install the CityEnergyAnalyst (CEA) on a Windows system (tested with Windows 10).

1. `Download the latest version of CEA (2.13.5a1) in here`_.
    Note: For previous releases please check `here <https://github.com/architecture-building-systems/CityEnergyAnalyst/releases/>`__.
    Note: To install from the source check :doc:`here <installation-on-windows-manual>`

.. _`Download the latest version of CEA (2.13.5a1) in here` : https://github.com/architecture-building-systems/CityEnergyAnalyst/releases/download/v2.13/Setup_CityEnergyAnalyst_2.13.5a1.exe

2. Open the installer and follow the instructions
    Note: For installing the development version of CEA, tick the box "development version" during the installation.


Interfaces
~~~~~~~~~~

There are different ways in which you can interact with the code of CEA.

#. The command line interface: This is the command line to all the commands of CEA from your computer terminal
#. The dashboard: This a web-based interface to CEA, open source and developed by the CEA team.
#. The pycharm interface: this interface provides access to all the source code of CEA.
#. The Rhino/Grasshopper interface: This a 3D modeling interface to CEA.
#. The ArcGIS interface: This a GIS interface to CEA (Not supported anymore).

The command line interface and dashboard interface are included during the installation of CEA.

Other interfaces require a few additional steps to get them up and running.

Pycharm
-------

In order to access and work on the source code of CEA from pycharm do:

#. Make sure to have installed the development version of CEA (see step 2 of the installation guide.
#. Download and install `Github Desktop (64-bit) <https://desktop.github.com/>`__.
#. Download and install `Pycharm Community edition (64-bit) <https://www.jetbrains.com/pycharm/download/#section=windows>`__ OR your own favorite editor.
#. Open PyCharm from the start menu and open project CityEnergyAnalyst (stored where you installed City Energy Analyst).
#. Open ``File>Settings>Project:CityEnergyAnalyst>Project Interpreter>Project Interpreter``.
#. Click on the settings button (it looks like a wheel) next to the current interpreter path, and click Add.
#. Click ``Conda Environment`` from the left hand list and select existing environment.
#. Point to the location of your conda environment. It should look something like
   ``C:\Users\your_name\Miniconda2\envs\cea\python.exe`` or
   ``C:\Users\your_name\AppData\Local\conda\conda\envs\cea\python.exe``.
   Where 'your_name' represents your user name in windows.
#. Click apply changes.

Grasshopper
------------

.. attention:: This is a highly experimental interface to Rhino/Grasshopper, and we do not include any tutorials nor support to the public.
               for the time being, just a few modules of CEA have been integrated. If you are interested in support or would like to furthermore activate this interface
               contact shi@arch.ethz.ch

In order to install the interface for Rhino/Grasshopper do:

#. Download and install `Rhino 5.0 <https://www.rhino3d.com/download>`_ (requires a licence).
#. Download and install the `Grasshopper for rhino 5.0 <https://www.grasshopper3d.com/page/download-1>`_.
#. Follow the steps of the installation guide of the code base described above.
#. In the CEA command line Type ``cea install-grasshopper`` and press ENTER.

ArcGIS
-------

.. attention:: We ended support of Arcigs by the 1st of May of 2019. This means that there are not anymore
               tutorials nor advice on how to use this interface. You could still use this interface at your own risk.
               We invite all CEA users to get acquainted with the CEA Dashboard. The CEA dashboard is our new 100% open source user interface.
               We will aim to create a first tutorial on how to use this interface by mid-april of 2019.

In order to install the interface for ArcGIS do:

#. Download and install `ArcGIS Desktop 10.5 or 10.6 <https://desktop.arcgis.com/en/arcmap/latest/get-started/installation-guide/introduction.htm>`_ (requires a licence).
    * An `Esri account <https://www.arcgis.com/home/signin.html>`_ must be created to buy and download ArcGIS Desktop, located in Products: All Products.
    * ETH affiliates are advised to access ArcGIS via the ETH IT Shop.
#. Download and install the `ArcGIS Desktop Background Geoprocessing (64 Bit) <https://desktop.arcgis.com/en/arcmap/latest/analyze/executing-tools/64bit-background.htm>`_.
#. Follow the steps of the installation guide of the code base described above.
#. In the CEA command line Type ``cea install-arcgis`` and press ENTER.

