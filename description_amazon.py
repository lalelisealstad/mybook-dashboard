import asyncio
import pandas as pd 
from apps.async_googleapi import book_info_add, asyncio
from apps.api import api_key
from apps.collect_data import *

amazondf = pd.read_pickle('assets/amazon_books.pkl')

amazondf_already = pd.read_pickle('assets/amazon_books_description.pkl')
mazondf_already_list = amazondf_already.Title.tolist()

amazondfsample = amazondf.query('Title not in @mazondf_already_list')

min_count = 80 #change to 80 
# Use groupby and apply to sample each group equally
dfcall = amazondfsample.groupby('genre', group_keys=False).apply(lambda x: x.sample(min_count))

n = 400
dfcall_limit = dfcall.sample(n)
filename = 'assets/amazon_books_description.pkl'

# Async function to handle the process
async def process_data(df, api_key, filename):
    print(df)
    books_desc = await book_info_add(df, api_key)
    books_desc_genre = books_desc.merge(dfcall_limit[['Title', 'genre']], how='left', left_on='Title_org', right_on='Title')
    books_desc_genre = books_desc_genre.drop(columns='Title_y').rename(columns={'Title_x':'Title'})
    amazondfnew = pd.concat([amazondf_already, books_desc_genre])

    amazondfnew.to_pickle(filename)
# Run the asynchronous code
asyncio.run(process_data(dfcall_limit, api_key, filename))

