\# MoneticFlow — Détection de fraude monétique en temps réel



Plateforme Big Data pour l'analyse et le monitoring des autorisations de paiement électronique.



\## Architecture



CSV (PaySim) → Producer Kafka → Topic “transactions” → Consumer → Modèle RF → Résultats

↓

API FastAPI





\## Stack technique



\- \*\*Apache Kafka\*\* — ingestion des flux de transactions

\- \*\*Python\*\* — producer, consumer, modélisation

\- \*\*Scikit-learn\*\* — modèle Random Forest

\- \*\*FastAPI\*\* — API de scoring temps réel

\- \*\*Pandas\*\* — feature engineering



\## Dataset



PaySim — simulateur de transactions de paiement mobile  

6 362 620 transactions | 0.13% de fraudes



\## Notebooks



| Notebook | Description |

|---|---|

| 01\_EDA | Analyse exploratoire du dataset |

| 02\_FeatureEngineering | Création des variables explicatives |

| 03\_Modelisation | Entraînement Random Forest — ROC-AUC : 0.9999 |



\## Pipeline temps réel



1\. `producer.py` — envoie les transactions vers Kafka

2\. `consumer.py` — reçoit et analyse chaque transaction

3\. `api.py` — API FastAPI pour scorer une transaction



\## Résultats



\- 10 000 transactions traitées

\- 158 fraudes détectées

\- Score de confiance jusqu'à 1.0000



\## Lancer le projet



```bash

\# 1. Zookeeper

.\\bin\\windows\\zookeeper-server-start.bat .\\config\\zookeeper.properties



\# 2. Kafka

.\\bin\\windows\\kafka-server-start.bat .\\config\\server.properties



\# 3. Consumer

python consumer.py



\# 4. Producer

python producer.py



\# 5. API

python -m uvicorn api:app --reload

```



\## API Endpoints



| Endpoint | Méthode | Description |

|---|---|---|

| `/` | GET | Test API |

| `/predict` | POST | Scorer une transaction |

| `/stats` | GET | Statistiques des résultats |

