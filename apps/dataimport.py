# Improt packages
import pandas as pd
import numpy as np

# Import functions from apps folder
from apps.collect_data import *



def dataprep(mybooksgr, mybooksgg):
    mybooksgr = mybooksgr.rename(columns=lambda x: x.replace(' ', '_'))

    # Merge dataframes 
    mybooks = pd.merge(mybooksgr,
                        mybooksgg,
                        on='Title', 
                        suffixes = ('_Goodreads', '_GoogleBooks'), 
                        how='left')
    
    # Page count category variable
    def categorize_pages(number_of_pages):
        if number_of_pages >= 100 and number_of_pages <= 249:
            return '100-249'
        elif number_of_pages >= 250 and number_of_pages <= 349:
            return '250-349'
        elif number_of_pages >= 350 and number_of_pages <= 449:
            return '350-449'
        elif number_of_pages >= 450 and number_of_pages <= 599:
            return '450-599'
        elif number_of_pages >= 600 and number_of_pages <= 749:
            return '600-749'
        elif number_of_pages >= 750 and number_of_pages <= 999:
            return '750-999'
        else:
            return '1000+'

    # Apply the categorize_pages function to create the 'Page_Cat' column
    mybooks['Page_Cat'] = mybooks['Number_of_Pages'].apply(categorize_pages)

    # Define the desired order of categories
    category_order = ['100-249', '250-349', '350-449', '450-599', '600-749', '750-999', '1000+']

    # Convert the 'Page_Cat' column to a categorical variable with the specified order
    mybooks['Page_Cat'] = pd.Categorical(mybooks['Page_Cat'], categories=category_order, ordered=True)
    
    # drop duplicates
    mybooks = mybooks.drop_duplicates(subset=['Title', 'Author'])

    # Create year and quarter read variable 
    #  Impute data_added where date_read  is na
    mybooks['Date_Read'] = np.where(mybooks['Date_Read'].isnull() & mybooks['Read_Count']==1, mybooks['Date_Added'], mybooks['Date_Read'])

    # Convert 'Date_Read' column to datetime type
    mybooks['Date_Read'] = pd.to_datetime(mybooks['Date_Read'], format='mixed')
    mybooks = mybooks.sort_values(by='Date_Read')

    # Extract year and quarter from 'Date_Read' column
    mybooks['Year'] = mybooks['Date_Read'].dt.year
    mybooks['Quarter'] = mybooks['Date_Read'].dt.quarter

    # Create a new column combining year and quarter
    mybooks['Year_Quarter'] = np.where(mybooks['Date_Read'].notnull(), mybooks['Year'].astype(str) + '-Q' + mybooks['Quarter'].astype(str), np.nan)
    # Replace '.0' in the Year_Quarter column with an empty string
    mybooks['Year_Quarter'] = mybooks['Year_Quarter'].fillna('').str.replace('.0', '')

    # Convert Year_Quarter to categorical variable
    mybooks['Year_Quarter'] = pd.Categorical(mybooks['Year_Quarter'], ordered=True)

    # filter na in publication year and make column publication year integer 
    mybooks['Original_Publication_Year'] = mybooks['Original_Publication_Year'].fillna( 0)
    mybooks['Original_Publication_Year'] = mybooks['Original_Publication_Year'].astype(int)

    mybooks = mybooks.replace('nan', np.nan)
    mybooks = mybooks.replace('NaN', np.nan)    

    return mybooks