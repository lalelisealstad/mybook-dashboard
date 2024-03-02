def ml_genre(df): 
    import pandas as pd
    
    
    # function for text cleaning 
    import re
    def clean_text(text):
        # remove backslash-apostrophe 
        text = re.sub("\'", "", text) 
        # remove everything except alphabets 
        text = re.sub("[^a-zA-Z]"," ",text) 
        # remove whitespaces 
        text = ' '.join(text.split()) 
        # convert text to lowercase 
        text = text.lower() 
        
        return text

    # remove stopwords
    from apps.english_stopwords import stopwords
    stop_words = set(stopwords)

    # function to remove stopwords
    def remove_stopwords(text):
        no_stopword_text = [w for w in text.split() if not w in stop_words]
        return ' '.join(no_stopword_text)


    # load pre-trained vectoriser, multilabel Binarizer and the model 
    import pickle
    tfidf_vectorizer = pickle.load(open("assets/ml_model/tfidf_vectorizer.pickle", "rb"))
    loaded_model = pickle.load(open("assets/ml_model/ML2", "rb"))
    multilabel_binarizer = pickle.load(open("assets/ml_model/multilabel_binarizer.pickle", "rb"))
    
    
    # predict genre and add it to a new column "genres"

    # main ml program, cleaning and prediction
    from ast import literal_eval
    from langdetect import detect
    
    def main(q):
        if pd.isnull(q):  # Check if description is NaN
            return None
        elif detect(q) != 'en': 
            return None
        else:
            q = clean_text(q)
            q = remove_stopwords(q)
            q_vec = tfidf_vectorizer.transform([q])
            q_pred = loaded_model.predict(q_vec)
            return multilabel_binarizer.inverse_transform(q_pred)
    
    df['genres'] = df['Description'].apply(main)

    def makelist(list1):
        return str(list1).replace('(','').replace(')','').replace(',]',']')

    df['genres'] = df['genres'].apply(makelist)
    return df 

# manipulate df with genre 
import pandas as pd
import numpy as np 

def make_genre_tbl(df_genres):
    import numpy as np 
    tbl_genre = (
        pd.DataFrame(
            np.round(
                (
                df_genres.query('Read_Count > 0 & My_Rating > 0')
                .groupby('genres').aggregate({'genres':'count', 'My_Rating':'mean'})
                )
            ,2)
        # only count above 5
        ).query('genres > genres.quantile(0.07)')
    )
    return tbl_genre
