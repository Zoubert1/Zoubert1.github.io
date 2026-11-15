import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/" \
          "mwaskom/seaborn-data/master/flights.csv"
    return pd.read_csv(url)


df_flights = load_data()


st.subheader("Aperçu des données")
st.dataframe(df_flights.head(10))

# Affichage de KPI
total_passengers = df_flights["passengers"].sum()
st.metric("Total de passagers historiques", f"{total_passengers:,}")


# Approche 1: Graphiques natifs Streamlit (st. *_chart)
annual_passengers = df_flights.groupby("year")["passengers"].sum()

st.subheader("Evolution du trafic aérien (Bar Chart natif)")
st.bar_chart(annual_passengers)


# Approche 2 : Matplotlib & Seaborn (st.pyplot)

df_iris = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")

st.subheader("Distribution par espèce (Seaborn)")

# 1. Creation explicite de la figure
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=df_iris, x="species", y="sepal_length", ax=ax, palette="viridis")
ax.set_title("Longueur moyenne des sépales par espèce")

# 2. Rendu dans Streamlit
st.pyplot(fig)


# Approche 3: Plotly pour des graphiques ultra-interactifs (st.plotly_chart)
st.subheader("Nuage de points interactif (Plotly)")

# Création de la figure Plotly
fig_plotly = px.scatter(
                        df_iris, 
                        x="sepal_width", 
                        y="sepal_length", 
                        color="species", 
                        size="petal_length", 
                        hover_data=["petal_width"], 
                        title="Relation Sépale vs Pétale"
)

# Rendu dans Streamlit
st.plotly_chart(fig_plotly, use_container_width=True)


st.title("📊 Explorateur Interactif Seaborn Data")

# 1. Sélectionn du jeu de données
dataset_name = st.selectbox(
    "Choisissez un jeu de données Seaborn :", 
    ["flights", "iris", "penguins", "taxis"] 
)

# Chargement dynamique 
@st.cache_data 
def get_dataset(name):
    return pd.read_csv("https://raw.githubusercontent.com/" \
                       f"mwaskom/seaborn-data/master/{name}.csv") 

df = get_dataset(dataset_name) 

st.write(f"### Aperçu du '{dataset_name}' ({df.shape[0]} lignes, {df.shape[1]} colonnes)")
st.dataframe(df.head())

# 2. Configuration du graphique interactif
st.subheader("Configuration de la visualisation")
num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if len(num_cols) >= 2:
    col_x = st.selectbox("Axe X :", num_cols, index=0)
    col_y = st.selectbox("Axe Y :", num_cols, index=min(1, len(num_cols)-1)) 
    chart_type = st.radio("Type de graphique :", 
                          ["Scatter Chart", "Line Chart", "Bar Chart"], horizontal=True)

    # Génération du graphique selon le choix
    if chart_type == "Scatter Chart": 
        st.scatter_chart(df, x=col_x, y=col_y) 
    elif chart_type == "Line Chart": 
        st.line_chart(df.set_index(col_x)[col_y]) 
    elif chart_type == "Bar Chart": 
        st.bar_chart(df.set_index(col_x)[col_y]) 

    # Option pour afficher la matrice de corrélation
    st.divider() 
    if st.checkbox("Afficher la matrice de corrélation numérique"): 
        st.subheader("Matrice de corrélation") 
        corr = df[num_cols].corr() 
        
        fig_corr, ax_corr = plt.subplots(figsize=(6, 4))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax_corr) 
        st.pyplot(fig_corr) 
    else: 
        st.warning("Ce jeu de données ne contient pas assez " \
                   "de colonnes numériques pour générer ce graphique.")