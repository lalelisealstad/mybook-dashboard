def get_wikidata(url):
    """
    Function that uses webscrapping to get the tables in a wikipedia page into one pandas dataframe
    Params: url of wikipedia page
    
    """
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    import re

    # Send a GET request to the URL and retrieve the content
    response = requests.get(url)
    content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Find all the tables on the page
    tables = soup.find_all("table", class_="wikitable")

    # Specify the index of the table you want to extract data from
    # table_index = 1

    # # Select the specified table
    # table = tables[table_index]

    df = pd.DataFrame([])

    for table in tables: 
        # Create the first column Year. I do this in this way because the column has merged cells
        # Extract the table rows
        rows = []
        for row in table.find_all("tr"):
            rows.append(row)

        # Create an empty list to store the values of the first column
        first_column = []
        # Print the DataFrame
        # Iterate over the rows and extract the year value from the <a> tag
        for row in rows:
            cells = row.find_all(["th", "td"])
            if cells:
                # Check if the first cell has rowspan attribute
                if cells[0].has_attr("rowspan"):
                    # Get the year value from the <a> tag
                    year = cells[0].find("a").text.strip()
                    
                    # Get the rowspan value
                    rowspan = int(cells[0]["rowspan"])
                    
                    # Repeat the year value based on rowspan
                    first_column.extend([year] * rowspan)


        # Create empty lists to store the column values
        second_column = []
        third_column = []
        fourth_column = []

        # Extract the data from the second, third, and fourth columns
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 4:
                second_column.append(cells[0].text.strip())
                third_column.append(cells[1].text.strip())
                fourth_column.append(cells[2].text.strip())

        # Create a DataFrame from the column values
        data = {
            "Year" : first_column, 
            "Author": second_column,
            "Title": third_column,
            "Result": fourth_column
        }
        datadf = pd.DataFrame(data)
        df = pd.concat([datadf, df])

    # Print the DataFrame
    df.Year = df.Year.astype(int)

    # Some titles are returned with wikipedia reference or added characthers, example, title[2]. I adjust the titles to remove the square brackets and the content within. 
    # Function to remove square brackets and their contents using regex
    def remove_square_brackets(text):
        return re.sub(r'\[.*?\]', '', text)

    # Apply the function to the 'Title' column
    df['Title'] = df['Title'].apply(remove_square_brackets)
    return df



def get_book_info(book_name, author_name):

    """
    Function to get book details using Google API. 
    Params: book_name, author_name
    
    """
    import requests
    import pandas as pd
    import numpy as np

    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': f'intitle:{book_name}+inauthor:{author_name}',
        'maxResults': 1
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        book = data['items'][0]['volumeInfo']
    else:
        # Adjust the book name with the added string ': A novel'
        adjusted_book_name = f"{book_name}: A novel"
        params['q'] = f'intitle:{adjusted_book_name}'

        response = requests.get(base_url, params=params)
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            book = data['items'][0]['volumeInfo']
        else:
            # Reset the query to check for just the title
            params['q'] = f'intitle:{book_name}'
            
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                book = data['items'][0]['volumeInfo']
            else:
                book = {}

    # title = using the imput from the df to make sure the title return will match the df. 
    authors = book.get('authors', [np.nan])
    publish_date = book.get('publishedDate', np.nan)
    description = book.get('description', np.nan)
    identifiers = book.get('industryIdentifiers', [])
    isbn = identifiers[0]['identifier'] if identifiers else np.nan
    page_count = book.get('pageCount', np.nan)
    categories = book.get('categories', [np.nan])
    average_rating = book.get('averageRating', np.nan)
    rating_count = book.get('ratingsCount', np.nan)
    language = book.get('language', np.nan)

    book_info = pd.DataFrame({
        'Title': [book_name],
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

    return book_info


def book_info_add(df): 
    import pandas as pd 
    """
    Iterates over a dataframe with book title and author to collect book information from Google Books API 
    by applying the get_book_info funcation to all the rows of books in the dataframe.
    Returns the book information in a dataframe
    Params: a dataframe with the columns Author and Title. 
    """

    # Create an empty DataFrame to store the book information
    combined_book_info = pd.DataFrame()

    # Iterate over the rows of the dataset
    for _, row in df.iterrows():
        book_name = row['Title']
        author_name = row['Author']
        
        # Call the get_book_info function for each book
        book_info = get_book_info(book_name, author_name)
        
        # Concatenate the resulting DataFrame to the combined_book_info DataFrame
        combined_book_info = pd.concat([combined_book_info, book_info])

    # Reset the index of the combined DataFrame
    combined_book_info = combined_book_info.reset_index(drop=True)

    # Display the combined DataFrame
    return combined_book_info


def get_book_topics(title, author):
    import requests
    import pandas as pd
    base_url = 'http://openlibrary.org/search.json'
    params = {
        'title': title,
        'author': author,
        'limit': 1
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'docs' in data and len(data['docs']) > 0:
        book = data['docs'][0]
        topics = book.get('subject', [])
        return topics
    else:
        return []
