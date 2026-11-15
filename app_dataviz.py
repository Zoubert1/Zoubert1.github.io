import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


st.title(" ✈️ Données sur les vols")

# 1) Chargement du dataset flights de Seaborn
@st.cache_data
def charger_donnees():
    return pd.read_csv("https://raw.githubusercontent.com/" \
                       f"mwaskom/seaborn-data/master/flights.csv")


df_flight = charger_donnees()


# Filtre par plage d'années
st.sidebar.header("Filtres")

annee_min, annee_max = int(df_flight["year"].min()), int(df_flight["year"].max())
plage_annees = st.sidebar.slider(
    "Plage d'années",
    min_value=annee_min,
    max_value=annee_max,
    value=(annee_min, annee_max),
)

mois_options = ["Tous les mois"] + list(df_flight["month"].unique())
mois_choisi = st.sidebar.selectbox("Mois", mois_options)

# Application des filtres
df_filtre = df_flight[df_flight["year"].between(plage_annees[0], plage_annees[1])]
if mois_choisi != "Tous les mois":
    df_filtre = df_filtre[df_filtre["month"] == mois_choisi]

# 4. Affichages
# 4.1 Indicateur
total = int(df_filtre["passengers"].sum())
st.metric(
    label=f"Total des passagers ({plage_annees[0]} - {plage_annees[1]}, {mois_choisi.lower()})",
    value=f"{total:,}".replace(",", " "),
)

# 4.2 Graphique en lignesadd
st.subheader("Évolution du nombre de passagers")

if df_filtre.empty:
    st.warning("Aucune donnée pour cette sélection.")
else:
    df_ligne = df_filtre.copy()
    # Construction d'un axe temporel (année + mois)
    df_ligne["date"] = pd.to_datetime(
        df_ligne["year"].astype(str) + "-" + df_ligne["month"].astype(str),
        format="%Y-%B",
    )
    df_ligne = df_ligne.sort_values("date").set_index("date")
    st.line_chart(df_ligne["passengers"])

# 4.3 Heatmap (case à cocher)
if st.checkbox("Afficher la heatmap (année × mois)"):
    st.subheader("Répartition des passagers par année et par mois")

    # Heatmap sur la plage d'années sélectionnée (tous les mois)
    df_heat = df_flight[df_flight["year"].between(plage_annees[0], plage_annees[1])]
    pivot = df_heat.pivot(index="month", columns="year", values="passengers")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
    ax.set_xlabel("Année")
    ax.set_ylabel("Mois")
    st.pyplot(fig)


