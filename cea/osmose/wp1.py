from __future__ import division
import numpy as np
import time
import pandas as pd
import os
import subprocess
import csv
import cea.osmose.settings as settings

import cea.osmose.extract_demand_outputs as extract_demand_outputs
import cea.osmose.plot_osmose_result as plot_results
import cea.osmose.compare_el_usages as compare_el

# import from settings # TODO: add to config
TECHS = settings.TECHS
specified_buildings = settings.specified_buildings
timesteps = settings.timesteps
start_t = settings.start_t
osmose_project_path = settings.osmose_project_path
ampl_lic_path = settings.ampl_lic_path
result_destination = settings.result_destination
new_calculation = settings.new_calculation


def main(case):
    # make folder to save results
    path_to_case_folder = os.path.join(result_destination, case)
    make_directory(path_to_case_folder, new_calculation)

    # extract demand outputs
    building_names = extract_demand_outputs.extract_cea_outputs_to_osmose_main(case, start_t, timesteps,
                                                                               specified_buildings)

    ## start ampl license
    start_ampl_license(ampl_lic_path, "start")

    ## run osmose
    write_string_to_txt(path_to_case_folder, osmose_project_path, "path_to_case_folder.txt")  # osmose input
    write_value_to_csv(timesteps, osmose_project_path, "timesteps.csv")  # osmose input
    for building in building_names:
        write_value_to_csv(building, osmose_project_path, "building_name.csv")  # osmose input
        for tech in TECHS:
            t = time.localtime()
            print time.strftime("%H:%M", t)
            t0 = time.clock()
            exec_osmose(tech, osmose_project_path)
            time_elapsed = time.clock() - t0
            print round(time_elapsed,0), ' s for running: ', tech, '\n'

        #plot results
        building_timestep_tag = building + "_" + str(timesteps)
        building_result_path = os.path.join(path_to_case_folder, building_timestep_tag)
        #building_result_path = os.path.join(building_result_path, "reduced")
        plot_results.main(building, TECHS, building_result_path)
        #compare_el.main(building, building_result_path)
    #start_ampl_license(ampl_lic_path, "stop")
    return np.nan


def make_directory(dirName, new_calculation=True):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print"Directory ", dirName, " Created "
    elif new_calculation == True:
        raise ValueError("Directory ", dirName,
                         " already exists, please clean up the files and restart the calculation.")
    else:
        print"Directory ", dirName, " already exists"
    return np.nan


def write_value_to_csv(timesteps, osmose_project_path, filename):
    csvData = [[timesteps, "N/A"], []]
    file_path = os.path.join(osmose_project_path, filename)
    with open(file_path, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    csvFile.close()
    return np.nan


def write_string_to_txt(content, osmose_project_path, filename):
    file_path = os.path.join(osmose_project_path, filename)
    with open(file_path, "w") as text_file:
        text_file.write(content)
    return np.nan


def start_ampl_license(ampl_lic_path, action):
    command = os.path.join(ampl_lic_path, "ampl_lic.exe " + action)
    p_ampllic = subprocess.Popen(command, cwd=ampl_lic_path)
    ampllic_out, ampllic_err = p_ampllic.communicate()
    if ampllic_out is not None:
        print ampllic_out.decode('utf-8')
    if ampllic_err is not None:
        ampllic_err.decode('utf-8')
    return np.nan


def exec_osmose(tech, osmose_project_path):
    frontend_file = tech + "_frontend.lua"
    frontend_path = osmose_project_path + "\\" + frontend_file
    project_path = os.path.dirname(osmose_project_path)

    p = subprocess.Popen(["lua", (frontend_path)], cwd=project_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    print "running: ", frontend_file
    output, err = p.communicate()

    if err.decode('utf-8') is not '':
        # print(err.decode('utf-8'))
        if err.decode('utf-8').startswith('WARNING:'):
            print 'warning' #, err.decode('utf-8')
        elif err.decode('utf-8').startswith('pandoc: Could not find image'):
            print 'warning' #, err.decode('utf-8')
        else:
            print "ERROR"

    # print(output.decode('utf-8'))

    # print OutMsg
    result_path = os.path.dirname(osmose_project_path) + "\\results\\" + tech
    run_folder = os.listdir(result_path)[len(os.listdir(result_path))-1]
    OutMsg_path = os.path.join(result_path,run_folder) + "\\scenario_1\\tmp\\OutMsg.txt"
    f = open(OutMsg_path, "r")
    print tech, run_folder, "OutMsg: ", f.readline(), f.readline(), f.readline()

    return 'ok', output.decode('utf-8')


if __name__ == '__main__':
    #cases = ['WTP_CBD_m_WP1_RET']
    cases = ['WTP_CBD_m_WP1_HOT','WTP_CBD_m_WP1_OFF','WTP_CBD_m_WP1_RET']
    for case in cases:
        main(case)
    # stop ampl license
    start_ampl_license(ampl_lic_path, "stop")
