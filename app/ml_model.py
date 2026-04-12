# ml_model.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training data (you can expand later)
texts = [
    "plastic bottle", "polybag", "plastic wrapper",
    "glass bottle", "window glass",
    "food waste", "vegetable peel", "leftover food",
    "paper box", "newspaper", "cardboard",
    "metal can", "aluminum foil"
]

labels = [
    "Plastic", "Plastic", "Plastic",
    "Glass", "Glass",
    "Organic", "Organic", "Organic",
    "Paper", "Paper", "Paper",
    "Metal", "Metal"
]

# Vectorizer + Model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)


# Prediction function
def predict_waste(text):
    X_test = vectorizer.transform([text])
    prediction = model.predict(X_test)[0]
    confidence = max(model.predict_proba(X_test)[0]) * 100

    # Extra info mapping
    info = {
        "Plastic": (True, "Recycle at plastic facility"),
        "Glass": (True, "Reuse or recycle"),
        "Organic": (False, "Compost"),
        "Paper": (True, "Recycle paper"),
        "Metal": (True, "Scrap recycling")
    }

    recyclable, disposal = info.get(prediction, (False, "General disposal"))

    return {
        "waste_type": prediction,
        "recyclable": recyclable,
        "disposal": disposal,
        "confidence": round(confidence, 2)
    }