
# Import libraries 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import numpy as np
import re

# topics viz tree map

def tree_topics(topics_dict): 
    """
    Creates a tree map visualization of book topics by count
    param: dictionary containing title of the book as key and the value is one list containing the book's topics
    """
    word_counts_dict = Counter()

    # Count the occurrences of each word in the values of the original dictionary
    for values in topics_dict.values():
        for value in values:
            for word in value.replace(', ', ',').split(','):
                word_counts_dict[word.lower()] += 1

    df_word_counts = pd.DataFrame(list(word_counts_dict.items()), columns=['Word', 'Count'])
    df_word_counts = df_word_counts.sort_values(by='Count', ascending=False).reset_index().head(45)

    fig = px.treemap(
        df_word_counts,
        path=['Word'],
        values='Count',
        custom_data=['Count'] )

    fig.update_layout(
        title={
            'text': 'Most common book topics',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=22
            )
        },
        uniformtext=dict(minsize=16),  # Increase the minimum text size to 70
        font=dict(
            size=16  # Adjust the font size for the entire figure
        )
    )
    
    
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{customdata[0]}'
    )
    # Show the plot
    return fig


# Publication year and rating 
def viz_pub_year(df):

    # Group the DataFrame by year and calculate the average rating and count of books
    df = df.query('Original_Publication_Year != 0')
    year_data = df.groupby('Original_Publication_Year',  observed=True).agg({'My_Rating': 'mean', 'Title': 'count'}).reset_index()
    
    # Extract the year labels, average ratings, and book counts
    labels = year_data['Original_Publication_Year']
    ratings = year_data['My_Rating']
    book_counts = year_data['Title']
    
    hover_text = []
    for year in labels:
        books = df[df['Original_Publication_Year'] == year]
        book_text = ""
        for i, (_, book) in enumerate(books.iterrows()):
            if i >= 19:
                book_text += "..."
                break
            book_text += f"{book['Title']} - Rating: {book['My_Rating']}<br>"
        hover_text.append(f"<span style='font-size: 16px;'>{year}</span><br>" + book_text)

    
    # Scale the bubble sizes based on the logarithm of the count of books
    sizes = np.log(book_counts)  # Logarithmic scaling
    
    # Adjust the scaling factor to increase the size difference
    scaling_factor = 1.5  # Adjust the scaling factor as needed
    sizes = sizes * scaling_factor
    
    # Set a minimum size for bubbles with a count of 1
    min_size = 1  # Adjust the minimum size as needed
    sizes = np.where(book_counts < 2, min_size, sizes)
    
    # Create the scatter plot
    fig = go.Figure(data=go.Scatter(
        x=labels,
        y=ratings,
        mode='markers',
        text=hover_text,
        hoverinfo='text',
        marker=dict(
            size=sizes,
            sizemode='diameter',
            sizeref=sizes.max() / 50,  # Adjust the size scaling factor as needed
            color=ratings,
            colorscale='Purp',  # Choose a desired color scale
            showscale=True
        )
    ))
    
    # Customize the plot layout
    fig.update_layout(
        title='My Rating vs. Publication Year',
        xaxis=dict(title='Publication Years'),
        yaxis=dict(title='My Rating'),
        showlegend=False,
        template = "plotly_white"
    )
    return fig


# Publication year vs rating 
def viz_year_read(df):
    
    df = df.dropna(subset=['Year_Quarter'])
    
    # Count the number of books read in each year and quarter
    year_quarter_counts = df.groupby('Year_Quarter',  observed=True).size().reset_index(name='Books Read')
    
    # Create the line chart
    fig = px.line(year_quarter_counts, x='Year_Quarter', y='Books Read', markers=True, template = "plotly_white")
    fig['data'][0]['line']['color']='#A777F1'
    # Customize the plot layout
    fig.update_layout(
        title='Number of books read - Timeline',
        xaxis=dict(title='Year and Quarter'),
        yaxis=dict(title='Number of Books Read'),
        showlegend=False
    )
    return fig

### Page count 

