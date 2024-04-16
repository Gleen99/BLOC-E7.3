import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Charger les données
data = pd.read_excel('delinquance.xlsx')

# Filtrer les données pour le département 33
data_dept_33 = data[data['Code.département'] == 33]

# Créer un graphique pour chaque année
fig = make_subplots(rows=3, cols=2, subplot_titles=('22',  '23'))

# Liste des années à afficher
years = [22, 23]

# Créer un graphique pour chaque année
for i, year in enumerate(years, start=1):
    # Filtrer les données pour l'année en cours
    data_year = data_dept_33[data_dept_33['annee'] == year]

    # Calculer le nombre total de crimes par classe de délinquance pour l'année en cours
    total_crimes = data_year.groupby('classe')['faits'].sum().reset_index()

    # Créer un diagramme à barres pour l'année en cours
    fig.add_trace(
        go.Bar(x=total_crimes['classe'], y=total_crimes['faits'], name=f'Année {year}'),
        row=(i + 1) // 2, col=(i % 2) + 1
    )

# Mettre à jour les propriétés de la mise en page pour centrer le graphique
fig.update_layout(
    title='Répartition des différents types de crimes dans le département de la Gironde par année',
    showlegend=False,
    margin=dict(t=100, b=100, l=100, r=100)  # Ajustement des marges
)

# Afficher les graphiques
fig.show()
