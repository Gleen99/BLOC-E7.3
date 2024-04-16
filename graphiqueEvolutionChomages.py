import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Charger les données
data = pd.read_excel('TCRD_025.xlsx')
# Filtrer les données pour le département de la Gironde
gironde_data = data[data['Département'] == 'Gironde']

# Créer une figure avec Plotly
fig = make_subplots()
fig.update_layout(title='Évolution du taux de chômage dans la Gironde', xaxis_title='Trimestre', yaxis_title='Taux de chômage', xaxis=dict(tickangle=45))

# Définir les données initiales
initial_data = go.Scatter(x=gironde_data.columns[2:], y=gironde_data.iloc[0, 2:] * 10, mode='lines+markers', name='Gironde')

# Ajouter les données initiales à la figure
fig.add_trace(initial_data)

# Définir la fonction d'animation
def update(frame):
    # Mettre à jour les données
    new_data = go.Scatter(x=gironde_data.columns[2:], y=gironde_data.iloc[frame, 2:], mode='lines+markers', name='Gironde')
    # Mettre à jour la figure
    fig.data[0] = new_data

# Créer l'animation
frames = [go.Frame(data=[go.Scatter(x=gironde_data.columns[2:], y=gironde_data.iloc[i, 2:])], name=str(i)) for i in range(len(gironde_data))]
fig.frames = frames

# Afficher l'animation
fig.show()