def visualize_categories(myreads, column, title, xtitle):
    # Group the DataFrame by page category and count the number of books in each category
    category_counts = myreads[column].value_counts().sort_index()

    # Assign a unique color to each category
    colors = ['rgb(251,180,174)', 'rgb(179,205,227)', 'rgb(204,235,197)', 'rgb(222,203,228)', 'rgb(254,217,166)', 'rgb(250,231,175)','rgb(251,180,174)' ]

    # Create the bar chart
    fig = go.Figure(data=go.Bar(
        x=category_counts.index,
        y=category_counts.values,
        marker=dict(color=colors),
    ))

    # Set the chart title and axis labels
    fig.update_layout(
        title=title,
        xaxis=dict(title=xtitle),
        yaxis=dict(title='Number of Books'),
        template = "plotly_white"
    )
    
    return fig


# pie chart, top 5 categories and languages

def viz_top_values(column, top_n=5):
    # Drop NaN values from the column
    column = column.dropna()
    value_col = column.value_counts().reset_index()

    if len(value_col) > top_n: 
        remaining_count =value_col['count'].iloc[top_n:].sum()
        other = pd.DataFrame([['Other', remaining_count]], columns=[value_col.columns[0], 'count'])
        val_df =  pd.DataFrame(pd.concat([value_col.head(top_n), other]))
    else:
        val_df = pd.DataFrame(value_col)


    labels = val_df.iloc[:, 0]
    values = val_df['count']

    # Define the color theme 
    colors = ['rgba(230,230,250, 0.8)', 'rgb(179,205,227)', 'rgb(204,235,197)', 'rgb(222,203,228)', 'rgb(254,217,166)', 'rgb(250,231,175)','rgb(251,180,174)', 'rgb(251,180,174)','#9DC8C8', '#84B1ED' ]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Set the colors using the color theme
    fig.update_traces(marker=dict(colors=colors))

    fig.update_layout(title=f'Top {top_n} {column.name}')

    return fig


#### highest and lowest rated books

def book_ratings_top(data, title_txt):
    # Define custom colors
    my_rating_color = 'rgb(180,151,231)'
    google_books_color = '#34A853'
    goodreads_color = '#e9e5cd'

    # Filter the data where My_Rating > 0 since this would include non-rated books
    filtered_data = data[data['My_Rating'] > 0]

    # Sort the filtered data by your own rating in ascending order for bottom-rated books
    filtered_data = filtered_data.sort_values(['My_Rating', 'Date_Read'], ascending=True)

    # Select the top 10 books based on your own rating
    top_books = filtered_data.tail(15)

    # Create the figure object
    fig = px.scatter(template = "plotly_white")

    # Add trace for Average_Rating_GoogleBooks as dots with a different color and shape
    fig.add_trace(go.Scatter(
        x=top_books['Average_Rating_GoogleBooks'],
        y=top_books['Title'],
        mode='markers',
        name=f"Average Rating Google Books",
        marker=dict(color=google_books_color, symbol='square', size=15),
    ))

    # Add trace for Average_Rating_Goodreads as dots with a different color and shape
    fig.add_trace(go.Scatter(
        x=top_books['Average_Rating_Goodreads'],
        y=top_books['Title'],
        mode='markers',
        name='Average Rating Goodreads',
        marker=dict(color=goodreads_color, symbol='diamond', size=15),
    ))

    # Add trace for My Rating as dots
    fig.add_trace(go.Scatter(
        x=top_books['My_Rating'],
        y=top_books['Title'],
        mode='markers',
        name='My Rating',
        marker=dict(color=my_rating_color, symbol='circle', size=15),
    ))

    # Update the layout
    fig.update_layout(
        title= f'{title_txt}<br><span style="font-size: 11px;">*Showing only 15 latest read books</span>',
        # font=dict(size=12),
        yaxis=dict(title='Title', side='top', showticklabels=True),
        xaxis=dict(
            title='Rating',
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            range=[0.5, 5.5],  # Set the X-axis range from 0 to 5, 
            showgrid=True),
        legend=dict(
            title='Rating',  # Set legend title
            orientation='h',  # Adjust x position of the legend
            y=-0.15  # Adjust y position of the legend
        )
        )
    return fig


