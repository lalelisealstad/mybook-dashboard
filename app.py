import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# import plotly.express as px
# import plotly.graph_objs as go
import pandas as pd 
import json
import numpy as np
from apps.viz import *
from apps.dataimport import *
from apps.collect_data import *
from datetime import datetime
import base64
import io
import pandas as pd
import logging


from apps.async_googleapi import book_info_add, asyncio
from apps.api import api_key
from apps.prediction import make_genre_tbl, ml_genre


# Configure logging to see errors in gcp 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#  Create a Dash web application
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=0.9, maximum-scale=1.2, minimum-scale=0.5,'}])


# Define the layout of the app with rows and columns using Bootstrap grid system
app.layout = html.Div([
        html.Div([
            dbc.Container([
                dbc.Row(
                    dbc.Col(
                        [
                            html.H1("Book dashboard", className="my-4 text-center",style={'color': '#2B2B35', 'text-align': 'center'},),
                            html.H6("Visualising statistics of read books", style={'color': '#2B2B35', 'text-align': 'center'},),
                        ],
                    style={'background-color': '#D6C9F2'}, className='five columns')
            ,justify="center"),
            
            # row to upload books 
            dbc.Row([
                dbc.Col(
                    [
                        dcc.Markdown(id='data-info-text1', dangerously_allow_html=True, style={'font-size': '16px'}),
                        dcc.Markdown(id='data-info-text2', dangerously_allow_html=True, style={'font-size': '11px'}),
                    ],xs=10, sm=10, md=10, lg=5, xl=5
                ),
                dbc.Col([
                    dbc.Spinner(children=[
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files', style={'color': 'blue', 'font-weight': 'bold'}), 
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
                        dcc.Markdown(id='upload-text', dangerously_allow_html=True, style={'font-size': '11px',  'textAlign': 'center'}),
                    ]), 
                    dcc.Markdown('''Upload may take a while depending on library size. Large libraries may take up to 15 minutes..''', style={'font-size': '11px',  'textAlign': 'center'})]
                    ,xs=10, sm=10, md=10, lg=5, xl=5
                )
            ], className="mt-2", style={'color': '#2B2B35'}, justify="center"), 
            
            # row with text summarising year in books

            # dbc.Row([
            #     dbc.Col(
            #             html.Div(id='data-info-text3'),
            #             # (f"This year I have read over {len(myreads.query('Year == @today_year'))} books. Totaling {f'{(myreads.Number_of_Pages.sum().astype(int)):,}'} pages read!", style={'color': '#2B2B35', 'text-align': 'center'}),
            #         xs=10, sm=10, md=10, lg=5, xl=5
            #     ),
            # ], className="mt-6", style={'height': '40px', 'font-size': '16px'}, justify="center"), 

            # First row with figures
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig1'
                        # figure=viz_pub_year(myreads),
                    )
                    ,xs=12, sm=12, md=12, lg=5, xl=5
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig2'
                    )
                    ,xs=12, sm=12, md=12, lg=5, xl=5
                ),
            ],className="mt-2", justify="center"),

            # Second row with bar charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='fig3'
                    )
                    ,xs=12, sm=12, md=12, lg=5, xl=5
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fig4'
                    )
                    ,xs=12, sm=12, md=12, lg=5, xl=5
                ),
            ], className="mt-4", justify="center"),  

            # Third row - pie charts
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='viztop1',
                    )
                    ,xs=12, sm=12, md=12, lg=5, xl=5
                ),
                dbc.Col(
                    dcc.Graph(
                        id='viztop2',
                    )
                    ,xs=12, sm=12, md=12, lg=5, xl=5
                ),
            ], className="mt-4", justify="center"),  

            # My top authors
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tbl1',
                    )
                    ,xs=12, sm=12, md=12, lg=5, xl=5
                    ),
                dbc.Col(
                    dcc.Graph(
                        id='tbl2',
                    )
                   ,xs=12, sm=12, md=12, lg=5, xl=5
                ),
            ], className="mt-4", justify="center"),

            # Rows for bottom and top rated books
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='figr1',
                    )
                    ,xs=12, sm=12, md=12, lg=5, xl=5
                    ),
            # ], className="mt-4", justify="center"), 
            # dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='figr2',
                    )
                   ,xs=12, sm=12, md=12, lg=5, xl=5
                ),
            ], className="mt-4", justify="center"),  
            
            # Sixth row with desc fig
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tree',
                    )
                    ,xs=12, sm=12, md=12, lg=10, xl=10
                ), 
            ], className="mt-4", justify="center"), 

            # Seventh row with topic fig
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='tree2'
                    )
                    ,xs=12, sm=12, md=12, lg=10, xl=10  
                ),
            ], className="mt-4", justify="center"),  
            
            # Eight row with scatter plot popularity
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='scatter-fig'
                    )
                    ,xs=12, sm=12, md=12, lg=10, xl=10
                ),
            ], className="mt-4", justify="center"),  
            
            # 9th row with lollipop
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='lolli-fig'
                    )
                    ,xs=12, sm=12, md=12, lg=10, xl=10
                ),
            ], className="mt-4", justify="center", style={'height': '810px'}),   
            
            # 10th row with spider
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='spider-fig'
                    )
                    ,xs=12, sm=12, md=12, lg=10, xl=10 
                ),
            ], className="mt-4", justify="center", style={'height': '610px'}),   
            
            # 11th row with scatter plot popularity
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='genre-timeline-fig'
                    )
                    ,xs=12, sm=12, md=12, lg=10, xl=10 
                ),
            ], className="mt-4", justify="center", style={'height': '710px'}),   
            
            html.Div([
                # dcc.Store inside the user's current browser session
                dcc.Store(id='store-data', data=[], storage_type='session'), # store of the list of read books
                dcc.Store(id='is-uploaded-data', data=[], storage_type='session')  # store binary showing if data is uploaded 
            ])
        ], fluid=True),
    ], style={'width': '100%', 'display': 'inline-block',
                                 'box-shadow': '2px 2px 2px lightgrey',
                                 'background-color': '#fcfcfc',
                                 'padding': '5px',
                                 'align':"center"
                                 }),  
])


