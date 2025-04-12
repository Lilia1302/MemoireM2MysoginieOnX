import pandas as pd
import re

#open the csv file 
df = pd.read_csv('tweets_processed.csv', sep=',')

#drop useless columns
df = df.drop(['link', 'is-retweet', 'is-pinned', 'external-link','replying-to','user_avatar','stats_comments','stats_retweets','stats_quotes','stats_likes','quoted-post_link','quoted-post_text','quoted-post_user_name','quoted-post_user_username','quoted-post_user_profile_id','quoted-post_user_avatar','quoted-post_date','quoted-post_pictures','quoted-post_videos','quoted-post_gifs'], axis= 1)

#drop empty tweets
df = df.dropna(subset=['text'])

#clean data
def clean_text(text):
    text = re.sub(r'@[\w]+', '', text)  #remove mentions 
    text = re.sub(r'http\S+', '', text)  #remove links
    text = re.sub(r'#\S+', '', text)  #remove hashtags
    #remove special caracters
    text = re.sub(r'[^A-Za-z0-9À-ÿ\s]', '', text)
    return text

df['cleaned_text'] = df['text'].apply(clean_text)

#save cleaned tweets
df.to_csv('tweets_nettoye.csv', index=False)
