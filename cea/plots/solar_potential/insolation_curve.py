from plotly.offline import plot
import plotly.graph_objs as go
from cea.plots.variable_naming import LOGO

def insolation_curve(data_frame, analysis_fields, title, output_path):

    traces = []
    x = data_frame.index.values
    for field in analysis_fields:
        y = data_frame[field].values
        if field == "T_out_dry_C":
            trace = go.Scatter(x= x, y= y, name = field.split('t', 1)[0], yaxis='y2', opacity = 0.2)
        else:
            trace = go.Scatter(x= x, y= y, name = field)
        traces.append(trace)

    # CREATE FIRST PAGE WITH TIMESERIES
    layout = dict(images=LOGO, title=title, yaxis=dict(title='Isolation [W/m2]'), yaxis2=dict(title='Temperature [C]', overlaying='y',
                   side='right'),xaxis=dict(rangeselector=dict(buttons=list([
                    dict(count=1,label='1d',step='day',stepmode='backward'),
                    dict(count=1,label='1w',step='week',stepmode='backward'),
                    dict(count=1,label='1m',step='month',stepmode='backward'),
                    dict(count=6,label='6m',step='month', stepmode='backward'),
                    dict(count=1,label='1y',step='year',stepmode='backward'),
                    dict(step='all')])),rangeslider=dict(),type='date'))

    fig = dict(data=traces, layout=layout)
    plot(fig,  auto_open=False, filename=output_path)