def book_ratings_bottom(data, title_txt):
    # Define custom colors
    my_rating_color = 'rgb(180,151,231)'
    google_books_color = '#34A853'
    goodreads_color = '#e9e5cd'

    # Filter the data where My_Rating > 0 since this would include non-rated books
    filtered_data = data[data['My_Rating'] > 0]

    # Sort the filtered data by your own rating in ascending order for bottom-rated books
    filtered_data = filtered_data.sort_values(['My_Rating', 'Date_Read'], ascending=True)

    # Select the top 10 books based on your own rating
    top_books = filtered_data.head(15)

    # Create the figure object
    fig = px.scatter(template = "plotly_white")

    # Add trace for My Rating as dots
    fig.add_trace(go.Scatter(
        x=top_books['My_Rating'],
        y=top_books['Title'],
        mode='markers',
        name='My Rating',
        marker=dict(color=my_rating_color, symbol='circle', size=15),
    ))

    # Add trace for Average_Rating_GoogleBooks as dots with a different color and shape
    fig.add_trace(go.Scatter(
        x=top_books['Average_Rating_GoogleBooks'],
        y=top_books['Title'],
        mode='markers',
        name=f"Average Rating Google Books",
        marker=dict(color=google_books_color, symbol='square', size=15),
    ))

    # Add trace for Average_Rating_Goodreads as dots with a different color and shape
    fig.add_trace(go.Scatter(
        x=top_books['Average_Rating_Goodreads'],
        y=top_books['Title'],
        mode='markers',
        name='Average Rating Goodreads',
        marker=dict(color=goodreads_color, symbol='diamond', size=15),
    ))

    # Update the layout
    fig.update_layout(
        title= f'{title_txt}<br><span style="font-size: 11px;">*Showing only 15 latest read books</span>',
        # font=dict(size=12),
        yaxis=dict(title='Title', side='top', showticklabels=True),
        xaxis=dict(
            title='Rating',
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            range=[0.5, 5.5],  # Set the X-axis range from 0 to 5, 
            showgrid=True),
        legend=dict(
            title='Rating',  # Set legend title
            orientation='h',  # Adjust x position of the legend
            y=-0.15  # Adjust y position of the legend
        )
        )
    return fig




# My top authors 

def author_count_fig(myreads):
        
        tbl_authors = myreads.Author.value_counts().head(20).reset_index().sort_values(by=['count'], ascending = True)

        fig_author = px.bar(tbl_authors, x = 'count', y = 'Author', orientation = 'h', labels = {'count' : 'Number of books read by author'})

        fig_author.update_layout(title = 'My most read authors',
                template='plotly_white',
                plot_bgcolor='white',
                paper_bgcolor='white',
                height = 600)

        fig_author.update_traces(marker_color='#C1E1C1', width=0.4)
        return fig_author



def author_rating_fig(myreads): 
    
    ls_authors = myreads.Author.value_counts().head(20).reset_index().sort_values(by=['count'], ascending = True)['Author']

    myreads['My_Rating'] = myreads['My_Rating'].replace(0, np.nan)

    # Calculate the mean 'My_Rating' grouped by 'Author'
    myreads['mean_rating_by_author'] = myreads.groupby('Author',  observed=True)['My_Rating'].transform('mean').copy()

    myreads['My_Rating'] = np.where((myreads['My_Rating'] == np.nan) | myreads['My_Rating'].isnull(), myreads['mean_rating_by_author'], myreads['My_Rating'])


    tbl_rating_authors = (
        myreads.query('Author in @ls_authors')
        .groupby('Author')['My_Rating'].mean().reset_index()
        ).set_index('Author').reindex(index = ls_authors).reset_index()


    fig_author_rating = px.bar(tbl_rating_authors, x = 'My_Rating', y = 'Author', orientation = 'h', labels = {'My_Rating' : 'My average rating of author'})

    fig_author_rating.update_layout(title = 'My average rating of my most read authors',
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height = 600)

    fig_author_rating.update_traces(marker_color='#FFD580', width=0.4)
    
    return fig_author_rating



# Three viz of count of words in description

