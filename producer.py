import pandas as pd
import json
import time
from kafka import KafkaProducer

df = pd.read_csv("C:/Users/Lenovo/MoneticFlow/paysim_features.csv")

# Limiter à 10 000 pour le test
df = df.head(10000)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print(f"Dataset chargé : {len(df)} transactions")
print("Envoi des transactions vers Kafka...")

for i, row in df.iterrows():
    message = row.to_dict()
    producer.send('transactions', value=message)
    
    if i % 1000 == 0:
        print(f"Envoyé : {i} transactions")
    
    time.sleep(0.001)  # 1000 transactions/seconde

producer.flush()
print("Terminé.")