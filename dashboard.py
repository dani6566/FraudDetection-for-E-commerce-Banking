import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import requests
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout for the dashboard
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Fraud Detection Dashboard"), className="text-center my-4")
        ]),

        dbc.Row([
            # Summary boxes with card styling
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H3("Total Transactions"),
                    html.H4(id='total-transactions', className="card-text")
                ]),
                className="text-center my-2 shadow-sm"
            )),
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H3("Total Fraud Cases"),
                    html.H4(id='total-fraud-cases', className="card-text")
                ]),
                className="text-center my-2 shadow-sm"
            )),
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H3("Fraud Percentage"),
                    html.H4(id='fraud-percentage', className="card-text")
                ]),
                className="text-center my-2 shadow-sm"
            )),
        ], className="mb-5"),

        # Fraud by country (map chart)
        dbc.Row([
            dbc.Col([
                html.H5("Fraud Cases by Country"),
                dcc.Graph(id='fraud-by-country-map')
            ])
        ], className="mb-5"),

        # Fraud trends over time (line chart)
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='fraud-trends-chart')
            ])
        ], className="mb-5"),

        # Fraud by browser (bar chart)
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='fraud-by-browser-chart')
            ])
        ]),
    ])
])

# Callback to update summary boxes
@app.callback(
    [Output('total-transactions', 'children'),
     Output('total-fraud-cases', 'children'),
     Output('fraud-percentage', 'children')],
    Input('total-transactions', 'id')
)
def update_summary(_):
    response = requests.get('http://localhost:5000/summary')
    summary_data = response.json()

    return (summary_data['total_transactions'],
            summary_data['total_fraud_cases'],
            f"{summary_data['fraud_percentage']:.2f}%")

# Callback to update fraud trends chart
@app.callback(
    Output('fraud-trends-chart', 'figure'),
    Input('fraud-trends-chart', 'id')
)
def update_fraud_trends(_):
    response = requests.get('http://localhost:5000/fraud-trends')
    fraud_trends_data = response.json()

    dates = list(fraud_trends_data.keys())
    fraud_counts = list(fraud_trends_data.values())

    return {
        'data': [{
            'x': dates,
            'y': fraud_counts,
            'type': 'line',
            'name': 'Fraud Cases'
        }],
        'layout': {
            'title': 'Fraud Cases Over Time'
        }
    }

# Callback to update fraud by country map
@app.callback(
    Output('fraud-by-country-map', 'figure'),
    Input('fraud-by-country-map', 'id')
)
def update_country_map(_):
    response = requests.get('http://localhost:5000/fraud-by-country')
    fraud_by_country_data = response.json()

    countries = list(fraud_by_country_data.keys())
    fraud_counts = list(fraud_by_country_data.values())

    figure = {
        'data': [{
            'type': 'choropleth',
            'locations': countries,
            'locationmode': 'country names',
            'z': fraud_counts,
            'colorscale': 'Reds',
            'colorbar': {'title': 'Fraud Cases'},
        }],
        'layout': {
            'title': 'Fraud Cases by Country',
            'geo': {'scope': 'world'}
        }
    }
    return figure

# Callback to update fraud by browser chart
@app.callback(
    Output('fraud-by-browser-chart', 'figure'),
    Input('fraud-by-browser-chart', 'id')
)
def update_browser_chart(_):
    response = requests.get('http://localhost:5000/fraud-by-device-browser')
    data = response.json()

    browsers = list(data['fraud_by_browser'].keys())
    browser_fraud_counts = list(data['fraud_by_browser'].values())

    browser_chart = {
        'data': [{
            'x': browsers,
            'y': browser_fraud_counts,
            'type': 'bar',
            'name': 'Fraud by Browser'
        }],
        'layout': {
            'title': 'Fraud Cases by Browser'
        }
    }

    return browser_chart

if __name__ == '__main__':
    app.run_server(debug=True)
