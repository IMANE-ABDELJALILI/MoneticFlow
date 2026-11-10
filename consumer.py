import warnings
warnings.filterwarnings("ignore")

import json
import joblib
import numpy as np
import pandas as pd
from kafka import KafkaConsumer
from datetime import datetime

# Charger le modèle
model = joblib.load("C:/Users/Lenovo/MoneticFlow/random_forest_fraud.pkl")

feature_cols = ['step', 'type_encoded', 'amount',
                'oldbalanceOrg', 'newbalanceOrig',
                'oldbalanceDest', 'newbalanceDest',
                'balance_error_orig', 'balance_error_dest',
                'orig_account_emptied', 'dest_was_empty',
                'amount_to_balance_ratio']

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='fraud-detector-v3'
)

output_file = "C:/Users/Lenovo/MoneticFlow/resultats_fraudes.csv"
results = []

print("Consumer démarré — en attente de transactions...")

fraud_count = 0
total_count = 0

for message in consumer:
    transaction = message.value
    total_count += 1

    features = pd.DataFrame([transaction])[feature_cols]
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0][1]

    results.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'amount': transaction['amount'],
        'type_encoded': transaction['type_encoded'],
        'prediction': prediction,
        'fraud_score': round(proba, 4),
        'is_fraud': int(prediction == 1)
    })

    if prediction == 1:
        fraud_count += 1
        print(f"🚨 FRAUDE | montant={transaction['amount']:.2f} | score={proba:.4f}")

    if total_count % 1000 == 0:
        df_results = pd.DataFrame(results)
        df_results.to_csv(output_file, index=False)
        print(f"✅ Traité : {total_count} | Fraudes : {fraud_count} | Sauvegardé")

    if total_count >= 10000:
        df_results = pd.DataFrame(results)
        df_results.to_csv(output_file, index=False)
        print(f"\n✅ Terminé : {total_count} transactions | {fraud_count} fraudes")
        print(f"Résultats : {output_file}")
        break