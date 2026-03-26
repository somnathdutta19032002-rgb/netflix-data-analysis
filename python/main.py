import pandas as pd
import numpy as np
df = pd.read_csv(
    r"C:\Users\ACER\PycharmProjects\NETFLIXCONTENTSTRATEGYINTELLIGENCEDASHBOARD\data\netflix_titles.csv"
)
df=df.drop_duplicates()
df['date_added']=pd.to_datetime(df['date_added'],errors='coerce')
df=df.dropna(subset=['date_added'])
df['country']=df['country'].fillna("Unknown")
df['director']=df['director'].fillna("Unknown")
df['cast']=df['cast'].fillna("Unknown")
df['rating']=df['rating'].fillna("Not Rated")
df['country']=df['country'].str.strip()
df['listed_in']=df['listed_in'].str.strip()
df['type']=df['type'].str.strip()
df[['duration_value','duration_unit']]=df['duration'].str.split(' ',expand=True)
df['duration_value']=pd.to_numeric(df['duration_value'],errors='coerce')


#FEATUREENGINEERING
df['year_added']=df['date_added'].dt.year
current_year=pd.Timestamp.today().year
df['content_age']=current_year-df['release_year']
df['is_recent']=np.where(df['content_age']<=5,1,0)
df['decade']=(df['release_year']//10)


#genereCOUNTRYexplosion
df['listed_in']=df['listed_in'].str.split(', ')
df['genre_count']=df['listed_in'].apply(len)
df=df.explode('listed_in')
df['country']=df['country'].str.split(', ')
df=df.explode('country')

#strategyscore

df['strategy_score']=(
    df['is_recent']*0.4+(df['genre_count']/df['genre_count'].max())*0.3+
    (1/(df['content_age']+1))*0.3
)

df.to_csv("netflix_final_ready.csv",index=False)


