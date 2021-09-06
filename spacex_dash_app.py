# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'ALL Sites', 'value': 'ALL'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}
                                            ],
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True                                                
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0,
                                    max=10000,
                                    value=[min_payload, max_payload],
                                    marks={
                                        0: '0 kg',
                                        1000: '1000 kg',
                                        2000: '2000 kg',
                                        3000: '3000 kg',
                                        4000: '4000 kg',
                                        5000: '5000 kg',
                                        6000: '6000 kg',
                                        7000: '7000 kg',
                                        8000: '8000 kg',
                                        9000: '9000 kg',
                                        10000: '10000 kg',
                                    },
                                    step=1000
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))
def get_graph(launch_site):
    if launch_site=='ALL':
        df = spacex_df[spacex_df['class']==1]
        fig = px.pie(df, values='class', names='Launch Site', title='Success Launches for All Sites')
    else:
        tmp_df = spacex_df[spacex_df['Launch Site']==launch_site]
        total = len(tmp_df)
        success = int(tmp_df['class'].sum())
        names = ['Success', 'Failed']
        values = [success, total-success]
        fig = px.pie(tmp_df, values=values, names=names, title='Success Launches for {site_name}'.format(site_name=launch_site))
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_graph(launch_site, payload):
    tmp_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]
    if launch_site!='ALL':
        tmp_df = tmp_df[tmp_df['Launch Site']==launch_site]        
    fig = px.scatter(tmp_df, x='Payload Mass (kg)', y='class', color="Booster Version Category")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
