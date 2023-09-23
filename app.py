import dash
from dash import dcc
# import dash_core_components as dcc
from dash import html
# import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd 
import json
import numpy as np
from apps.viz import *

## GET THE DATA
mybooks = pd.read_pickle('assets/my_books.pkl')
myreads = mybooks.query('Exclusive_Shelf == "read"')
myreads['Date_Read'] = myreads['Date_Read'].fillna(myreads['Date_Added'].copy())
myreads = myreads.sort_values(by='Date_Read')

#  Create a Dash web application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app with rows and columns using Bootstrap grid system
app.layout = dbc.Container([
    html.H1("Visualising my read books", className="mt-4"),  # Add margin top
    html.H5("Using Goodreads library export with Open Library API and Google Books API"),
    # First row with two columns
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='scatter-plot',
                figure=viz_pub_year(myreads)
            ),
            width=6  # Width for the first column
        ),
        dbc.Col(
            dcc.Graph(
                id='bar-chart',
                figure=viz_year_read(myreads)
            ),
            width=6  # Width for the second column
        ),
    ], className="mt-4"),  # Add margin top

    # Second row with a component (e.g., dropdown) and a figure
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='line-chart',
                figure=viz_top_values(mybooks['Language'], top_n=5)
            ),
            width=6  # Width for the line chart column
        ),
        dbc.Col(
            dcc.Graph(
                id='line-chart',
                figure=visualize_page_categories(myreads, 'Page_Cat')
            ),
            width=6  # Width for the line chart column
        ),
    ], className="mt-4"),  # Add margin top

    # Third row with a component (e.g., dropdown) and a figure
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='line-chart',
                figure=create_rating_table(myreads)
            ),
            width=5  # Width for the line chart column
            ),
        dbc.Col(
            dcc.Graph(
                id='line-chart',
                figure=create_author_table(myreads)
            ),
            width=7  # Width for the line chart column
        ),
    ], className="mt-4"),  # Add margin top   
    
    # Fourth row with a component (e.g., dropdown) and a figure
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='line-chart',
                figure=desc_tree(mybooks['Description'])
            ),
            width=12  # Width for the line chart column
        ),
    ], className="mt-2"),  # Add margin top   
], fluid=True)  # Use fluid=True for a full-width container


#desc_tree(mybooks['Description'])
if __name__ == '__main__':
    app.run_server(debug=True)