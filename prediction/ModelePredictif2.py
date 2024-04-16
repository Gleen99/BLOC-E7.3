
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

# Chargement des données
df_chomage = pd.read_excel("df_chomage.xlsx")
df_crimes = pd.read_excel("df_crimes.xlsx")
df_resultats_elections = pd.read_excel("df_resultats_elections.xlsx")

# Néttoyage + préparation des données
df_resultats_elections['candidat'] = df_resultats_elections['candidat'].str.strip()
df_merged = pd.merge(df_resultats_elections, df_chomage, on='annee', how='left')
df_merged = pd.merge(df_merged, df_crimes, on='annee', how='left')

# Entrainement du modèle pour les candidats
def train_candidate_models(df, candidates):
    models = {}
    for candidate in candidates:
        data = df[df['candidat'] == candidate]
        X = data[['taux_chomage', 'nombre_crimes']]
        y = data['resultat_election']
        model = LinearRegression()
        model.fit(X, y)
        models[candidate] = model
    return models

# Prédictions des valeurs futures d'élections
def predict_future(models, df_future, years, candidates):
    predictions = []
    for candidate, model in models.items():
        X_future = df_future[['taux_chomage', 'nombre_crimes']]
        future_predictions = model.predict(X_future)
        for year, prediction in zip(years, future_predictions):
            predictions.append({
                'candidat': candidate,
                'annee': year,
                'predicted_result': prediction
            })
    return pd.DataFrame(predictions)

# Selection des candidats avec suffisament de données
key_candidates = df_resultats_elections.groupby('candidat').filter(lambda x: len(x) > 1)['candidat'].unique()

# Entrainment du modèle
candidate_models = train_candidate_models(df_merged, key_candidates)

# Préparation de la donnée pour les futures années
future_years = [2023, 2024, 2025, 2026]
df_future = pd.DataFrame({
    'annee': future_years,
    'taux_chomage': [6.5, 6.7, 7, 7.8],  # Taux de chomage prévu (à changer si on le souhaite)
    'nombre_crimes': [94000, 96000, 98000, 110000]  # Nombre de crimes prévu (à changer si on le souhaite)
})


"""
Prédiction 1 :
'taux_chomage': [6.5, 6.3, 6.1, 5.9]
'nombre_crimes': [95000, 96000, 97000, 99000]

Prédiction 2 :
'taux_chomage': [6.5, 6.2, 5.9, 5.6]
'nombre_crimes': [94000, 93000, 92000, 91000] 

Prédiction 3 :
'taux_chomage': [6.5, 6.7, 7, 7.8]
'nombre_crimes': [94000, 96000, 98000, 110000] 
"""


# Création des predictions pour les futures années
df_predictions = predict_future(candidate_models, df_future, future_years, key_candidates)

# Visualisation des résultats
plt.figure(figsize=(12, 8))
sns.lineplot(data=df_predictions, x='annee', y='predicted_result', hue='candidat', marker='o')
plt.title("Intention de vote pour chaque parti politique (Gironde) pour 2023, 2024, 2025 et 2026")
plt.xlabel('Année')
plt.ylabel('Pourcentage des votes (%)')
plt.legend(title='Parti politique')
plt.grid(True)
plt.show()
