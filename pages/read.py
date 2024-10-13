
import dash
import dash
from dash import html, dcc , page_registry
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import logging
from datetime import datetime, timedelta
import base64
import io
import json

from apps.viz import *
from apps.dataimport import *
from apps.prediction import make_genre_tbl

from dash import dcc, html, Input, Output, State, callback, register_page

dash.register_page(__name__, path="/read")

layout = html.Div([
    html.P("", style={'color': '#2b2b35', 'text-align': 'center', 'font-size': '16px'}),
            # year-timeline
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='year-timeline'
                    )
                    ,xs=12, sm=12, md=10, lg=10, xl=10  
                ),
            ], className="mt-4", justify="center"),     
            
            # row with bar charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig3'
                    )
                    ,xs=12, sm=12, md=5, lg=5, xl=5
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig4'
                    )
                    ,xs=12, sm=12, md=5, lg=5, xl=5
                ),
            ], className="mt-4", justify="center"),  
        
            # publication year rating and read year-quarter
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig1'
                        # figure=viz_pub_year(myreads),
                    )
                    ,xs=12, sm=12, md=5, lg=5, xl=5
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig2'
                    )
                    ,xs=12, sm=12, md=5, lg=5, xl=5
                ),
            ],className="mt-2", justify="center"),

            # Third row - pie charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='viztop1',
                    )
                    ,xs=12, sm=12, md=5, lg=5, xl=5
                ),
                dbc.Col(
                    dcc.Graph(
                        id='viztop2',
                    )
                    ,xs=12, sm=12, md=5, lg=5, xl=5
                ),
            ], className="mt-4", justify="center"),  

            # My top authors
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tbl1',
                    )
                    ,xs=12, sm=12, md=5, lg=5, xl=5
                    ),
                dbc.Col(
                    dcc.Graph(
                        id='tbl2',
                    )
                   ,xs=12, sm=12, md=5, lg=5, xl=5
                ),
            ], className="mt-4", justify="center"),

            # Rows for bottom and top rated books
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='figr1',
                    )
                    ,xs=12, sm=12, md=5, lg=5, xl=5
                    ),
            # ], className="mt-4", justify="center"), 
            # dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='figr2',
                    )
                   ,xs=12, sm=12, md=5, lg=5, xl=5
                ),
            ], className="mt-4", justify="center"),  
            
            #row with desc fig
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tree',
                    )
                    ,xs=12, sm=12, md=10, lg=10, xl=10
                ), 
            ], className="mt-4", justify="center"), 

            # row with topic fig
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tree2'
                    )
                    ,xs=12, sm=12, md=10, lg=10, xl=10  
                ),
            ], className="mt-4", justify="center"),  
            
            # row with lollipop
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='lolli-fig'
                    )
                    ,xs=12, sm=12, md=10, lg=10, xl=10
                ),
            ], className="mt-4", justify="center", style={'height': '810px'}),   
            
            # row with spider
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='spider-fig'
                    )
                    ,xs=12, sm=12, md=10, lg=10, xl=10 
                ),
            ], className="mt-4", justify="center", style={'height': '610px'}),   
            
            # row with scatter plot popularity
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='genre-timeline-fig'
                    )
                    ,xs=12, sm=12, md=10, lg=10, xl=10 
                ),
            ], className="mt-4", justify="center", style={'height': '710px'}),   
])



# Callback to update the line chart with uploaded data
@callback(
    [
        Output('fig1', 'figure'),
        Output('fig2', 'figure'),
        Output('fig3', 'figure'),
        Output('fig4', 'figure'),
        Output('viztop1', 'figure'),
        Output('viztop2', 'figure'),
        Output('tbl1', 'figure'),
        Output('tbl2', 'figure'),
        Output('figr1', 'figure'),
        Output('figr2', 'figure'),
        Output('year-timeline', 'figure'), 
        Output('lolli-fig', 'figure'),
        Output('spider-fig', 'figure'),
        Output('genre-timeline-fig', 'figure'), 
            ],
    Input('store-read-data', 'data'))
# # another here
# # )


def make_figs(myreads_json): 

    myreads = pd.read_json(io.StringIO(myreads_json), orient='split')
    
    from ast import literal_eval
    myreads['genres'] = myreads['genres'].apply(literal_eval).copy()
    allgenredf = myreads.query('genres != "[]"').copy().explode('genres')
    genre_tbl = make_genre_tbl(allgenredf)

    # in case there is no description, then no genre 
    if myreads.Description.isna().all(): 
        fig = go.Figure()
        fig.update_layout(title='Goodreads library books do not have book description, therefore not able to predict genre')
        lolli_figure	 = 	fig
        spider_figure	 = 	fig
        genre_timeline_figure	 = 	fig
    else: 
        lolli_figure	 = lolli_fig(genre_tbl)
        spider_figure	 = 	spider_fig(genre_tbl)
        genre_timeline_figure	 = 	stack_fig(allgenredf, genre_tbl)

    return(
            viz_pub_year(myreads), 
            viz_year_read(myreads), 
            visualize_categories(myreads.query('My_Rating >0 '), 'My_Rating', 'How do I rate my books?<br><span style="font-size: 8px;">Number of books per Ratings category</span>', 'Goodreads rating'), 
            visualize_categories(myreads, 'Page_Cat', 'How long are the books I read?<br><span style="font-size: 8px;">Number of books per Page Count</span>', 'Page Count'),
            viz_top_values(myreads['Language'], top_n=7),
            viz_top_values(myreads['Categories'], top_n=7),
            author_count_fig(myreads),
            author_rating_fig(myreads),
            book_ratings_top(myreads, 'Top Rated Books'),
            book_ratings_bottom(myreads, 'Lowest Rated Books'),
            viz_read(myreads), 
            lolli_figure, 
            spider_figure, 
            genre_timeline_figure)






######################

# # app call back for the three figure using open library api
@callback(
    [Output('tree', 'figure')],
    [Input('store-read-topic-data', 'data'),
    Input('is-uploaded-data', 'data')]
)
# # app call back for the three figure using open library api

def update_figure_ol_api(data, isuploaded):    
    if isuploaded == True: 
        nmyreads = pd.DataFrame(data)
        nmy_topics = get_book_topics(nmyreads)
        fig = tree_topics(nmy_topics)
    else: 
        with open('assets/my_topics.json') as file:
            json_data = json.load(file)
        my_topics = dict(json_data)
        my_read_topics = {k: v for k, v in my_topics.items() if k in list(set(data['Title'].values()))}  
        fig = tree_topics(my_read_topics)
    return [fig]


# call back for the desc tree since the computation was previously slow (when using nltk, not doing that anymore) 
@callback(
    [Output('tree2', 'figure')],
    [Input('store-read-data', 'data')]
)
def update_figure_ol_api(myreads_json):    
    myreads = pd.read_json(io.StringIO(myreads_json), orient='split')

    desctree = desc_tree(myreads['Description']),
    return desctree