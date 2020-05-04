import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
tod = pd.read_csv('C:\\Users\\birju\\Documents\\GitHub\\cs301\\NYPD_Complaint_Data_Clean.csv')
tod_count = pd.read_csv('C:\\Users\\birju\\Documents\\GitHub\\cs301\\NYPD_Complaint_Data_Count.csv')
income = pd.read_csv('C:\\Users\\birju\\Documents\\GitHub\\cs301\\NYC_Income_Arrests.csv')
pop = pd.read_csv('C:\\Users\\birju\\Documents\\GitHub\\cs301\\NYC_Population_vs_Arrests.csv')
edu = pd.read_csv('C:\\Users\\birju\\Documents\\GitHub\\cs301\\NYC_Crime_vs_Education.csv')
edu = edu.groupby('Borough').median()
edu.reset_index(inplace=True)
locations = np.arange(edu.shape[0])
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.Hr(),
    html.H1(children = 'NYC Crime Dashboard', style = {'textAlign': 'center'}),
    html.Hr(),
    html.Plaintext(children = 'This dashboard is purposed with displaying the relationship between crime in New York City\nand various factors such as the time of day and the population.\nClick on a page below to compare crime in NYC to a specific factor. Use the options on these pages\nto manipulate the graphs and draw your own conclusions about crime in NYC', style = {'fontSize': '18px', 'textAlign': 'center'}),
    
    html.Hr(),
    html.Div(style = {'width': '20%', 'display': 'inline-block'}),
    html.Div(dcc.Link('NYC Crime vs Time of Day', href = '/page-1'), style = {'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Income', href = '/page-2'), style = {'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Population', href = '/page-3'), style = {'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Education', href = '/page-4'), style = {'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Hr(),
    html.Div(children = 'Created by Birju Dhaduk for a CS 301 honors enhancement project', style = {'fontSize': '12px', 'textAlign': 'right'}),
    html.Hr()
])

