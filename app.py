import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from future.utils import iteritems
from flask import Flask, render_template, redirect
import pandas as pd

app = Flask(__name__)

wordnet_lemmatizer = WordNetLemmatizer()

df = pd.read_csv("Resources/weights_df")
list(df)
new_df = df.set_index('Unnamed: 0')

#Tokenization function
def format_review(review):
    
    #Set all words to lowercase
    words = review.lower()
    
    #"Tokenize" the words, splitting the string into separate words aka tokens
    tokens = nltk.tokenize.word_tokenize(words)
            
    tokens_lemmatized = []
    
    for t in tokens:
        tokens_lemmatized.append(wordnet_lemmatizer.lemmatize(t))
    
    #Reduce the tokens to numbers
    review_sum = 0
    for t in tokens_lemmatized:
        if t in new_df.index:
            number = new_df.loc[t].values[0]
            review_sum += number
    return review_sum


@app.route('/')
def home():
    return render_template("template.html")


@app.route('/click')
def received(review):
    return redirect('/')

    # value = format_review(review)
    # print(review_score)
        
    # if value == 0:
    #     return "I don't know these words, sorry"
    # elif value > 8:
    #     return 5
    # elif value > 0:
    #     return 4
    # elif value > -20:
    #     return 2
    # else:
    #     return 1
    
    
    
    
    
    
    
    
    


if __name__ == "__main__":
    app.run(debug=True)