import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd 
import json
import numpy as np
from apps.viz import *
from apps.dataimport import *
from apps.collect_data import *
from datetime import datetime
import pickle 
import base64
import io
import requests
import pandas as pd
import aiohttp
import nest_asyncio
import time

from apps.async_googleapi import book_info_add 
import asyncio
from apps.api import api_key
async def get_ggl(books):
    global nmyreadsgg 
    nmyreadsgg = await book_info_add(books, api_key) 


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
                    style={'background-color': '#D6C9F2', 'size':10},
                width=10)
            ,justify="center"),
            
            # row to upload books 
            dbc.Row([
                dbc.Col(
                    [
                        dcc.Markdown(id='data-info-text1', dangerously_allow_html=True, style={'font-size': '16px'}),
                        dcc.Markdown(id='data-info-text2', dangerously_allow_html=True, style={'font-size': '11px'}),
                    ], 
                    width=5  # Width for the second column
                ),
                dbc.Col(
                    dbc.Spinner(children=[
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files', style={'color': 'blue', 'font-weight': 'bold'})
                            ]),
                            style={
                                'width': '100%',
                                'height': '100px',
                                'lineHeight': '100px',
                                'borderWidth': '2px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            multiple=False),  # Allow only one file upload at a time
                        dcc.Markdown(id='upload-text', dangerously_allow_html=True, style={'font-size': '11px'}),
                    ]),width=5 
                )
            ], className="mt-2", style={'color': '#2B2B35', 'height': '160px'}, justify="center"), 
            
            # row with text summarising year in books

            dbc.Row([
                dbc.Col(
                        html.Div(id='data-info-text3'),
                        # (f"This year I have read over {len(myreads.query('Year == @today_year'))} books. Totaling {f'{(myreads.Number_of_Pages.sum().astype(int)):,}'} pages read!", style={'color': '#2B2B35', 'text-align': 'center'}),
                    width=10 
                ),
            ], className="mt-6", style={'height': '30px', 'font-size': '16px'}, justify="center"), 

            # First row with figures
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig1'
                        # figure=viz_pub_year(myreads),
                    ),
                    width=5  # Width for the first column
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig2'
                    ),
                    width=5  
                ),
            ],className="mt-2", justify="center"),

            # Second row with bar charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig3'
                    ),
                    width=5  
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig4'
                    ),
                    width=5 
                ),
            ], className="mt-4", justify="center"),  # Add margin top

            # Third row - pie charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='viztop1',
                    ),
                    width=5  
                ),
                dbc.Col(
                    dcc.Graph(
                        id='viztop2',
                    ),
                    width=5  
                ),
            ], className="mt-4", justify="center"),  

            # Tables
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tbl1',
                    ),
                    width=5 
                    ),
                dbc.Col(
                    dcc.Graph(
                        id='tbl2',
                    ),
                    width=5  
                ),
            ], className="mt-4", justify="center"),   

            # Rows for bottom and top rated books
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='figr1',
                    ),
                    width=10 
                    ),
            ], className="mt-4", justify="center"), 
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='figr2',
                    ),
                    width=10  
                ),
            ], className="mt-4", justify="center"),  
            
            # Sixth row with desc fig
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tree2',
                    ),
                    width=10,
                ), 
            ], className="mt-4", style={'height': '420px'}, justify="center"), 

            # # Seventh row with topic fig
            # dbc.Row([
            #     dbc.Col(
            #         dcc.Graph(
            #             id='tree2'
            #         ),
            #         width=12  
            #     ),
            # ], className="mt-0"), 
            html.Div([
                # dcc.Store inside the user's current browser session
                dcc.Store(id='store-data', data=[], storage_type='session'), # store of the list of read books
                dcc.Store(id='is-uploaded-data', data=[], storage_type='session')  # store binary showing if data is uploaded 
            ])
        ], fluid=True),
    ], style={'width': '100%', 'display': 'inline-block',
                                 'box-shadow': '2px 2px 2px lightgrey',
                                 'background-color': '#fcfcfc',
                                 'padding': '10px',
                                 'align':"center"

                                 }),  
])

 ### CALLBACKS


# Initialize an empty DataFrame to store uploaded data
uploaded_data = pd.DataFrame()
my_read_topics = {}
today_year = datetime.today().year

# Callback to update the line chart with uploaded data
@app.callback(
    [
        Output('fig1', 'figure'),
        Output('data-info-text1', 'children'),
        Output('data-info-text2', 'children'),
        Output('fig2', 'figure'),
        Output('data-info-text3', 'children'),
        Output('fig3', 'figure'),
        Output('fig4', 'figure'),
        Output('viztop1', 'figure'),
        Output('viztop2', 'figure'),
        Output('tbl1', 'figure'),
        Output('tbl2', 'figure'),
        Output('figr1', 'figure'),
        Output('figr2', 'figure'),
        Output('upload-text', 'children'),
        Output('store-data', 'data'), 
        Output('is-uploaded-data', 'data')
        ],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)


