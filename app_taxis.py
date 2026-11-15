import pandas as pd
import streamlit as st

taxis = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv")


st.title("Dashboard Analyse Taxis - Zoubert")
arrondissement = taxis["pickup_borough"].unique()
quartier_prise = st.selectbox(
                                "Choisissez votre quartier de prise en charge:",
                                arrondissement
)

masque_quartier = taxis["pickup_borough"] == quartier_prise

st.dataframe(taxis[masque_quartier].head())
st.metric("Nombre total de courses enregistrées", len(masque_quartier))
