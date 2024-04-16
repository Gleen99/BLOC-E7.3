import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Charger les données électorales présidentielles 2022
resultats_elections_data_2022 = pd.read_excel('resultats-par-niveau-cirlg-t1-france-entiere_2022.xlsx')
# Charger les données électorales présidentielles 2017
resultats_elections_data_2017 = pd.read_excel('éléction-2017.xlsx')
# Charger les données électorales des partis politiques
parties_politiques = pd.read_excel('df_partie.xlsx')

# Créer un dictionnaire pour associer chaque candidat à son parti politique correspondant
candidats_partis = {
    "ARTHAUD": "Lutte ouvrière",
    "ROUSSEL": "Parti communiste français",
    "MACRON": "La République en marche",
    "LASSALLE": "Résistons",
    "LE PEN": "Rassemblement national",
    "ZEMMOUR": "Reconquête",
    "MÉLENCHON": "La France insoumise",
    "HIDALGO": "Parti socialiste",
    "HAMON": "Parti socialiste",
    "JADOT": "Europe Écologie Les Verts",
    "PÉCRESSE": "Les Républicains",
    "FILLON": "Les Républicains",
    "POUTOU": "Nouveau Parti anticapitaliste",
    "DUPONT-AIGNAN": "Debout la France",
    "CHEMINADE": "Solidarité et Progrès",
    "ASSELINEAU": "Union Populaire Républicaine",
}

# Créer une liste pour stocker les résultats
data_to_plot = []

# Parcourir chaque candidat
for candidat, parti_candidat in candidats_partis.items():
    # Initialiser les compteurs de voix pour 2017 et 2022
    voix_2017 = 0
    voix_2022 = 0

    # Rechercher les voix obtenues par le candidat en 2017
    for colonne_nom in resultats_elections_data_2017.filter(like='Nom').columns:
        if candidat in resultats_elections_data_2017[colonne_nom].values:
            index = resultats_elections_data_2017[resultats_elections_data_2017[colonne_nom] == candidat].index[0]
            colonne_voix = resultats_elections_data_2017.columns[resultats_elections_data_2017.columns.get_loc(colonne_nom) + 2]
            voix_2017 += resultats_elections_data_2017.loc[index, colonne_voix]

    # Rechercher les voix obtenues par le candidat en 2022
    for colonne_nom in resultats_elections_data_2022.filter(like='Nom').columns:
        if candidat in resultats_elections_data_2022[colonne_nom].values:
            index = resultats_elections_data_2022[resultats_elections_data_2022[colonne_nom] == candidat].index[0]
            colonne_voix = resultats_elections_data_2022.columns[resultats_elections_data_2022.columns.get_loc(colonne_nom) + 2]
            voix_2022 += resultats_elections_data_2022.loc[index, colonne_voix]

    # Ajouter les résultats à la liste
    data_to_plot.append((parti_candidat, voix_2017, voix_2022))

# Créer un DataFrame à partir de la liste de résultats
df = pd.DataFrame(data_to_plot, columns=['Parti politique', 'Voix_2017', 'Voix_2022'])

# Créer une figure avec Plotly
fig = make_subplots(rows=2, cols=1, subplot_titles=("Votes exprimés en 2017", "Votes exprimés en 2022"))

# Ajouter les barres pour 2017
fig.add_trace(go.Bar(x=df['Parti politique'], y=df['Voix_2017'], name='2017'), row=1, col=1)

# Ajouter les barres pour 2022
fig.add_trace(go.Bar(x=df['Parti politique'], y=df['Voix_2022'], name='2022'), row=2, col=1)

# Mettre à jour les propriétés de la mise en page
fig.update_layout(title='Nombre de votes exprimés pour chaque parti politique en 2017 et 2022', barmode='group')

# Afficher la figure
fig.show()
