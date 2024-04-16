import pandas as pd
import plotly.graph_objs as go

# Charger les données électorales présidentielles 2022
resultats_elections_data_2022 = pd.read_excel('resultats-par-niveau-cirlg-t2-france-entiere_1.xlsx')
# Charger les données électorales présidentielles 2017
resultats_elections_data_2017 = pd.read_excel('Presidentielle_2017_Resultats_Communes_Tour_2_c.xlsx')

# Filtrer les données pour le département de la Gironde (code 33)
departement_2_2022 = resultats_elections_data_2022[resultats_elections_data_2022['Libellé du département'] == 'Gironde']
departement_2_2017 = resultats_elections_data_2017[resultats_elections_data_2017['Libellé du département'] == 'Gironde']

# Filtrer les données pour chaque candidat pour 2022
macron_2022 = departement_2_2022[((departement_2_2022['Nom'] == 'MACRON') & (departement_2_2022['Prénom'] == 'Emmanuel')) | ((departement_2_2022['Nom.1'] == 'MACRON') & (departement_2_2022['Prénom.1'] == 'Emmanuel'))]['Voix'].sum()
le_pen_2022 = departement_2_2022[((departement_2_2022['Nom'] == 'LE PEN') & (departement_2_2022['Prénom'] == 'Marine')) | ((departement_2_2022['Nom.1'] == 'LE PEN') & (departement_2_2022['Prénom.1'] == 'Marine'))]['Voix.1'].sum()

# Filtrer les données pour chaque candidat pour 2017
macron_2017 = departement_2_2017[((departement_2_2017['Nom'] == 'MACRON') & (departement_2_2017['Prénom'] == 'Emmanuel')) | ((departement_2_2017['Nom.1'] == 'MACRON') & (departement_2_2017['Prénom.1'] == 'Emmanuel'))]['Voix'].sum()
le_pen_2017 = departement_2_2017[((departement_2_2017['Nom'] == 'LE PEN') & (departement_2_2017['Prénom'] == 'Marine')) | ((departement_2_2017['Nom.1'] == 'LE PEN') & (departement_2_2017['Prénom.1'] == 'Marine'))]['Voix.1'].sum()

# Créer un graphique à barres pour comparer les résultats
fig = go.Figure(data=[
    go.Bar(name='Emmanuel Macron', x=['2022', '2017'], y=[macron_2022, macron_2017]),
    go.Bar(name='Marine Le Pen', x=['2022', '2017'], y=[le_pen_2022, le_pen_2017])
])

# Mettre en forme le graphique
fig.update_layout(title='Comparaison des résultats des élections présidentielles (Gironde)',
                  xaxis_title='Année',
                  yaxis_title='Nombre de voix',
                  barmode='group')

# Afficher le graphique
fig.show()
