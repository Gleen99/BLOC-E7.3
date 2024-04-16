import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# Chargement des données
def load_data():
    df_chomage = pd.read_excel("df_chomage.xlsx")
    df_crimes = pd.read_excel("df_crimes.xlsx")
    df_elections = pd.read_excel("df_resultats_elections.xlsx")
    return df_chomage, df_crimes, df_elections

# Prétraitement et interpolation des résultats des élections
def preprocess_and_interpolate(df_chomage, df_crimes, df_elections):
    df_elections['candidat'] = df_elections['candidat'].str.strip()
    df = pd.merge(pd.merge(df_elections, df_chomage, on='annee'), df_crimes, on='annee')
    
    def interpolate_results(candidate, years):
        candidate_data = df[df['candidat'] == candidate]
        candidate_data = candidate_data.sort_values('annee')
        if len(candidate_data) > 3:
            spline = UnivariateSpline(candidate_data['annee'].values, candidate_data['resultat_election'].values, s=0)
            return spline(years)
        else:
            return np.interp(years, candidate_data['annee'], candidate_data['resultat_election'])

    years = np.arange(df['annee'].min(), df['annee'].max() + 1)
    interpolated_results = {}
    for candidate in df['candidat'].unique():
        interpolated_results[candidate] = interpolate_results(candidate, years)
    
    all_candidates = np.repeat(df['candidat'].unique(), len(years))
    all_years = np.tile(years, len(df['candidat'].unique()))
    results = np.concatenate([interpolated_results[c] for c in df['candidat'].unique()])
    
    df_interpolated = pd.DataFrame({
        'annee': all_years,
        'candidat': all_candidates,
        'resultat_election': results
    })
    return df_interpolated

# Prédictions futures
def predict_future_results(model, years, df, df_chomage, df_crimes):
    future_data = pd.DataFrame({
        'annee': np.tile(years, len(df['candidat'].unique())),
        'candidat': np.repeat(df['candidat'].unique(), len(years))
    })
    future_data = future_data.merge(df_chomage, on='annee', how='left').merge(df_crimes, on='annee', how='left')
    future_data.fillna({
        'taux_chomage': df_chomage['taux_chomage'].mean(),
        'nombre_crimes': df_crimes['nombre_crimes'].mean()
    }, inplace=True)
    
    le = LabelEncoder()
    future_data['candidat_encoded'] = le.fit_transform(future_data['candidat'])
    X_future = future_data[['annee', 'taux_chomage', 'nombre_crimes', 'candidat_encoded']]
    X_future_scaled = StandardScaler().fit_transform(X_future)
    future_data['resultat_election'] = model.predict(X_future_scaled)
    return future_data

# Formation et évaluation du modèle
def train_model(df):
    le = LabelEncoder()
    df['candidat_encoded'] = le.fit_transform(df['candidat'])
    X = df[['annee', 'taux_chomage', 'nombre_crimes', 'candidat_encoded']]
    y = df['resultat_election']
    X_scaled = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# Visualisation des résultats
def plot_election_results(df):
    plt.figure(figsize=(14, 8))
    for candidate in df['candidat'].unique():
        candidate_data = df[df['candidat'] == candidate]
        plt.plot(candidate_data['annee'], candidate_data['resultat_election'], marker='o', label=candidate)
    plt.title('Résultats des élections interpolés et prédictions futures par année pour chaque candidat')
    plt.xlabel('Année')
    plt.ylabel('Pourcentage des voix (%)')
    plt.legend(title='Candidat')
    plt.grid(True)
    plt.show()

# Programme principal
def main():
    df_chomage, df_crimes, df_elections = load_data()
    df_interpolated = preprocess_and_interpolate(df_chomage, df_crimes, df_elections)
    model = train_model(df_interpolated)
    future_years = [2023, 2024, 2025]
    df_future_predictions = predict_future_results(model, future_years, df_interpolated, df_chomage, df_crimes)
    df_combined_visualization = pd.concat([df_interpolated, df_future_predictions])
    plot_election_results(df_combined_visualization)

if __name__ == '__main__':
    main()
