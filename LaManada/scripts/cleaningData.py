import pandas as pd
import re

#open the csv file 
df = pd.read_csv('tweets_lamanada.csv', sep=',')

#drop useless columns
df = df.drop(['count', 'retweets', 'likes'], axis= 1)

#drop empty tweets
df = df.dropna(subset=['text'])

#clean data
def clean_text(text):
    text = re.sub(r'@[\w]+', '', text)  #remove mentions 
    text = re.sub(r'http\S+', '', text)  #remove links
    text = re.sub(r'#\S+', '', text)  #remove hashtags
    #remove special caracters
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return text

df['cleaned_text'] = df['text'].apply(clean_text)

#convert dates to dateTime format 
df['created_at'] = pd.to_datetime(df['created_at'])

#save cleaned tweets
df.to_csv('tweets_nettoye.csv', index=False)






