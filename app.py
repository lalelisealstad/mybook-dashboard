import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

# Sample data for your figures (replace with your own data)
data = [
    {'Category': 'A', 'Value': 10},
    {'Category': 'B', 'Value': 15},
    {'Category': 'C', 'Value': 7},
]

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the app with rows and columns
app.layout = html.Div([
    html.H1("Your Dashboard Title"),

    # First row with two figures side by side
    html.Div([
        html.Div([
            dcc.Graph(
                id='scatter-plot',
                figure={
                    'data': [
                        go.Scatter(
                            x=[1, 2, 3],
                            y=[4, 1, 2],
                            mode='lines+markers',
                            name='Line Plot',
                        ),
                    ],
                    'layout': go.Layout(
                        title='Scatter Plot',
                        xaxis={'title': 'X-Axis'},
                        yaxis={'title': 'Y-Axis'},
                    )
                }
            ),
        ], className='six columns'),  # Specify the width of the column (6 out of 12)

        html.Div([
            dcc.Graph(
                id='bar-chart',
                figure={
                    'data': [
                        go.Bar(
                            x=['A', 'B', 'C'],
                            y=[10, 15, 7],
                            name='Bar Chart',
                        ),
                    ],
                    'layout': go.Layout(
                        title='Bar Chart',
                        xaxis={'title': 'Category'},
                        yaxis={'title': 'Value'},
                    )
                }
            ),
        ], className='six columns'),  # Specify the width of the column (6 out of 12)
    ], className='row'),  # Create a row to contain the figures

    # Second row with a component (e.g., dropdown) and a figure
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Option 1', 'value': 'opt1'},
                    {'label': 'Option 2', 'value': 'opt2'},
                ],
                value='opt1',
            ),
        ], className='three columns'),  # Specify the width of the column (3 out of 12)

        html.Div([
            dcc.Graph(
                id='line-chart',
                figure={
                    'data': [
                        go.Scatter(
                            x=[1, 2, 3],
                            y=[4, 2, 3],
                            mode='lines+markers',
                            name='Line Chart',
                        ),
                    ],
                    'layout': go.Layout(
                        title='Line Chart',
                        xaxis={'title': 'X-Axis'},
                        yaxis={'title': 'Y-Axis'},
                    )
                }
            ),
        ], className='nine columns'),  # Specify the width of the column (9 out of 12)
    ], className='row'),  # Create another row for the dropdown and line chart

])

if __name__ == '__main__':
    app.run_server(debug=True)
