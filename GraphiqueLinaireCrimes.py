import pandas as pd
import plotly.express as px

# Charger les données
data = pd.read_excel('delinquance.xlsx')

# Filtrer les données pour le département 33
data_dept_33 = data[data['Code.département'] == 33]

# Agréger les données par année
crimes_par_annee = data_dept_33.groupby('annee')['faits'].sum().reset_index()

# Ajouter "20" devant les années
crimes_par_annee['annee'] = '20' + crimes_par_annee['annee'].astype(str)

# Tracer l'évolution temporelle des crimes avec Plotly
fig = px.line(crimes_par_annee, x='annee', y='faits', title='Évolution temporelle des crimes dans le département de la Gironde')
fig.update_xaxes(title_text='Année')
fig.update_yaxes(title_text='Nombre de crimes')
fig.show()
