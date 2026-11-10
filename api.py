import warnings
warnings.filterwarnings("ignore")

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Charger le modèle
model = joblib.load("C:/Users/Lenovo/MoneticFlow/random_forest_fraud.pkl")

app = FastAPI(title="MoneticFlow — API Détection de Fraude")

# Schéma de la transaction
class Transaction(BaseModel):
    step: int
    type_encoded: int
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float
    balance_error_orig: float
    balance_error_dest: float
    orig_account_emptied: int
    dest_was_empty: int
    amount_to_balance_ratio: float

@app.get("/")
def root():
    return {"message": "MoneticFlow API — Détection de fraude monétique"}

@app.post("/predict")
def predict(transaction: Transaction):
    data = pd.DataFrame([transaction.dict()])
    prediction = model.predict(data)[0]
    proba = model.predict_proba(data)[0][1]
    
    return {
        "prediction": int(prediction),
        "label": "FRAUDE" if prediction == 1 else "NORMAL",
        "fraud_score": round(float(proba), 4)
    }

@app.get("/stats")
def stats():
    import json
    results = pd.read_csv("C:/Users/Lenovo/MoneticFlow/resultats_fraudes.csv")
    return {
        "total_transactions": len(results),
        "total_fraudes": int(results["is_fraud"].sum()),
        "taux_fraude": round(float(results["is_fraud"].mean() * 100), 2)
    }