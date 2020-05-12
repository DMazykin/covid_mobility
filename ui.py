import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import data

import plotly.express as px




page_layout = dbc.Container([
    dbc.Jumbotron([
            html.H4("Covid-19: Mobility overview", className="display-4"),
            html.P(["Data aimed to help with adjustment for MTPL business"], className="lead"),
            html.Hr(className="my-2"),
            html.P(
                ["Based on Google Community Mobility Reports: ", html.A('link', href="https://www.google.com/covid19/mobility/")],
            )
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Container([
                dbc.Select(
                    id="selected_country",
                    options=data.country_list,
                ),
                html.Div(id='card', style={'margin-top': '1rem'})
            ],
            fluid=True, 
            style={'margin-top': '2rem'})
        ], width=2),
        dbc.Col([
            html.Div(
                id='country_map',
                style={'margin-top': '2rem'})
        ], width=3),
        dbc.Col([
            dbc.Container(
                id='mobility_plot',
                style={'margin-top': '2rem'})
        ], width=7)
    ])
    

], fluid=True)