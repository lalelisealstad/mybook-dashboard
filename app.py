import dash
from dash import html, dcc, page_registry
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# from dash import dcc, html, Input, Output, State, callback, register_page
import logging
import pandas as pd
from datetime import datetime, timedelta
import base64
import io
import json


from apps.collect_data import *
from apps.async_googleapi import book_info_add, asyncio
from apps.api import api_key
from apps.prediction import make_genre_tbl, ml_genre
from apps.dataimport import *


# Configure logging to see errors in GCP
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a Dash web application
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUX],
                use_pages=True,  # Ensure this flag is true to enable the pages feature
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=0.9, maximum-scale=1.2, minimum-scale=0.5,'}], 
                suppress_callback_exceptions=True)

app.title = 'Book Dashboard'

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        dbc.Container([
            dbc.Row(
                dbc.Col(
                    [
                        html.H1("Book Dashboard", className="my-4 text-center heading"),
                        html.P("Welcome to the Book Reading Statistics Dashboard. Explore insightful data about your reading habits and uncover new insights into your literary adventures!",
                               className="subheading"),
                    ],
                    className='five columns box-background')
            , justify="center"),

            # Row to upload books
            dbc.Row([
                dbc.Col(
                    [
                        dcc.Markdown(id='data-info-text1', dangerously_allow_html=True, className="markdown-large"),
                        dcc.Markdown(id='data-info-text2', dangerously_allow_html=True, className="markdown-small"),
                    ], xs=10, sm=10, md=10, lg=5, xl=5
                ),
                dbc.Col([
                    dbc.Spinner(children=[
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files', className='upload-link'),
                            ]),
                            className="upload-area",
                            multiple=False),  # Allow only one file upload at a time
                        dcc.Markdown(id='upload-text', dangerously_allow_html=True, className="upload-text"),
                    ])
                ], xs=10, sm=10, md=10, lg=5, xl=5)
            ], className="upload-section", justify="center"),

            # Tabs and page navigation
            html.Div(
                [
                    dcc.Location(id="url", refresh="callback-nav"),
                    dcc.Tabs(
                        id='tabs', 
                        value='tab-1', 
                        children=[
                            dcc.Tab(label='Read', value='tab-1', className="tab", selected_className="tab--selected"),
                            dcc.Tab(label='Want to read', value='tab-2', className="tab", selected_className="tab--selected"),
                        ]
                    ),
                    dash.page_container
                ]
            ),

            # dcc.Store inside the user's current browser session
            html.Div([
                dcc.Store(id='store-read-topic-data', data=[], storage_type='session'),  # store dict read book topics
                dcc.Store(id='is-uploaded-data', data=[], storage_type='session'),  # store binary showing if data is uploaded
                dcc.Store(id='store-read-data', data=[], storage_type='session'), 
                dcc.Store(id='store-wanttoread-data', data=[], storage_type='session')
            ])
        ], fluid=True),
    ], className="main-container"),
])



@app.callback(
    Output("url", "href"),
    Input("tabs", "value")
)
def update_tab_content(value):  
    if value == "tab-2":
        return "/wanttoread"
    return "/read"




# # Initialize an empty DataFrame to store uploaded data
uploaded_data = pd.DataFrame()
my_read_topics = {}
today_year = datetime.today().year

# Callback to update the line chart with uploaded data
@app.callback(
        [Output('data-info-text1', 'children'),
        Output('data-info-text2', 'children'),
        Output('upload-text', 'children'),
        Output('store-read-topic-data', 'data'), 
        Output('is-uploaded-data', 'data'), 
        Output('store-read-data', 'data'), 
        Output('store-wanttoread-data', 'data')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)


# Store data  
def update_figure_gapi(contents, filename):
    
    if contents is None:
        # Use the default data if no file is uploaded
        if uploaded_data.empty:
            # Load your default data
            mybooks= pd.read_parquet('assets/my_books_genres.parquet', engine='pyarrow')
            myreads = mybooks.loc[mybooks['Exclusive_Shelf'] == "read"].copy()
            toreads = mybooks.loc[mybooks['Exclusive_Shelf'] == "to-read"].copy()
            uploadtxt_sug1 = "See your reading stats by uploading your Goodreads library export here:"
            uploadtxt_sug2 =  """How to find and export Goodreads library:<br>
                            1. Go to [your Goodreads profile](https://www.goodreads.com/?target=_blank)<br>
                            2. Click on "My Books". If you are on a mobile, go to [https://www.goodreads.com/review/import](https://www.goodreads.com/review/import)<br>
                            3. Scroll down and click on "Import/Export" under "Tools" on the left sidebar<br>
                            4. Click "Export Your Books" to download the export file<br><br>
                            Once you upload your data, you'll find insightful statistics and trends about your reading habits."""
            myreads_list = myreads[['Author','Title']].to_dict()
            
            myreads_json = myreads.to_json(orient='split')
            toreads_json = toreads.to_json(orient='split')
            return (
                uploadtxt_sug1, 
                uploadtxt_sug2,     
                'Upload may take a while depending on library size. Large libraries may take up to 10 minutes..', 
                myreads_list, 
                False,
                myreads_json,
                toreads_json
                )



    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        new_data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        logging.info('start async')
        nmyreadsgg = asyncio.run(book_info_add(new_data, api_key))
        logging.info('ascync complete - requests complete')
        new_data = dataprep(new_data, nmyreadsgg)
        logging.info('dataprep completed')
        nmyreads_list = nmyreads[['Author','Title']].to_dict()
        
        new_data = ml_genre(new_data)
        print('prediction complete')

        nmyreads = new_data.loc[new_data['Exclusive Shelf'] == "read"].copy()
        ntoreads = new_data.loc[new_data['Exclusive Shelf'] == "read"].copy()
        
        nmyreads_json = nmyreads.to_json(orient='split')
        ntoreads_json = ntoreads.to_json(orient='split')
        
#         # Year summary
        today = datetime.today()
        one_year_ago = today - timedelta(days=365)

#         n_fig1	 = 	viz_pub_year(nmyreads)
        n_data_info_text1	 = 	f"Your data have been uploaded and the figures updated. In the last 12 months you have read {len(nmyreads.query('Date_Read > @one_year_ago'))} books. Totaling {(nmyreads.query('Date_Read > @one_year_ago').Number_of_Pages.sum().astype(int))} pages read. <br><br>View the figures to discover how you rate your books, your most read authors, explore different genres and more. You can interact with the figures by hovering over points to see details or zoom in for a closer look. If you need to reset the figures, simply double-click on them. Enjoy exploring your reading stats!"
        n_data_info_text2	 = 	""
        n_upload_text	 = 	'Upload success'
                
        return(n_data_info_text1	,
            n_data_info_text2	,
            n_upload_text	,
            nmyreads_list	,
            True,
            nmyreads_json,
            nmyreads_json) 
    
    
    except Exception as e:
        logging.error(f"An error occurred on line {e.__traceback__.tb_lineno}: {e}")
        uploadtxt_fail = f"Upload failiure...Are you using the csv file from Goodreads export?<br>Report error message: {str(e)}"
        myreads_list = myreads[['Author','Title']].to_dict()
        
        return (
            uploadtxt_fail, 
            "", 
            'upload fail', 
            myreads_list, 
            False, 
            myreads_json,
            toreads_json
        )


server = app.server 
# Callbacks should be defined below

if __name__ == '__main__':
    # app.run_server(debug=False, host="0.0.0.0", port=8080, use_reloader=False)  # debug=False in deployment
    app.run_server(debug=True, host="0.0.0.0", port=8080)