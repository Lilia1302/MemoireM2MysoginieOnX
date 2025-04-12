import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

nltk.download('punkt')  # tokenisation
nltk.download('omw-1.4')  #lemmatisation
nltk.download('stopwords')  #stopwords
nltk.download('punkt_tab') 

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('spanish'))

#tokenization and lemmatization
def tokenize_and_lemmatize(text):
    #tokenisation
    tokens = word_tokenize(text, language='spanish')
    
    #remove stopwords
    tokens = [word.lower() for word in tokens if word not in string.punctuation and word.lower() not in stop_words]
    
    #lemmatisation
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    #join lemmatized tokens to create text
    return " ".join(lemmatized_tokens)

df_tweets = pd.read_csv('tweets_nettoye.csv')

#apply lemmatization
df_tweets['lemmatized_text'] = df_tweets['cleaned_text'].apply(tokenize_and_lemmatize)

print("\nExemple avant lemmatisation :")
print(df_tweets['cleaned_text'].iloc[0])

print("\nExemple après lemmatisation :")
print(df_tweets['lemmatized_text'].iloc[0])


df_tweets.to_csv('tweets_avec_lemmas.csv', index=False)
print("Fichier sauvegardé sous 'tweets_avec_lemmas.csv'")


