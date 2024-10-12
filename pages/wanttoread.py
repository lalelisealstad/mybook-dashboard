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
from apps.collect_data import *
from apps.async_googleapi import book_info_add, asyncio
from apps.api import api_key
from apps.prediction import make_genre_tbl, ml_genre



# dash.register_page(__name__, path="/wanttoread")
dash.register_page(__name__)


layout = html.Div(
    html.P("page want to read", style={'color': '#2b2b35', 'text-align': 'center', 'font-size': '16px'}),
#             # year-timeline
)