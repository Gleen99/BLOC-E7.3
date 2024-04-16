import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Charger les données électorales présidentielles 2022
resultats_elections_data = pd.read_excel('resultats-par-niveau-cirlg-t1-france-entiere.xlsx')
# Charger les données électorales présidentielles 2017
resultats_elections_data_dix_sept = pd.read_excel('éléction-2017.xlsx')

# Filtrer les données pour le département de la Gironde
gironde_data_2022 = resultats_elections_data[resultats_elections_data['Libellé du département'] == 'Gironde']
gironde_data_dix_sept = resultats_elections_data_dix_sept[resultats_elections_data_dix_sept['Libellé du département'] == 'Gironde']

# Calculer les sommes pour 2022
total_inscrits_2022 = gironde_data_2022['Inscrits'].sum()
total_votants_2022 = gironde_data_2022['Votants'].sum()
total_abstentions_2022 = gironde_data_2022['Abstentions'].sum()
total_votes_blancs_2022 = gironde_data_2022['Blancs'].sum()
total_votes_nuls_2022 = gironde_data_2022['Nuls'].sum()

# Calculer les sommes pour 2017
total_inscrits_2017 = gironde_data_dix_sept['Inscrits'].sum()
total_votants_2017 = gironde_data_dix_sept['Votants'].sum()
total_abstentions_2017 = gironde_data_dix_sept['Abstentions'].sum()
total_votes_blancs_2017 = gironde_data_dix_sept['Blancs'].sum()
total_votes_nuls_2017 = gironde_data_dix_sept['Nuls'].sum()

# Créer une figure avec Plotly
fig = make_subplots(rows=5, cols=1, subplot_titles=("Evolution des inscrits", "Evolution des votants", "Evolution des abstentions", "Evolution des votes blancs", "Evolution des votes nuls"))

# Ajouter les traces pour 2022
fig.add_trace(go.Scatter(x=['2022'], y=[total_inscrits_2022], mode='lines+markers', name='Inscrits 2022'), row=1, col=1)
fig.add_trace(go.Scatter(x=['2022'], y=[total_votants_2022], mode='lines+markers', name='Votants 2022'), row=2, col=1)
fig.add_trace(go.Scatter(x=['2022'], y=[total_abstentions_2022], mode='lines+markers', name='Abstentions 2022'), row=3, col=1)
fig.add_trace(go.Scatter(x=['2022'], y=[total_votes_blancs_2022], mode='lines+markers', name='Blancs 2022'), row=4, col=1)
fig.add_trace(go.Scatter(x=['2022'], y=[total_votes_nuls_2022], mode='lines+markers', name='Nuls 2022'), row=5, col=1)

# Ajouter les traces pour 2017
fig.add_trace(go.Scatter(x=['2017'], y=[total_inscrits_2017], mode='lines+markers', name='Inscrits 2017'), row=1, col=1)
fig.add_trace(go.Scatter(x=['2017'], y=[total_votants_2017], mode='lines+markers', name='Votants 2017'), row=2, col=1)
fig.add_trace(go.Scatter(x=['2017'], y=[total_abstentions_2017], mode='lines+markers', name='Abstentions 2017'), row=3, col=1)
fig.add_trace(go.Scatter(x=['2017'], y=[total_votes_blancs_2017], mode='lines+markers', name='Blancs 2017'), row=4, col=1)
fig.add_trace(go.Scatter(x=['2017'], y=[total_votes_nuls_2017], mode='lines+markers', name='Nuls 2017'), row=5, col=1)

# Mettre à jour les titres et les étiquettes des axes

# Afficher la figure
fig.show()
