import nltk
# nltk.data.path.append('C:/Users/HP/AppData/Roaming/nltk_data')
from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Flask setup
app = Flask(__name__)

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Load data and train model
df = pd.read_csv('Restaurant_Reviews.tsv', delimiter='\t', quoting=3)
# Preprocess reviews
def text_preprocess(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text.lower())
    ps = PorterStemmer()
    tokens = [word for word in tokens if word not in string.punctuation]
    new_text = []
    all_stopwords = stopwords.words("english")
    all_stopwords.remove("not")
    for word in tokens:
        if word in all_stopwords:
            new_text.append('')
        else:
            new_text.append(word)
    stemmed_tokens = [ps.stem(word) for word in new_text]
    return " ".join(stemmed_tokens)

df["Processed Reviews"] = df["Review"].apply(text_preprocess)
# print(df)
#TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=1500)
X = tfidf.fit_transform(df['Processed Reviews']).toarray()
y = df['Liked']

# Train a model (MultinomialNB for simplicity here)
model = MultinomialNB(alpha=1)
model.fit(X, y)

# Save model and vectorizer for reuse
pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(tfidf, open('tfidf.pkl', 'wb'))

# Load model (optional if saving/loading later)
model = pickle.load(open('model.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    review = request.form['review']
    processed = text_preprocess(review)
    vect = tfidf.transform([processed]).toarray()
    prediction = model.predict(vect)[0]
    return render_template('index.html', review=review, prediction='Positive' if prediction == 1 else 'Negative')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    review = data.get('review', '')
    processed = text_preprocess(review)
    vect = tfidf.transform([processed]).toarray()
    prediction = model.predict(vect)[0]
    return jsonify({'prediction': 'Positive' if prediction == 1 else 'Negative'})

if __name__ == "__main__":
    app.run(debug=True)
