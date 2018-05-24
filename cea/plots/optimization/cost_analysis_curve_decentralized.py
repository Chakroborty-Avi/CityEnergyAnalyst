from __future__ import division

import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import numpy as np
from cea.plots.variable_naming import LOGO, COLOR


def cost_analysis_curve_decentralized(data_frame, locator, final_generation, config):
    analysis_fields_cost_decentralized_heating = ["BoilerBG Share", "BoilerNG Share", "FC Share", "GHP Share",
                                                       "Operation Costs [CHF]", "Annualized Investment Costs [CHF]"]
    title = 'Decentralized Cost Analysis for generation ' + str(final_generation)
    total_demand = pd.read_csv(locator.get_total_demand())
    building_names = total_demand.Name.values

    if config.plots.network_type == 'DH':
        individual = 0

        column_names = ['Disconnected_Capex_Boiler_BG', 'Disconnected_Capex_Boiler_NG', 'Disconnected_Capex_GHP',
                        'Disconnected_Capex_FC', 'Disconnected_Opex_Boiler_BG', 'Disconnected_Opex_Boiler_NG',
                        'Disconnected_Opex_GHP', 'Disconnected_Opex_FC']

        data_frame_building = pd.DataFrame(np.zeros([len(building_names), len(column_names)]), columns=column_names)
        output_path = locator.get_timeseries_plots_file('gen' + str(final_generation) + '_decentralized_cost_analysis_split')

        for building_number, building_name in enumerate(building_names):

            analysis_fields_building = []
            for j in range(len(analysis_fields_cost_decentralized_heating)):
                analysis_fields_building.append(str(building_name) + " " + analysis_fields_cost_decentralized_heating[j])


            print (data_frame[analysis_fields_building[0]][individual])

            data_frame_building['Disconnected_Capex_Boiler_BG'][building_number] = data_frame[analysis_fields_building[0]][individual] * data_frame[analysis_fields_building[5]][individual]
            data_frame_building['Disconnected_Capex_Boiler_NG'][building_number] = data_frame[analysis_fields_building[1]][individual] * data_frame[analysis_fields_building[5]][individual]
            data_frame_building['Disconnected_Capex_GHP'][building_number] = data_frame[analysis_fields_building[2]][individual] * data_frame[analysis_fields_building[5]][individual]
            data_frame_building['Disconnected_Capex_FC'][building_number] = data_frame[analysis_fields_building[3]][individual] * data_frame[analysis_fields_building[5]][individual]
            data_frame_building['Disconnected_Opex_Boiler_BG'][building_number] = data_frame[analysis_fields_building[0]][individual] * data_frame[analysis_fields_building[4]][individual]
            data_frame_building['Disconnected_Opex_Boiler_NG'][building_number] = data_frame[analysis_fields_building[1]][individual] * data_frame[analysis_fields_building[4]][individual]
            data_frame_building['Disconnected_Opex_GHP'][building_number] = data_frame[analysis_fields_building[2]][individual] * data_frame[analysis_fields_building[4]][individual]
            data_frame_building['Disconnected_Opex_FC'][building_number] = data_frame[analysis_fields_building[3]][individual] * data_frame[analysis_fields_building[4]][individual]

        # CALCULATE GRAPH
        traces_graph = calc_graph(column_names, data_frame_building)

        # CREATE FIRST PAGE WITH TIMESERIES
        layout = go.Layout(images=LOGO, title=title, barmode='stack',
                           yaxis=dict(title='Cost [$ per year]', domain=[0.0, 1.0]))

        fig = go.Figure(data=traces_graph, layout=layout)
        plot(fig, auto_open=False, filename=output_path)

    if config.plots.network_type == 'DC':
        output_path = locator.get_timeseries_plots_file('gen' + str(final_generation) + '_DCN_decentralized_cost_analysis_split')
        # CALCULATE GRAPH
        traces_graph = calc_graph(analysis_fields, data_frame)

        # CREATE FIRST PAGE WITH TIMESERIES
        layout = go.Layout(images=LOGO, title=title, barmode='stack',
                           yaxis=dict(title='Cost [$ per year]', domain=[0.0, 1.0]))

        fig = go.Figure(data=traces_graph, layout=layout)
        plot(fig, auto_open=False, filename=output_path)

    return {'data': traces_graph, 'layout': layout}


def calc_graph(analysis_fields, data_frame):
    # main data about technologies
    data = (data_frame)
    graph = []
    for field in analysis_fields:
        y = data[field].values
        trace = go.Bar(x=data.index, y=y, name=field, marker=dict(color=COLOR[field]))
        graph.append(trace)

    return graph