def desc_tree(Description):
    from collections import Counter
    stopwords_dict = {'like', 'author', 'S', 'will','new','york','time','book','novel', 'read', 'day', 'make','year', 'one', 'times', 'times, of', 's', 'award','author','new','york','selling','story','t','1','og', 'call', 'upon', 'still', 'nevertheless', 'down', 'every', 'forty', '‘re', 'always', 'whole', 'side', "n't", 'now', 'however', 'an', 'show', 'least', 'give', 'below', 'did', 'sometimes', 'which', "'s", 'nowhere', 'per', 'hereupon', 'yours', 'she', 'moreover', 'eight', 'somewhere', 'within', 'whereby', 'few', 'has', 'so', 'have', 'for', 'noone', 'top', 'were', 'those', 'thence', 'eleven', 'after', 'no', '’ll', 'others', 'ourselves', 'themselves', 'though', 'that', 'nor', 'just', '’s', 'before', 'had', 'toward', 'another', 'should', 'herself', 'and', 'these', 'such', 'elsewhere', 'further', 'next', 'indeed', 'bottom', 'anyone', 'his', 'each', 'then', 'both', 'became', 'third', 'whom', '‘ve', 'mine', 'take', 'many', 'anywhere', 'to', 'well', 'thereafter', 'besides', 'almost', 'front', 'fifteen', 'towards', 'none', 'be', 'herein', 'two', 'using', 'whatever', 'please', 'perhaps', 'full', 'ca', 'we', 'latterly', 'here', 'therefore', 'us', 'how', 'was', 'made', 'the', 'or', 'may', '’re', 'namely', "'ve", 'anyway', 'amongst', 'used', 'ever', 'of', 'there', 'than', 'why', 'really', 'whither', 'in', 'only', 'wherein', 'last', 'under', 'own', 'therein', 'go', 'seems', '‘m', 'wherever', 'either', 'someone', 'up', 'doing', 'on', 'rather', 'ours', 'again', 'same', 'over', '‘s', 'latter', 'during', 'done', "'re", 'put', "'m", 'much', 'neither', 'among', 'seemed', 'into', 'once', 'my', 'otherwise', 'part', 'everywhere', 'never', 'myself', 'must', 'will', 'am', 'can', 'else', 'although', 'as', 'beyond', 'are', 'too', 'becomes', 'does', 'a', 'everyone', 'but', 'some', 'regarding', '‘ll', 'against', 'throughout', 'yourselves', 'him', "'d", 'it', 'himself', 'whether', 'move', '’m', 'hereafter', 're', 'while', 'whoever', 'your', 'first', 'amount', 'twelve', 'serious', 'other', 'any', 'off', 'seeming', 'four', 'itself', 'nothing', 'beforehand', 'make', 'out', 'very', 'already', 'various', 'until', 'hers', 'they', 'not', 'them', 'where', 'would', 'since', 'everything', 'at', 'together', 'yet', 'more', 'six', 'back', 'with', 'thereupon', 'becoming', 'around', 'due', 'keep', 'somehow', 'n‘t', 'across', 'all', 'when', 'i', 'empty', 'nine', 'five', 'get', 'see', 'been', 'name', 'between', 'hence', 'ten', 'several', 'from', 'whereupon', 'through', 'hereby', "'ll", 'alone', 'something', 'formerly', 'without', 'above', 'onto', 'except', 'enough', 'become', 'behind', '’d', 'its', 'most', 'n’t', 'might', 'whereas', 'anything', 'if', 'her', 'via', 'fifty', 'is', 'thereby', 'twenty', 'often', 'whereafter', 'their', 'also', 'anyhow', 'cannot', 'our', 'could', 'because', 'who', 'beside', 'by', 'whence', 'being', 'meanwhile', 'this', 'afterwards', 'whenever', 'mostly', 'what', 'one', 'nobody', 'seem', 'less', 'do', '‘d', 'say', 'thus', 'unless', 'along', 'yourself', 'former', 'thru', 'he', 'hundred', 'three', 'sixty', 'me', 'sometime', 'whose', 'you', 'quite', '’ve', 'about', 'even'}
        
    descriptions_all = ' '.join(Description.dropna()).lower()

    descriptions_all = re.findall(r'\b\w+\b', descriptions_all.lower())

    # Remove stop words from the list of words
    filtered_words = [word for word in descriptions_all if word not in stopwords_dict]

    word_counts = Counter(filtered_words)

    # Create a DataFrame from the word counts
    word_counts_df = pd.DataFrame(word_counts.items(), columns=['Word', 'Count'])
    # Create a tree map using Plotly Express
    fig = px.treemap(word_counts_df.sort_values(by='Count', ascending=False).head(55), path=['Word'], values='Count', custom_data=['Count'] )

    fig.update_layout(
        title={
            'text': 'Most common words found in book descriptions',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            # 'font': dict(
            #     size=22
            # )
        },
        # uniformtext=dict(minsize=16),  # Increase the minimum text size to 70
        # font=dict(
        #     size=16  # Adjust the font size for the entire figure
        # )
    )

    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{customdata[0]}'
    )

    return fig


