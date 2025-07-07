import joblib
import pandas as pd
from goal_classifier import classify_goal_description


# Load model and encoders
model = joblib.load("xgb_investment_model.pkl")
encoders = joblib.load("xgb_label_encoders.pkl")

risk_mapping = {"Low": 0, "Medium": 1, "High": 2}
goal_mapping = {
    "Retirement": 0,
    "Buy a House": 1,
    "Child Education": 2,
    "Emergency Fund": 3,
    "Tax Saving": 4,
    "Car Purchase": 5,
    "Travel Abroad": 6
}

def predict_instrument(user_input):
    # Encode input manually
    risk_encoded = risk_mapping[user_input["risk_profile"]]
    goal_encoded = classify_goal_description(user_input["goal"])


    input_df = pd.DataFrame([{
        "age": user_input["age"],
        "salary": user_input["salary"],
        "savings": user_input["savings"],
        "risk_profile": risk_encoded,
        "goal": goal_encoded,
        "goal_amount": user_input["goal_amount"],
        "years_to_goal": user_input["years_to_goal"]
    }])

    # Predict with confidence
    pred = model.predict(input_df)
    prob = model.predict_proba(input_df)

    predicted_label = encoders['selected_instrument'].inverse_transform(pred)[0]
    confidence = round(prob[0][pred[0]] * 100, 1)

    return predicted_label, confidence