# google api figures         
def update_figure_gapi(contents, filename):
    global myreads
    
    if contents is None:
        # Use the default data if no file is uploaded
        if uploaded_data.empty:
            # Load your default data
            mybooks = pd.read_pickle("assets/my_books.pkl")
            myreads = mybooks.loc[mybooks['Exclusive_Shelf'] == "read"]
            uploadtxt_sug1 = "See your reading stats by uploading your Goodreads library export here:"
            uploadtxt_sug2 =  """How to find and export Goodreads library:<br>
                            1. Go to [your Goodreads profile](https://www.goodreads.com/?target=_blank)<br>
                            2. Click on "My Books"<br>
                            3. Scroll down and click on "Import/Export" under "Tools" on the left sidebar<br>
                            4. Click "Export Your Books" to download the export file"""
            year_text = f"This year I have read over {len(myreads.query('Year == @today_year'))} books. Totaling {f'{(myreads.Number_of_Pages.sum().astype(int)):,}'} pages read!"
            myreads_list = myreads.Title.to_list()
             
            return (
                viz_pub_year(myreads), 
                uploadtxt_sug1, 
                uploadtxt_sug2, 
                viz_year_read(myreads), 
                year_text, 
                visualize_categories(myreads, 'My_Rating', 'How do I rate my books?<br><span style="font-size: 8px;">Number of books per Ratings category</span>', 'Goodreads rating'), 
                visualize_categories(myreads, 'Page_Cat', 'How long are the books I read?<br><span style="font-size: 8px;">Number of books per Page Count Category</span>', 'Page Count Category'),
                viz_top_values(myreads['Language'], top_n=7),
                viz_top_values(myreads['Categories'], top_n=7),
                create_rating_table(myreads),
                create_author_table(myreads),
                book_ratings(myreads, 'Top Rated Books', top_rated=True, show_legend=True),
                book_ratings(myreads, 'Bottom Rated Books',top_rated=False, show_legend=False),
                # desc_tree(myreads['Description']),
                ' ', 
                myreads_list, 
                False
            )

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        new_data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        nmyreads = new_data.loc[new_data['Exclusive Shelf'] == "read"]

        asyncio.run(get_ggl(nmyreads))

        nmyreads = dataprep(nmyreads, nmyreadsgg)
        print('dataprep completed')
        uploadtxt_suc = "Success, your data have been uploaded and the figures updated!"
        nyear_text = f"This year I have read over {len(nmyreads.query('Year == @today_year'))} books. Totaling {(nmyreads.Number_of_Pages.sum().astype(int))} pages read!"
        nmyreads_list = nmyreads.Title.to_list()
        
        return(
            viz_pub_year(nmyreads), 
            uploadtxt_suc, 
            "", 
            viz_year_read(nmyreads), 
            nyear_text, 
            visualize_categories(nmyreads, 'My_Rating', 'How do I rate my books?<br><span style="font-size: 8px;">Number of books per Ratings category</span>', 'Goodreads rating'),
            visualize_categories(nmyreads, 'Page_Cat', 'How long are the books I read?<br><span style="font-size: 8px;">Number of books per Page Count Category</span>', 'Page Count Category'),
            viz_top_values(nmyreads['Language'], top_n=7),
            viz_top_values(nmyreads['Categories'], top_n=7),
            create_rating_table(nmyreads),
            create_author_table(nmyreads),
            book_ratings(nmyreads, 'Top Rated Books', top_rated=True, show_legend=True),
            book_ratings(nmyreads, 'Bottom Rated Books',top_rated=False, show_legend=False),
            # desc_tree(nmyreads['Description']),
            'Upload success', 
            nmyreads_list, 
            True
        )
    
    except Exception as e:
        print(str(e))
        uploadtxt_fail = "Upload failiure...Are you using the csv file from Goodreads export?"
        year_text = f"This year I have read over {len(myreads.query('Year == @today_year'))} books. Totaling {(myreads.Number_of_Pages.sum().astype(int))} pages read!"
        myreads_list = myreads.Title.to_list()
        
        return (
            viz_pub_year(myreads), 
            uploadtxt_fail, 
            "", 
            viz_year_read(myreads), 
            year_text, 
            visualize_categories(myreads, 'My_Rating', 'How do I rate my books?<br><span style="font-size: 8px;">Number of books per Ratings category</span>', 'Goodreads rating'),
            visualize_categories(myreads, 'Page_Cat', 'How long are the books I read?<br><span style="font-size: 8px;">Number of books per Page Count Category</span>', 'Page Count Category'),
            viz_top_values(myreads['Language'], top_n=7),
            viz_top_values(myreads['Categories'], top_n=7),
            create_rating_table(myreads),
            create_author_table(myreads),
            book_ratings(myreads, 'Top Rated Books', top_rated=True, show_legend=True),
            book_ratings(myreads, 'Bottom Rated Books',top_rated=False, show_legend=False),
            # desc_tree(myreads['Description']),
            'upload fail', 
            myreads_list, 
            False
            
        )


# # app call back for the three figure using open library api
@app.callback(
    [Output('tree2', 'figure')],
    [Input('store-data', 'data'),
    Input('is-uploaded-data', 'data')]
)
# open library API figures

def update_figure_ol_api(data, isuploaded):    
    # if isuploaded == True: 
    #     nmy_topics = get_book_topics(nmyreads)
    # #   nmy_read_topics = dict(nmy_topics)
    #     my_read_topics = {k: v for k, v in my_topics.items() if k in data}  
    #     fig = tree_topics(my_read_topics)
    # else: 
        with open('assets/my_topics.json') as file:
            json_data = json.load(file)
        my_topics = dict(json_data)
        my_read_topics = {k: v for k, v in my_topics.items() if k in data}  
        fig = tree_topics(my_read_topics)
        return [fig]


    #     if new upload
    # try:
    #     nmy_topics = get_book_topics(nmyreads)
    #     nmy_read_topics = dict(nmy_topics)
    # except Exception as e:
    #     return tree_topics(my_read_topics)

if __name__ == '__main__':
    app.run_server(debug=True)