import plotly.express as px
import plotly.graph_objects as go

def scatter_popularity(df):
    # Create scatter plot

    df['My_Rating'] = df['My_Rating'].replace(0, np.nan)
    df = df.dropna(subset=['Rating_Count', 'Average_Rating_Goodreads'])

    melted_df = pd.melt(df[['Rating_Count', 'Average_Rating_Goodreads', 'My_Rating']], id_vars=['Rating_Count'], value_vars=['Average_Rating_Goodreads', 'My_Rating'],
                        var_name='Rating_Type', value_name='Rating')

    color_scale = px.colors.qualitative.Set2[2:8]  # 

    fig = px.scatter(
        melted_df, x='Rating_Count', y='Rating',color='Rating_Type', trendline="ols", title="Does popularity correlate with rating?<br>",
        template="plotly_white",  
        color_discrete_sequence=color_scale, 
        labels={"Rating_Type": "Rating", 'Average_Rating_Goodreads': "Average Rating on Goodreads"},
        category_orders={"Rating_Type": ["Average_Rating_Goodreads", "My_Rating"]}
    )
    # Customize the legend
    fig.update_layout(
        legend=dict(
            title='Rating Type:', 
            orientation='h',  
            x=0.5,  
            y=1.2,  
        ),
        
        xaxis=dict(
            title='Number of times the book has been rated in Google Books',  
        ),
        
        yaxis=dict(
            title='Rating', 
        )
    )
    return fig

def lolli_fig(tbl_genre):

    fig = px.scatter(tbl_genre, 
        y=tbl_genre.index.tolist(), 
        x="My_Rating",
        orientation='h',
        size="genres", 
        color=tbl_genre.index.tolist(),
        size_max=80)
    fig.update_traces(hovertemplate='Genre: %{x} <br>My average rating of books with genre: %{y}<br>Number of read books with genre: %{marker.size:}') #
    
    fig2 = px.bar(y=tbl_genre.index, x=tbl_genre['My_Rating'], orientation='h',)
    
    fig2.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(158,202,225)', marker_line_width=1.5, opacity=0.9, width=0.1)                  

    fig3 = go.Figure(data=fig.data + fig2.data)
    
    fig3.update_layout(
        title={
            'text': 'Rating and number of books read in genre',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_range=[(tbl_genre.My_Rating.min()-0.5),(tbl_genre.My_Rating.max()+0.1)],
        template="plotly_white",  
        showlegend = False, 
        height = 800,
        margin=dict(l=10, r=10, t=100, b=30),
        )
    
    fig3.add_annotation(
        x=0.45,
        y=1.01,
        xref='paper',
        yref='paper',
        text='<span style="font-size: 7px;">The size of the bubble represent the number of books read within genre. <br> The position of the bubble along the y-axis represent how well books within the genre have been rated.</span>',
        showarrow=False,
    )

    return fig3
 
 
# Spider figure - genre rating     
    
import plotly.express as px

def spider_fig(tbl_genre):
    spider_fig = px.line_polar(tbl_genre, r=tbl_genre.My_Rating, theta=tbl_genre.index, line_close=True, range_r=[1, tbl_genre.My_Rating.max()+0.2]).update_traces(fill='tonext', fillcolor='rgba(167, 119, 241, 0.5)')
    spider_fig.update_layout(template='plotly_white', title = 'My average rating of books with genre', height = 600)
    return spider_fig
    
    
    
# Genre - year quarter timeline

import plotly.express as px

def stack_fig(allgenredf, tbl_genre):
    
    tbl_percent = (
        pd.DataFrame(
            allgenredf.query('Read_Count > 0 & genres in @tbl_genre.index.tolist()')
            .groupby('Year_Quarter',observed=True)['genres'].value_counts(normalize = True)
            )
        .reset_index()
        .query('Year_Quarter != "" and proportion > 0.01')
    )
    
    fig = px.area(tbl_percent, x='Year_Quarter',y='proportion', color='genres', line_group='genres',
                title='Genre read - Timeline<span style="font-size: 7px;"><br>Proportion of books in genre read that year-quarter. A book can have multiple genres.</span>')
        
    fig.update_layout( 
        xaxis_title='Year quarter',
        yaxis_title='Proportion of books read in quarter with genre',
        legend_title="Genre",
        template="plotly_white"
        , height = 600)

    return fig 