
import pandas as pd
from apps.async_googleapi import book_info_add 
import asyncio
from apps.api import api_key
async def get_ggl(books):
    global nmyreads 
    nmyreads = await book_info_add(books, api_key) 

def sync_function():
    mybooksgr = pd.read_csv("assets/goodreads_library_export.csv")
    mybooksgr = mybooksgr.rename(columns=lambda x: x.replace(' ', '_'))
    print('first books printed')
    
    
    print("Sync function started")
    asyncio.run(get_ggl(mybooksgr.sample(3)))
    print(nmyreads)
    print('hello', len(nmyreads))
    
    
    print("Sync function completed")

if __name__ == "__main__":
    sync_function()
    
