
import requests
import pandas as pd
import numpy as np
import aiohttp
import asyncio
import nest_asyncio
import time

async def get_book_info_async(session, book_name, author_name, api_key):
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': f'intitle:{book_name}+inauthor:{author_name}',
        'key': api_key,
        'maxResults': 1,
        'fields': 'items(volumeInfo/title,volumeInfo/authors,volumeInfo/publishedDate,volumeInfo/description,volumeInfo/industryIdentifiers,volumeInfo/pageCount,volumeInfo/categories,volumeInfo/averageRating,volumeInfo/ratingsCount,volumeInfo/language)'
    }

    async with session.get(base_url, params=params) as response:
        if response.status == 200:
            print('request one done')
            data = await response.json()
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]['volumeInfo']
        else:
            print(f"Error {response.status}: {await response.text()}")
            return None

async def get_book_info(book_name, author_name, api_key):
    async with aiohttp.ClientSession() as session:
        return await get_book_info_async(session, book_name, author_name, api_key)

async def book_info_add(df, api_key):
    async def get_book_info_wrapper(row):
        book_name = row['Title']
        print(book_name)
        author_name = row['Author']
        await asyncio.sleep(1)
        return await get_book_info(book_name, author_name, api_key)

    # Run the asynchronous code
    tasks = [get_book_info_wrapper(row) for _, row in df.iterrows()]

    # Run the asynchronous code
    results = await asyncio.gather(*tasks)  # Corrected placement of await

    combined_book_info = pd.DataFrame()

    # Extract the actual results from the list
    for book_info in results:
        if book_info:
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
                'Language': [language]
            })
            combined_book_info = pd.concat([combined_book_info, book_info_df])

    # Reset the index of the combined DataFrame
    combined_book_info = combined_book_info.reset_index(drop=True)
    combined_book_info = combined_book_info.rename(columns=lambda x: x.replace(' ', '_'))

    return combined_book_info