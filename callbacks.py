import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import json

from dash.exceptions import PreventUpdate

from server import app
import data

@app.callback(
    [Output('country_map', 'children'), Output('card', 'children')],
    [Input('selected_country', 'value')], 
)
def update_map(country):
    if country is None:
        raise PreventUpdate
    else:

        #Map plot
        country_info = data.df_cases_country.loc[[country]]
                
        fig = px.choropleth_mapbox(country_info,
            geojson=data.geo['features'][data.map_features[country]], 
            color="Country_Region",
            locations="ISO3", featureidkey = "properties.ISO_A3",
            mapbox_style="carto-positron", zoom=3,
            center={"lat": country_info['Lat'][0], "lon": country_info['Long_'][0]},
        )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)

        map_plot = dcc.Graph(figure=fig)

        #Card
        card = dbc.Card([
            dbc.CardBody([
                html.H4("Covid-19", className="card-title"),
                html.Hr(),
                html.P([f"Number of cases: {int(country_info.Confirmed[0]):,d}"], className="card-subtitle h6 mb-3"),
                html.P([f"Deaths: {int(country_info.Deaths[0]):,d}"], className="card-subtitle h6 mb-3"),
                html.P([f"Recovered: {int(country_info.Recovered[0]):,d}"], className="card-subtitle h6 mb-3"),
                html.P([f"Active: {int(country_info.Active[0]):,d}"], className="card-subtitle h6 mb-3"),
                html.P([f"Incident Rate: {country_info.Incident_Rate[0]/100:.2%}"], className="card-subtitle h6 mb-3"),
                html.P([f"Mortality Rate: {country_info.Mortality_Rate[0]/100:.2%}"], className="card-subtitle h6 mb-3"),

            ]),
        ],
        className='w-100 mb-3')

       
        return map_plot, card


@app.callback(
    Output('mobility_plot', 'children'),
    [Input('selected_country', 'value')]
)
def update_mobility(country):
    if country is None:
        PreventUpdate
    else:

        df = data.df_mobility.loc[[country], :]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(x=df.date, y=df.residential_percent_change_from_baseline, 
                        name='Residential percent change',
                        mode='lines')
        )

        fig.add_trace(
            go.Scatter(x=df.date, y=df.retail_and_recreation_percent_change_from_baseline, 
                        name='Retail and recreation percent change',
                        mode='lines')
        )

        fig.add_trace(
            go.Scatter(x=df.date, y=df.transit_stations_percent_change_from_baseline, 
                        name='Transit stations percent change',
                        mode='lines')
        )
                                                        
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
          
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        

        return dcc.Graph(figure=fig)

