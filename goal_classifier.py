import joblib

# Load the model and vectorizer
model = joblib.load("goal_classifier.pkl")
vectorizer = joblib.load("goal_vectorizer.pkl")

# Optional: Label name map
goal_categories = {
    0: "Retirement",
    1: "Buy a House",
    2: "Child Education",
    3: "Emergency Fund",
    4: "Tax Saving",
    5: "Car Purchase",
    6: "Travel Abroad"
}

def classify_goal_description(description: str) -> int:
    vec = vectorizer.transform([description])
    label = model.predict(vec)[0]
    return label
