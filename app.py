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

## GET THE DATA - Goodreads pkl
mybooks = pd.read_pickle('assets/my_books.pkl')
myreads = mybooks.query('Exclusive_Shelf == "read"')
myreads.loc[myreads['Date_Read'].isnull(), 'Date_Read'] = myreads['Date_Added'].copy()
myreads = myreads.sort_values(by='Date_Read')

# GET DATA - topics json
import json

# Load JSON data from a file
with open('assets/my_topics.json') as file:
    json_data = json.load(file)

# Convert JSON data to a dictionary
my_topics = dict(json_data)
my_read_topics = {k: v for k, v in my_topics.items() if k in myreads.Title.to_list()}

# Finding todays year and the text for subtitle
from datetime import datetime
today_year = datetime.today().year

#  Create a Dash web application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Define the layout of the app with rows and columns using Bootstrap grid system
app.layout = html.Div([
        html.Div([
            dbc.Container([
                dbc.Row(
                    dbc.Col(
                        [
                            html.H1("Visualising my read books", className="my-4 text-center",style={'color': '#2B2B35', 'text-align': 'center'},),
                            html.H6("Using Goodreads library export with Open Library API and Google Books API", style={'color': '#2B2B35', 'text-align': 'center'},),
                        ],
                    # width={'size': 12, 'offset': 2}
                )
            , style={'background-color': '#FFEFFF'}),
            dbc.Row([
                dbc.Col(
                        html.H5(f"This year I have read over {len(myreads.query('Year == @today_year'))} books. Totaling {f'{(myreads.Number_of_Pages.sum().astype(int)):,}'} pages read!", style={'color': '#2B2B35', 'text-align': 'center'}),
                    width=12 
                ),
            ], className="mt-4", style={'height': '60px'}), 
            # First row with two columns
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig1',
                        figure=viz_pub_year(myreads),
                    ),
                    width=6  # Width for the first column
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig2',
                        figure=viz_year_read(myreads)
                    ),
                    width=6  # Width for the second column
                ),
            ],className="mt-2"),

            # Second row with bar charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig3',
                        figure=visualize_page_categories(myreads, 'My_Rating', 'How do I rate my books?<br><span style="font-size: 8px;">Number of books per Ratings category</span>', 'Goodreads rating')
                    ),
                    width=6  
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig4',
                        figure=visualize_page_categories(myreads, 'Page_Cat', 'How long are the books I read?<br><span style="font-size: 8px;">Number of books per Page Count Category</span>', 'Page Count Category')
                    ),
                    width=6 
                ),
            ], className="mt-0"),  # Add margin top

            # Third row - pie charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='pie1',
                        figure=viz_top_values(mybooks['Language'], top_n=7)
                    ),
                    width=6  
                ),
                dbc.Col(
                    dcc.Graph(
                        id='pie2',
                        figure=viz_top_values(mybooks['Categories'], top_n=7)
                    ),
                    width=6  
                ),
            ], className="mt-0"),  

            # Fourth row with ratings table and author table
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tbl1',
                        figure=create_rating_table(myreads)
                    ),
                    width=5 
                    ),
                dbc.Col(
                    dcc.Graph(
                        id='tbl2',
                        figure=create_author_table(myreads)
                    ),
                    width=7  
                ),
            ], className="mt-0"),   

            # Fifth row top and bottom books
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='figr1',
                        figure=book_ratings(myreads, 'Top Rated Books', top_rated=True, show_legend=True)
                    ),
                    width=7 
                    ),
                dbc.Col(
                    dcc.Graph(
                        id='figr2',
                        figure=book_ratings(myreads, 'Bottom Rated Books', top_rated=False,show_legend=False)
                    ),
                    width=5  
                ),
            ], className="mt-0", style={'height': '450px'}),  
            
            # Sixth row with desc fig
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tree1',
                        figure=desc_tree(mybooks['Description'])
                    ),
                    width=12 
                ),
            ], className="mt-0", style={'height': '420px'}), 

            # Seventh row with topic fig
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tree2',
                        figure=tree_topics(my_read_topics)
                    ),
                    width=12  
                ),
            ], className="mt-0"), 
        ], fluid=True),
    ], style={'margin': '0 40px'}),  # Adjust the margin values as needed
])


#desc_tree(mybooks['Description'])
if __name__ == '__main__':
    app.run_server(debug=True)