page_1_layout = html.Div([
    html.Hr(),
    html.H1(children = 'NYC Crime vs Time of Day', style = {'textAlign': 'center'}),
    html.Hr(),
    html.Div([
        dcc.Graph(
            figure = {
                'data': [
                    dict(
                        x = tod_count['Hour'],
                        y = tod_count[i],
                        name = i,
                        mode = 'lines+markers',
                        marker = {'size':8}
                    ) for i in ['Manhattan', 'Queens', 'Bronx', 'Brooklyn', 'Staten Island']
                ],
                'layout': dict(
                    title = 'Number of Complaints per Hour by Borough',
                    xaxis = {'title': 'Hour of the Day', 'tickangle': -45},
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
            figure = {
                'data': [
                    dict(
                        x = tod_count['Hour'],
                        y = tod_count[i],
                        name = i,
                        mode = 'lines+markers',
                        marker = {'size':8}
                    ) for i in ['Felony', 'Misdemeanor', 'Violation', 'Total']
                ],
                'layout': dict(
                    title = 'Number of Complaints per Hour by Crime Type',
                    xaxis = {'title': 'Hour of the Day', 'tickangle': -45},
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
        dcc.Graph(id = 'tod-specific-conditions')
    ], style = {'width': '75%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Crime Type'),
        dcc.RadioItems(
            id = 'tod-crime-type-pick',
            options=[{'label': i, 'value': i.upper()} for i in ['Felony', 'Misdemeanor', 'Violation']],
            value = 'FELONY'
        ),
        html.Hr(),
        html.Plaintext(children = 'Please give the dashboard a few seconds to \nload after making a selection.', style = {'fontSize': '14px'}),
        html.Hr(),
        dcc.Link(children = 'Link to NYPD Complaint Dataframe', href = 'https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243', target='_blank')
    ], style={'width': '25%', 'float': 'right', 'display': 'inline-block'}),

    html.Hr(),
    html.Div(style={'width': '20%', 'display': 'inline-block'}),
    html.Div(dcc.Link('NYC Crime vs Income', href='/page-2'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Population', href='/page-3'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Education', href='/page-4'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('Go Back to Home', href='/'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Hr(),
    html.Div(children = 'Created by Birju Dhaduk for a CS 301 honors enhancement project', style = {'fontSize': '12px', 'textAlign': 'right'}),
    html.Hr()
])

@app.callback(
    dash.dependencies.Output('tod-specific-conditions', 'figure'),
    [dash.dependencies.Input('tod-crime-type-pick', 'value')])
def update_tod_graph(complaint_type):
    subset = tod.loc[(tod['LAW_CAT_CD'] == complaint_type)]
    total = np.zeros(25)
    manhattan = np.zeros(25)
    queens = np.zeros(25)
    bronx = np.zeros(25)
    brooklyn = np.zeros(25)
    staten_island = np.zeros(25)
    for ind in subset.index:
        name = tod['BORO_NM'][ind]
        hour = int(str(tod['CMPLNT_FR_TM'][ind])[0:2])
        total[hour] += 1
        if name == 'MANHATTAN':
            manhattan[hour] += 1
        if name == 'QUEENS':
            queens[hour] += 1
        if name == 'BRONX':
            bronx[hour] += 1
        if name == 'BROOKLYN':
            brooklyn[hour] += 1
        if name == 'STATEN ISLAND':
            staten_island[hour] += 1
    total[24] = total[0]
    manhattan[24] = manhattan[0]
    queens[24] = queens[0]
    bronx[24] = bronx[0]
    brooklyn[24] = brooklyn[0]
    staten_island[24] = staten_island[0]
    hour = ['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM',
        '7AM', '8AM', '9AM', '10AM', '11AM', '12PM',
        '1PM', '2PM', '3PM', '4PM', '5PM', '6PM',
        '7PM', '8PM', '9PM', '10PM', '11PM', '12.AM']
    def get_name(i):
        if total[0] == i[0]:
            return 'Total'
        if manhattan[0] == i[0]:
            return 'Manhattan'
        if queens[0] == i[0]:
            return 'Queens'
        if bronx[0] == i[0]:
            return 'Bronx'
        if brooklyn[0] == i[0]:
            return 'Brooklyn'
        if staten_island[0] == i[0]:
            return 'Staten Island'
    return {'data': [
                dict(
                    x = hour,
                    y = i,
                    name = get_name(i),
                    mode = 'lines+markers',
                    marker = {'size':8}
                )for i in [manhattan, queens, bronx, brooklyn, staten_island, total]
            ],
            'layout': dict(
                title = 'Number of {} per Hour by Borough'.format(complaint_type.title()),
                xaxis = {'title': 'Hour of the Day', 'tickangle': -45},
                yaxis = {'title': 'Number of {}'.format(complaint_type.title())},
                margin = {'l': 60, 'b': 60, 't': 25, 'r': 0},
                legend = {'x': 0.1, 'y': 1},
                hovermode = 'closest'
            )}


page_2_layout = html.Div([
    html.Hr(),
    html.H1(children = 'NYC Crime vs Income', style = {'textAlign': 'center'}),
    html.Hr(),
    html.Div([
        dcc.Graph(
            figure={
                'data': [
                    dict(
                        x = income['Borough'],
                        y = income[i],
                        name = i,
                        type = 'bar'
                    ) for i in ['Total households', 'Total Arrests']
                ],
                'layout': dict(
                    title = 'Number of Households and Arrests by Borough',
                    xaxis = {'title': 'Borough', 'tickangle': 0},
                    yaxis = {'title': 'Number of Households/People'},
                    margin = {'l': 60, 'b': 40, 't': 25, 'r': 0},
                    legend = {'x': 0.75, 'y': 0.9},
                    hovermode = 'closest'
                )
            }
        )
    ], style = {'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(
            figure={
                'data': [
                    dict(
                        x = income['Borough'],
                        y = income[i],
                        name = i,
                        type = 'bar',
                        marker = {'color': '#2ca02c' if i == 'Median household income (dollars)' else '#d62728'}
                    ) for i in ['Median household income (dollars)', 'Mean household income (dollars)']
                ],
                'layout': dict(
                    title = 'Household Income by Borough',
                    xaxis = {'title': 'Borough', 'tickangle': 0},
                    yaxis = {'title': 'Household Income'},
                    margin = {'l': 60, 'b': 40, 't': 25, 'r': 0},
                    legend = {'x': 0.6, 'y': 0.9},
                    hovermode = 'closest'
                )
            }
        )
    ], style = {'width': '50%', 'display': 'inline-block'}),
    html.Hr(),
    html.Div([
        dcc.Graph(
            id = 'income-specific-conditions'
        )
    ], style = {'width': '60%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.Label('X-axis'),
            dcc.RadioItems(
                id = 'income-x-label',
                options=[{'label': i, 'value': i} for i in ['Total households', 'Total Arrests', 'Median household income (dollars)', 'Mean household income (dollars)']],
                value = 'Total households'
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Y-axis'),
            dcc.RadioItems(
                id = 'income-y-label',
                options=[{'label': i, 'value': i} for i in ['Total households', 'Total Arrests', 'Median household income (dollars)', 'Mean household income (dollars)']],
                value = 'Total Arrests'
            )
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
        html.Hr(),
        dcc.Link(children = 'Link to NYPD Arrests Dataframe', href = 'https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u', target='_blank'),
        html.Hr(),
        dcc.Link(children = 'Link to NYC Economic Profile Dataframe', href = 'https://popfactfinder.planning.nyc.gov/profile/1188/economic', target='_blank')
    ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),

    html.Hr(),
    html.Div(style={'width': '20%', 'display': 'inline-block'}),
    html.Div(dcc.Link('NYC Crime vs Time of Day', href='/page-1'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Population', href='/page-3'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Education', href='/page-4'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('Go Back to Home', href='/'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Hr(),
    html.Div(children = 'Created by Birju Dhaduk for a CS 301 honors enhancement project', style = {'fontSize': '12px', 'textAlign': 'right'}),
    html.Hr()
])

@app.callback(
    dash.dependencies.Output('income-specific-conditions', 'figure'),
    [dash.dependencies.Input('income-x-label', 'value'),
     dash.dependencies.Input('income-y-label', 'value')])
def update_income_graph(x_label, y_label):
    def number_to_boro(num):
        if num == 0:
            return 'Brooklyn'
        if num == 1:
            return 'Bronx'
        if num == 2:
            return 'Manhattan'
        if num == 3:
            return 'Queens'
        return 'Staten Island'
    return {'data': [
                dict(
                    x = [income[x_label][i]],
                    y = [income[y_label][i]],
                    name = number_to_boro(i),
                    mode = 'markers',
                    marker = {'size':15}
                )for i in [2, 3, 1, 0, 4]
            ],
            'layout': dict(
                title = x_label + ' vs. ' + y_label,
                xaxis = {'title': x_label, 'tickangle': 0},
                yaxis = {'title': y_label},
                margin = {'l': 60, 'b': 60, 't': 25, 'r': 25},
                legend = {'x': 0.1, 'y': 1},
                hovermode = 'closest'
            )}


page_3_layout = html.Div([
    html.Hr(),
    html.H1(children = 'NYC Crime vs Population', style = {'textAlign': 'center'}),
    html.Hr(),
    html.Div([
        dcc.Graph(
            id = 'pop-specific-conditions'
        )
    ], style = {'width': '60%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.Label('X-axis'),
            dcc.RadioItems(
                id = 'pop-x-label',
                options=[
                    {'label': 'Population', 'value': 'POPULATION'},
                    {'label': 'Number of Arrests', 'value': 'NUM_ARRESTS'},
                    {'label': 'Land Area', 'value': 'LAND_AREA'},
                    {'label': 'Population Density', 'value': 'POP_DENSITY'},
                    {'label': 'Percent of Arrests per Population', 'value': 'ARRESTS/POPULATION%'},
                    {'label': 'Number of Arrests per Square Mile', 'value': 'ARRESTS_PER_MILE'},
                    {'label': 'Number of Arrests per Day', 'value': 'ARRESTS_PER_DAY'}
                ],
                value = 'POPULATION'
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Y-axis'),
            dcc.RadioItems(
                id = 'pop-y-label',
                options=[
                    {'label': 'Population', 'value': 'POPULATION'},
                    {'label': 'Number of Arrests', 'value': 'NUM_ARRESTS'},
                    {'label': 'Land Area', 'value': 'LAND_AREA'},
                    {'label': 'Population Density', 'value': 'POP_DENSITY'},
                    {'label': 'Percent of Arrests per Population', 'value': 'ARRESTS/POPULATION%'},
                    {'label': 'Number of Arrests per Square Mile', 'value': 'ARRESTS_PER_MILE'},
                    {'label': 'Number of Arrests per Day', 'value': 'ARRESTS_PER_DAY'}
                ],
                value = 'NUM_ARRESTS'
            )
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
        html.Hr(),
        dcc.Link(children = 'Link to NYPD Arrests Dataframe', href = 'https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u', target='_blank'),
        html.Hr(),
        dcc.Link(children = 'Link to NYC Population Dataframe', href = 'https://data.cityofnewyork.us/City-Government/New-York-City-Population-By-Neighborhood-Tabulatio/swpk-hqdp/data', target='_blank')
    ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),
    
    html.Hr(),
    html.Div(style={'width': '20%', 'display': 'inline-block'}),
    html.Div(dcc.Link('NYC Crime vs Time of Day', href='/page-1'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Income', href='/page-2'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Education', href='/page-4'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('Go Back to Home', href='/'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Hr(),
    html.Div(children = 'Created by Birju Dhaduk for a CS 301 honors enhancement project', style = {'fontSize': '12px', 'textAlign': 'right'}),
    html.Hr()
])

@app.callback(
    dash.dependencies.Output('pop-specific-conditions', 'figure'),
    [dash.dependencies.Input('pop-x-label', 'value'),
     dash.dependencies.Input('pop-y-label', 'value')])
def update_income_graph(x_value, y_value):
    def number_to_boro(num):
        if num == 0:
            return 'Brooklyn'
        if num == 1:
            return 'Bronx'
        if num == 2:
            return 'Manhattan'
        if num == 3:
            return 'Queens'
        return 'Staten Island'
    def value_to_label(value):
        if value == 'POPULATION':
            return 'Population'
        if value == 'NUM_ARRESTS':
            return 'Number of Arrests'
        if value == 'LAND_AREA':
            return 'Land Area'
        if value == 'POP_DENSITY':
            return 'Population Density'
        if value == 'ARRESTS/POPULATION%':
            return 'Percent of Arrests per Population'
        if value == 'ARRESTS_PER_MILE':
            return 'Number of Arrests per Square Mile'
        if value == 'ARRESTS_PER_DAY':
            return 'Number of Arrests per Day'
    return {'data': [
                dict(
                    x = [pop[x_value][i]],
                    y = [pop[y_value][i]],
                    name = number_to_boro(i),
                    mode = 'markers',
                    marker = {'size':15}
                )for i in [2, 3, 1, 0, 4]
            ],
            'layout': dict(
                title = value_to_label(x_value) + ' vs. ' + value_to_label(y_value),
                xaxis = {'title': value_to_label(x_value), 'tickangle': 0},
                yaxis = {'title': value_to_label(y_value)},
                margin = {'l': 60, 'b': 60, 't': 25, 'r': 25},
                legend = {'x': 0.1, 'y': 1},
                hovermode = 'closest'
            )}


page_4_layout = html.Div([
    html.Hr(),
    html.H1(children = 'NYC Crime vs Education', style = {'textAlign': 'center'}),
    html.Hr(),
    html.Div([
        dcc.Graph(
            id = 'edu-specific-conditions'
        )
    ], style = {'width': '60%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.Label('X-axis'),
            dcc.RadioItems(
                id = 'edu-x-label',
                options=[
                    {'label': 'Total Cohort Num', 'value': 'Total Cohort Num'},
                    {'label': 'Dropped Out Num', 'value': 'Dropped Out Num'},
                    {'label': 'Population', 'value': 'Population'},
                    {'label': 'Amount of Arrest', 'value': 'Amount of Arrest'}
                ],
                value = 'Total Cohort Num'
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Y-axis'),
            dcc.RadioItems(
                id = 'edu-y-label',
                options=[
                    {'label': 'Total Cohort Num', 'value': 'Total Cohort Num'},
                    {'label': 'Dropped Out Num', 'value': 'Dropped Out Num'},
                    {'label': 'Population', 'value': 'Population'},
                    {'label': 'Amount of Arrest', 'value': 'Amount of Arrest'}
                ],
                value = 'Dropped Out Num'
            )
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
        html.Hr(),
        dcc.Link(children = 'Link to NYC Graduation Dataframe', href = 'https://data.cityofnewyork.us/Education/2005-2011-Graduation-Outcomes-Borough-Total-Cohort/di8r-g5w9', target='_blank'),
        html.Hr(),
        dcc.Link(children = 'Link to NYPD Arrests Dataframe', href = 'https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u', target='_blank'),
        html.Hr(),
        dcc.Link(children = 'Link to NYC Population Dataframe', href = 'https://data.cityofnewyork.us/City-Government/New-York-City-Population-By-Neighborhood-Tabulatio/swpk-hqdp/data', target='_blank')
    ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),
    
    html.Hr(),
    html.Div(style={'width': '20%', 'display': 'inline-block'}),
    html.Div(dcc.Link('NYC Crime vs Time of Day', href='/page-1'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Income', href='/page-2'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('NYC Crime vs Population', href='/page-3'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Div(dcc.Link('Go Back to Home', href='/'), style={'width': '15%', 'display': 'inline-block', 'textAlign': 'center'}),
    html.Hr(),
    html.Div(children = 'Created by Birju Dhaduk for a CS 301 honors enhancement project', style = {'fontSize': '12px', 'textAlign': 'right'}),
    html.Hr()
])

@app.callback(
    dash.dependencies.Output('edu-specific-conditions', 'figure'),
    [dash.dependencies.Input('edu-x-label', 'value'),
     dash.dependencies.Input('edu-y-label', 'value')])
def update_income_graph(x_value, y_value):
    def number_to_boro(num):
        if num == 0:
            return 'Brooklyn'
        if num == 1:
            return 'Bronx'
        if num == 2:
            return 'Manhattan'
        if num == 3:
            return 'Queens'
        return 'Staten Island'
    return {'data': [
                dict(
                    x = [edu[x_value][i]],
                    y = [edu[y_value][i]],
                    name = number_to_boro(i),
                    mode = 'markers',
                    marker = {'size':15}
                )for i in [2, 3, 1, 0, 4]
            ],
            'layout': dict(
                title = x_value + ' vs. ' + y_value,
                xaxis = {'title': x_value, 'tickangle': 0},
                yaxis = {'title': y_value},
                margin = {'l': 60, 'b': 60, 't': 25, 'r': 25},
                legend = {'x': 0.1, 'y': 1},
                hovermode = 'closest'
            )}


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