server = app.server  # Get the underlying Flask server instance

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
        # Output('data-info-text3', 'children'),
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
        Output('is-uploaded-data', 'data'),
        Output('scatter-fig', 'figure'),
        Output('lolli-fig', 'figure'),
        Output('spider-fig', 'figure'),
        Output('genre-timeline-fig', 'figure')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)


# google api figures         
def update_figure_gapi(contents, filename):
    global myreads
    global nmyreads
    global genre_tbl
    global ngenre_tbl
    global allgenredf
    global nallgenredf
    
    if contents is None:
        # Use the default data if no file is uploaded
        if uploaded_data.empty:
            # Load your default data
            mybooks= pd.read_pickle('assets/my_books_genres.pickle')
            myreads = mybooks.loc[mybooks['Exclusive_Shelf'] == "read"].copy()
            uploadtxt_sug1 = "See your reading stats by uploading your Goodreads library export here:"
            uploadtxt_sug2 =  """How to find and export Goodreads library:<br>
                            1. Go to [your Goodreads profile](https://www.goodreads.com/?target=_blank)<br>
                            2. Click on "My Books"<br>
                            3. Scroll down and click on "Import/Export" under "Tools" on the left sidebar<br>
                            4. Click "Export Your Books" to download the export file"""
            year_text = f"This year I have read over {len(myreads.query('Year == @today_year'))} books. Totaling {(myreads.query('Year == @today_year').Number_of_Pages.sum().astype(int))} pages read!"
            myreads_list = myreads[['Author','Title']].to_dict()
            
            # genre table 
            from ast import literal_eval
            myreads['genres'] = myreads['genres'].apply(literal_eval).copy()
            allgenredf = myreads.query('genres != "[]"').copy().explode('genres')
            genre_tbl = make_genre_tbl(allgenredf)
             
            return (
                viz_pub_year(myreads), 
                uploadtxt_sug1, 
                uploadtxt_sug2, 
                viz_year_read(myreads), 
                # year_text, 
                visualize_categories(myreads.query('My_Rating >0 '), 'My_Rating', 'How do I rate my books?<br><span style="font-size: 8px;">Number of books per Ratings category</span>', 'Goodreads rating'), 
                visualize_categories(myreads, 'Page_Cat', 'How long are the books I read?<br><span style="font-size: 8px;">Number of books per Page Count</span>', 'Page Count'),
                viz_top_values(myreads['Language'], top_n=7),
                viz_top_values(myreads['Categories'], top_n=7),
                author_count_fig(myreads),
                author_rating_fig(myreads),
                book_ratings_top(myreads, 'Top Rated Books'),
                book_ratings_bottom(myreads, 'Lowest Rated Books'),
                ' ', 
                myreads_list, 
                False, 
                scatter_popularity(myreads),
                lolli_fig(genre_tbl),
                spider_fig(genre_tbl),
                stack_fig(allgenredf, genre_tbl)
            )

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        new_data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        print(new_data)
        nmyreads = new_data.loc[new_data['Exclusive Shelf'] == "read"].copy()
        logging.info('almost async')
        nmyreadsgg = asyncio.run(book_info_add(nmyreads, api_key))
        logging.info('ascync complete - requests complete')
        nmyreads = dataprep(nmyreads, nmyreadsgg)
        logging.info('dataprep completed')
        uploadtxt_suc = "Success, your data have been uploaded and the figures updated!"
        nyear_text = f"This year I have read over {len(nmyreads.query('Year == @today_year'))} books. Totaling {(nmyreads.query('Year == @today_year').Number_of_Pages.sum().astype(int))} pages read!"
        nmyreads_list = nmyreads[['Author','Title']].to_dict()
        
        n_fig1	 = 	viz_pub_year(nmyreads)
        n_data_info_text1	 = 	uploadtxt_suc
        n_data_info_text2	 = 	""
        n_fig2	 = 	viz_year_read(nmyreads)
        n_fig3	 = 	visualize_categories(nmyreads.query('My_Rating > 0'), 'My_Rating', 'How do I rate my books?<br><span style="font-size: 8px;">Number of books per Ratings category</span>', 'Goodreads rating')
        n_fig4	 = 	visualize_categories(nmyreads, 'Page_Cat', 'How long are the books I read?<br><span style="font-size: 8px;">Number of books per Page Count</span>', 'Page Count')
        n_viztop1	 = 	viz_top_values(nmyreads['Language'], top_n=7)
        n_viztop2	 = 	viz_top_values(nmyreads['Categories'], top_n=7)
        n_tbl1	 = 	author_count_fig(nmyreads)
        n_tbl2	 = 	author_rating_fig(nmyreads)
        n_figr1	 = 	book_ratings_top(nmyreads, 'Top Rated Books')
        n_figr2	 = 	book_ratings_bottom(nmyreads, 'Lowest Rated Books')
        n_upload_text	 = 	'Upload success'
        n_scatter_fig	 = 	scatter_popularity(nmyreads)
        
        
        
        # predict genre 
        # in case there is no description, then no genre 
        if nmyreads.Description.isna().all(): 
            fig = go.Figure()
            fig.update_layout(title='Goodreads library books do not have book description, therefore not able to predict genre')
            n_lolli_fig	 = 	fig
            n_spider_fig	 = 	fig
            n_genre_timeline_fig	 = 	fig
        else:     
            nmyreads = ml_genre(nmyreads)
            print('prediction complete')
            # genre table 
            from ast import literal_eval
            nmyreads['genres'] = nmyreads['genres'].apply(literal_eval)
            # pd.to_pickle(nmyreads,'assets/test.pkl') # for testing 
            nallgenredf = nmyreads.query('genres != "[]"').copy().explode('genres')
            print(nallgenredf)
            ngenre_tbl = make_genre_tbl(nallgenredf)
            
            n_lolli_fig	 = 	lolli_fig(ngenre_tbl)
            n_spider_fig	 = 	spider_fig(ngenre_tbl)
            n_genre_timeline_fig	 = 	stack_fig(nallgenredf, ngenre_tbl)
                    
                
        return(
            n_fig1	,
            n_data_info_text1	,
            n_data_info_text2	,
            n_fig2	,
            n_fig3	,
            n_fig4	,
            n_viztop1	,
            n_viztop2	,
            n_tbl1	,
            n_tbl2	,
            n_figr1	,
            n_figr2	,
            n_upload_text	,
            nmyreads_list	,
            True,
            n_scatter_fig	,
            n_lolli_fig	,
            n_spider_fig	,
            n_genre_timeline_fig) 
    
    
    except Exception as e:
        logging.error(f"An error occurred on line {e.__traceback__.tb_lineno}: {e}")
        uploadtxt_fail = f"Upload failiure...Are you using the csv file from Goodreads export?<br>Report error message: {str(e)}"
        year_text = f"This year I have read over {len(myreads.query('Year == @today_year'))} books. Totaling {(myreads.query('Year == @today_year').Number_of_Pages.sum().astype(int))} pages read!"
        myreads_list = myreads[['Author','Title']].to_dict()
        
        return (
            viz_pub_year(myreads), 
            uploadtxt_fail, 
            "", 
            viz_year_read(myreads), 
            # year_text, 
            visualize_categories(myreads.query('My_Rating > 0'), 'My_Rating', 'How do I rate my books?<br><span style="font-size: 8px;">Number of books per Ratings category</span>', 'Goodreads rating'),
            visualize_categories(myreads, 'Page_Cat', 'How long are the books I read?<br><span style="font-size: 8px;">Number of books per Page Count</span>', 'Page Count'),
            viz_top_values(myreads['Language'], top_n=7),
            viz_top_values(myreads['Categories'], top_n=7),
            author_count_fig(myreads),
            author_rating_fig(myreads),
            book_ratings_top(myreads, 'Top Rated Books'),
            book_ratings_bottom(myreads, 'Lowest Rated Books'),
            'upload fail', 
            myreads_list, 
            False, 
            scatter_popularity(myreads), 
            lolli_fig(genre_tbl),
            spider_fig(genre_tbl),
            stack_fig(allgenredf, genre_tbl), 
        )


# # app call back for the three figure using open library api
@app.callback(
    [Output('tree', 'figure')],
    [Input('store-data', 'data'),
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
@app.callback(
    [Output('tree2', 'figure')],
    [Input('is-uploaded-data', 'data')]
)
def update_figure_ol_api(isuploaded):    
    if isuploaded == True: 
        desctree = desc_tree(nmyreads['Description']),
    else: 
        desctree = desc_tree(myreads['Description']),
    return desctree

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080, use_reloader=False) # debug False in deployment