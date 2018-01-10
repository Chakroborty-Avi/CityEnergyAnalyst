from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np

def heating_reset_schedule(data_frame, analysis_fields, title, output_path):

    # CREATE FIRST PAGE WITH TIMESERIES
    traces = []
    x = data_frame["T_out_dry_C"].values
    data_frame = data_frame.replace(0, np.nan)
    for field in analysis_fields:
        y = data_frame[field].values
        trace = go.Scatter(x= x, y= y, name = field, mode = 'markers')
        traces.append(trace)

    layout = go.Layout(title=title,
                       xaxis=dict(title='Outdoor Temperature [C]'),
                       yaxis=dict(title='HVAC System Temperature [C]'))
    fig = go.Figure(data=traces, layout=layout)
    plot(fig, auto_open=False, filename=output_path)