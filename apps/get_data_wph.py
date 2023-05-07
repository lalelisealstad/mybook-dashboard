import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_Women's_Prize_for_Fiction_winners"

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

df.to_parquet('assets/WPH.parquet')

