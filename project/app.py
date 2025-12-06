from flask import Flask, request, render_template_string
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# Load NLTK items
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# ---- Load your saved models ----
vectorizer = joblib.load("tfidf.joblib")
model = joblib.load("logreg_tfidf.joblib")

# ---- Text Cleaning Function ----
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return " ".join(tokens)

# ---- Flask Web App ----
app = Flask(__name__)

html = """
<!doctype html>
<html>
<head>
<title>AI Personality Predictor</title>
</head>
<body style="max-width:700px;margin:auto;font-family:Arial">
<h1>AI Personality Predictor</h1>
<p>Enter text below to predict Introvert / Extrovert:</p>

<form method="POST">
<textarea name="text" rows="8" style="width:100%"></textarea><br><br>
<button type="submit">Predict</button>
</form>

{% if result %}
    <h2>Prediction: {{ result }}</h2>
    <h3>Confidence: {{ confidence }}%</h3>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None

    if request.method == "POST":
        text = request.form["text"]
        cleaned = clean_text(text)

        vector = vectorizer.transform([cleaned])
        pred = model.predict(vector)[0]
        prob = model.predict_proba(vector).max() * 100

        result = "Introvert" if pred == 1 else "Extrovert"
        confidence = round(prob, 2)

    return render_template_string(html, result=result, confidence=confidence)

if __name__ == "__main__":
    app.run(debug=True)
