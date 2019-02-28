import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from future.utils import iteritems
from flask import Flask, render_template, redirect, url_for, request
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


@app.route('/click', methods=['GET', 'POST'])
def received():
    if request.method == 'POST':
        review = request.form['review']
        value = format_review(review)
        print(review)
        
        if value == 0:
            return redirect('/unknown')
        elif value > 8:
            return redirect('/five')
        elif value > 0:
            return redirect('/four')
        elif value > -20:
            return redirect('/two')
        else:
            return redirect('/one')
    else:
        review = request.args.get('review')

    return redirect('/')
    
@app.route('/unknown')
def unknown():
    return render_template('template_unknown.html')

@app.route('/five')
def five():
    return render_template("template_five.html")

@app.route('/four')
def four():
    return render_template("template_four.html")

@app.route('/two')
def two():
    return render_template("template_two.html")

@app.route('/one')
def one():
    return render_template("template_one.html")
    

if __name__ == "__main__":
    app.run(debug=True)