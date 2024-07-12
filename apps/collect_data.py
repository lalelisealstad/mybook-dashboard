import requests
import pandas as pd
import re


## BOOK TOPICS FROM OPEN LIBRARY API
def get_book_topics(df):
    """
    Collects topics of books using Open Library API.
    The output is a dictionary with title as the keys and the list of topics as the values.
    Params: df (pandas DataFrame) - DataFrame containing 'Title' and 'Author' columns.
    Returns: topics_dict (dict) - Dictionary with book titles as keys and corresponding topics as values.
    """
    import requests

    def get_book_topics(title, author):
        base_url = 'http://openlibrary.org/search.json'
        params = {
            'title': title,
            'author': author,
            'limit': 1
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for non-successful status codes
            data = response.json()

            if 'docs' in data and len(data['docs']) > 0:
                book = data['docs'][0]
                topics = book.get('subject', [])
                return topics
            else:
                return []
        except Exception as e:
            print(f"Error occurred for title: {title}, author: {author}")
            return []

    topics_dict = {}
    for _, row in df.iterrows():
        title = row['Title']
        author = row['Author']
        topics = get_book_topics(title, author)
        if topics:
            topics_dict[row['Title']] = topics

    return topics_dict
