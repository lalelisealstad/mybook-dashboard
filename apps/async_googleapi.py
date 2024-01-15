
import requests
import pandas as pd
import numpy as np
import aiohttp
import asyncio
import nest_asyncio
import time

async def get_book_info_async(session, book_name, author_name, api_key):
    book_name = book_name
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': f'intitle:{book_name}+inauthor:{author_name}',
        'key': api_key,
        'maxResults': 1,
        'fields': 'items(volumeInfo/title,volumeInfo/authors,volumeInfo/publishedDate,volumeInfo/description,volumeInfo/industryIdentifiers,volumeInfo/pageCount,volumeInfo/categories,volumeInfo/averageRating,volumeInfo/ratingsCount,volumeInfo/language)'
    }

    async with session.get(base_url, params=params) as response:
        if response.status == 200:
            print('request done')
            data = await response.json()
            if 'items' in data and len(data['items']) > 0:
                result = data['items'][0]['volumeInfo']
                result['Title_org'] = book_name
                return result
        else:
            print(f"Error {response.status}: {await response.text()}")
            return None

async def get_book_info(book_name, author_name, api_key):
    async with aiohttp.ClientSession() as session:
        return await get_book_info_async(session, book_name, author_name, api_key)


# ########
# async def book_info_add(df, api_key):
#     async def get_book_info_wrapper(row):
#         book_name = row['Title']
#         print(book_name)
#         author_name = row['Author']
#         await asyncio.sleep(3)
#         return await get_book_info(book_name, author_name, api_key)

#     # Run the asynchronous code
#     tasks = [get_book_info_wrapper(row) for _, row in df.iterrows()]

#     # Run the asynchronous code
#     results = await asyncio.gather(*tasks) 

    # combined_book_info = pd.DataFrame()
########

async def book_info_add(df, api_key):
    async def get_book_info_wrapper(row):
        book_name = row['Title']
        print(book_name)
        author_name = row['Author']
        return await get_book_info(book_name, author_name, api_key)

    # run in batches to not exceed google api quota limit 
    batch_size = 50
    combined_book_info = pd.DataFrame()
    
    # split and run queries of df in batches 
    for start in range(0, len(df), batch_size):
        end = start + batch_size
        current_batch = df.iloc[start:end]

        # Run the asynchronous code
        tasks = [get_book_info_wrapper(row) for _, row in current_batch.iterrows()]

        # Run the asynchronous code
        results = await asyncio.gather(*tasks) 

        # Extract and process the results
        for book_info in results:
            if book_info:
                # Extract the actual results from the list
                authors = book_info.get('authors', [np.nan])
                publish_date = book_info.get('publishedDate', np.nan)
                description = book_info.get('description', np.nan)
                identifiers = book_info.get('industryIdentifiers', [])
                isbn = identifiers[0]['identifier'] if identifiers else np.nan
                page_count = book_info.get('pageCount', np.nan)
                categories = book_info.get('categories', [np.nan])
                average_rating = book_info.get('averageRating', np.nan)
                rating_count = book_info.get('ratingsCount', np.nan)
                language = book_info.get('language', np.nan)
                book_name = book_info.get('Title_org', np.nan)


                book_info_df = pd.DataFrame({
                    'Title': [book_info.get('title', np.nan)],
                    'Author(s)': [", ".join(map(str, authors))],
                    'Publish Date': [publish_date],
                    'Description': [description],
                    'ISBN': [isbn],
                    'Page Count': [page_count],
                    'Categories': [", ".join(map(str, categories))],
                    'Average Rating': [average_rating],
                    'Rating Count': [rating_count],
                    'Language': [language],
                    'Title_org' : book_name
                })
                combined_book_info = pd.concat([combined_book_info, book_info_df])

            # Introduce a delay of 1 minute between batches, except for the last iteration or if df size is less than batch size
        if start + batch_size < len(df):
            await asyncio.sleep(70)


##################
    # Reset the index of the combined DataFrame
    combined_book_info = combined_book_info.reset_index(drop=True)
    combined_book_info = combined_book_info.rename(columns=lambda x: x.replace(' ', '_'))

    return combined_book_info