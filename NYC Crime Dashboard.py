import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

df = pd.read_csv('C:\\Users\\birju\\Documents\\CS 301\\NYPD_Complaint_Data_Clean.csv')
df_count = pd.read_csv('C:\\Users\\birju\\Documents\\CS 301\\NYPD_Complaint_Data_Count.csv')

app.layout = html.Div([
    html.H1(children = 'NYC Crime Dashboard', style = {'textAlign': 'center'}),

    html.Hr(),

    html.Div([
        dcc.Graph(
            id = 'by-borough',
            figure = {
                'data': [
                    dict(
                        x = df_count['Hour'],
                        y = df_count[i],
                        name = i,
                        mode = 'lines+markers',
                        marker = {'size':8}
                    ) for i in ['Manhattan', 'Queens', 'Bronx', 'Brooklyn', 'Staten Island']
                ],
                'layout': dict(
                    title = 'Number of Complaints per Hour by Borough',
                    xaxis = {'title': 'Hour of the Day'},
                    yaxis = {'title': 'Number of Complaints'},
                    margin = {'l': 60, 'b': 60, 't': 25, 'r': 0},
                    legend = {'x': 0.1, 'y': 1},
                    hovermode = 'closest'
                )
            }
        )
    ], style = {'width': '50%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
            id = 'by-complaint-type',
            figure = {
                'data': [
                    dict(
                        x = df_count['Hour'],
                        y = df_count[i],
                        name = i,
                        mode = 'lines+markers',
                        marker = {'size':8}
                    ) for i in ['Total', 'Felony', 'Misdemeanor', 'Violation']
                ],
                'layout': dict(
                    title = 'Number of Complaints per Hour by Complaint Type',
                    xaxis = {'title': 'Hour of the Day'},
                    yaxis = {'title': 'Number of Complaints'},
                    margin = {'l': 60, 'b': 60, 't': 25, 'r': 0},
                    legend = {'x': 0.1, 'y': 1},
                    hovermode = 'closest'
                )
            }
        )
    ], style = {'width': '50%', 'display': 'inline-block'}),

    html.Hr(),
    
    html.Div([
        dcc.Graph(id = 'specific-conditions')
    ], style = {'width': '75%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Borough'),
        dcc.RadioItems(
            id = 'borough-pick',
            options = [{'label': i, 'value': i.upper()} for i in ['All Boroughs', 'Manhattan', 'Queens', 'Bronx', 'Brooklyn', 'Staten Island']],
            value = 'MANHATTAN'
        ),

        html.Hr(),

        html.Label('Complaint Type'),
        dcc.RadioItems(
            id = 'complaint-type-pick',
            options=[{'label': i, 'value': i.upper()} for i in ['All Complaint Types', 'Felony', 'Misdemeanor', 'Violation']],
            value = 'FELONY'
        )
    ], style={'width': '25%', 'float': 'right', 'display': 'inline-block'})
])

@app.callback(
    dash.dependencies.Output('specific-conditions', 'figure'),
    [dash.dependencies.Input('borough-pick', 'value'),
     dash.dependencies.Input('complaint-type-pick', 'value')])
def update_specific_conditions_graph(borough, complaint_type):
    if borough == 'ALL BOROUGHS' and complaint_type == 'ALL COMPLAINT TYPES':
        count = df_count['Total']
    elif borough == 'ALL BOROUGHS':
        count = df_count[complaint_type.title()]
    elif complaint_type == 'ALL COMPLAINT TYPES':
        count = df_count[borough.title()]
    else:
        df_specific = df.loc[(df['BORO_NM'] == borough) & (df['LAW_CAT_CD'] == complaint_type)]
        count = np.zeros(25)
        for ind in df_specific.index:
            hour = int(str(df_specific['CMPLNT_FR_TM'][ind])[0:2])
            count[hour] += 1
        count[24] = count[0]
    return {'data': [
                dict(
                    x = df_count['Hour'],
                    y = count,
                    mode = 'lines+markers',
                    marker = {'size':8}
                )
            ],
            'layout': dict(
                title = 'Number of {} per Hour in {}'.format(complaint_type.title(), borough.title()),
                xaxis = {'title': 'Hour of the Day'},
                yaxis = {'title': 'Number of {}'.format(complaint_type.title())},
                margin = {'l': 60, 'b': 60, 't': 25, 'r': 0},
                hovermode = 'closest'
            )}

if __name__ == '__main__':
    app.run_server(debug=True)
