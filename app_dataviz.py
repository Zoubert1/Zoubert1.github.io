import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# st.title(" ✈️ Données sur les vols")

# # 1) Chargement du dataset flights de Seaborn
# @st.cache_data
# def charger_donnees():
#     return pd.read_csv("https://raw.githubusercontent.com/" \
#                        f"mwaskom/seaborn-data/master/flights.csv")


# df_flight = charger_donnees()


# # Filtre par plage d'années
# st.sidebar.header("Filtres")

# annee_min, annee_max = int(df_flight["year"].min()), int(df_flight["year"].max())
# plage_annees = st.sidebar.slider(
#     "Plage d'années",
#     min_value=annee_min,
#     max_value=annee_max,
#     value=(annee_min, annee_max),
# )

# mois_options = ["Tous les mois"] + list(df_flight["month"].unique())
# mois_choisi = st.sidebar.selectbox("Mois", mois_options)

# # Application des filtres
# df_filtre = df_flight[df_flight["year"].between(plage_annees[0], plage_annees[1])]
# if mois_choisi != "Tous les mois":
#     df_filtre = df_filtre[df_filtre["month"] == mois_choisi]

# # 4. Affichages
# # 4.1 Indicateur
# total = int(df_filtre["passengers"].sum())
# st.metric(
#     label=f"Total des passagers ({plage_annees[0]} - {plage_annees[1]}, {mois_choisi.lower()})",
#     value=f"{total:,}".replace(",", " "),
# )

# # 4.2 Graphique en lignesadd
# st.subheader("Évolution du nombre de passagers")

# if df_filtre.empty:
#     st.warning("Aucune donnée pour cette sélection.")
# else:
#     df_ligne = df_filtre.copy()
#     # Construction d'un axe temporel (année + mois)
#     df_ligne["date"] = pd.to_datetime(
#         df_ligne["year"].astype(str) + "-" + df_ligne["month"].astype(str),
#         format="%Y-%B",
#     )
#     df_ligne = df_ligne.sort_values("date").set_index("date")
#     st.line_chart(df_ligne["passengers"])

# # 4.3 Heatmap (case à cocher)
# if st.checkbox("Afficher la heatmap (année × mois)"):
#     st.subheader("Répartition des passagers par année et par mois")

#     # Heatmap sur la plage d'années sélectionnée (tous les mois)
#     df_heat = df_flight[df_flight["year"].between(plage_annees[0], plage_annees[1])]
#     pivot = df_heat.pivot(index="month", columns="year", values="passengers")

#     fig, ax = plt.subplots(figsize=(12, 6))
#     sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
#     ax.set_xlabel("Année")
#     ax.set_ylabel("Mois")
#     st.pyplot(fig)



"""
Trafic aérien 1949-1960 : tableau de bord interactif
Stack : Streamlit · Pandas · Plotly
Lancer avec : streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Trafic aérien 1949-1960",
    page_icon="✈️",
    layout="wide",
)

URL_DONNEES = (
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
)

MOIS_FR = {
    "January": "Janvier", "February": "Février", "March": "Mars",
    "April": "Avril", "May": "Mai", "June": "Juin",
    "July": "Juillet", "August": "Août", "September": "Septembre",
    "October": "Octobre", "November": "Novembre", "December": "Décembre",
}
ORDRE_MOIS = list(MOIS_FR.values())

# Palette
NUIT = "#0F2A43"
HORIZON = "#2E6F95"
CIEL = "#9CC5E0"
BALISE = "#F2A541"
BRUME = "#F3F6F9"

# Liens à personnaliser
LIEN_LINKEDIN = "https://www.linkedin.com/in/zoubert-hamidouni"

# ----------------------------------------------------------------------------
# Style
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

    html, body, [class*="css"], .stMarkdown, label {{
        font-family: 'IBM Plex Sans', sans-serif;
    }}
    .block-container {{ padding-top: 2rem; max-width: 1200px; }}

    /* En-tête */
    .hero {{
        background: {NUIT};
        color: white;
        padding: 2rem 2.2rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        border-left: 6px solid {BALISE};
    }}
    .hero h1 {{
        font-family: 'Fraunces', serif;
        font-size: 2.3rem;
        margin: 0 0 .4rem 0;
        color: white;
        line-height: 1.15;
    }}
    .hero p {{ margin: 0; color: {CIEL}; font-size: 1.02rem; max-width: 62ch; }}
    .tags {{ margin-top: 1rem; }}
    .tag {{
        display: inline-block;
        border: 1px solid {CIEL};
        color: white;
        border-radius: 999px;
        padding: .15rem .8rem;
        margin-right: .4rem;
        font-size: .82rem;
    }}

    /* Indicateurs */
    [data-testid="stMetric"] {{
        background: {BRUME};
        border: 1px solid #DCE5EC;
        border-top: 4px solid {HORIZON};
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }}
    [data-testid="stMetricValue"] {{
        font-family: 'Fraunces', serif;
        color: {NUIT};
    }}
    [data-testid="stMetricLabel"] p {{ color: {HORIZON}; font-weight: 500; }}

    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {{ gap: 1.2rem; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 500; }}

    /* Pied de page */
    .footer {{
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid #DCE5EC;
        color: #5B6B7A;
        font-size: .9rem;
    }}
    .footer a {{ color: {HORIZON}; text-decoration: none; font-weight: 500; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Données
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner="Chargement des données…")
def charger_donnees() -> pd.DataFrame:
    df = pd.read_csv(URL_DONNEES)
    df["mois"] = pd.Categorical(
        df["month"].map(MOIS_FR), categories=ORDRE_MOIS, ordered=True
    )
    df["date"] = pd.to_datetime(
        {"year": df["year"], "month": df["mois"].cat.codes + 1, "day": 1}
    )
    return df.drop(columns="month").rename(columns={"year": "annee"})


def formater(n: float) -> str:
    """Sépare les milliers par une espace : 1234567 -> 1 234 567."""
    return f"{n:,.0f}".replace(",", " ")


df = charger_donnees()

# ----------------------------------------------------------------------------
# Barre latérale : filtres
# ----------------------------------------------------------------------------
st.sidebar.header("Filtres")

annee_min, annee_max = int(df["annee"].min()), int(df["annee"].max())
plage = st.sidebar.slider(
    "Période",
    min_value=annee_min,
    max_value=annee_max,
    value=(annee_min, annee_max),
)

mois_choisis = st.sidebar.multiselect(
    "Mois",
    options=ORDRE_MOIS,
    default=ORDRE_MOIS,
    help="Retirez des mois pour isoler une saison (ex. juillet-août).",
)

tous_les_mois = len(mois_choisis) == len(ORDRE_MOIS)
afficher_tendance = st.sidebar.toggle(
    "Tendance (moyenne mobile 12 mois)",
    value=True,
    disabled=not tous_les_mois,
    help="Disponible uniquement quand les 12 mois sont sélectionnés.",
)

df_f = df[df["annee"].between(*plage) & df["mois"].isin(mois_choisis)]

# ----------------------------------------------------------------------------
# En-tête
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Trafic aérien, 1949-1960</h1>
        <p>Douze ans de passagers, mois par mois. Une tendance qui monte
        et une saisonnalité qui s'amplifie avec elle.</p>
        <div class="tags">
            <span class="tag">Python</span>
            <span class="tag">Pandas</span>
            <span class="tag">Plotly</span>
            <span class="tag">Streamlit</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if df_f.empty:
    st.warning("Aucune donnée pour cette sélection. Choisissez au moins un mois.")
    st.stop()

# ----------------------------------------------------------------------------
# Indicateurs
# ----------------------------------------------------------------------------
total = df_f["passengers"].sum()
moyenne = df_f["passengers"].mean()
record = df_f.loc[df_f["passengers"].idxmax()]

annuel = df_f.groupby("annee", as_index=False)["passengers"].sum()
if len(annuel) >= 2:
    croissance = annuel["passengers"].iloc[-1] / annuel["passengers"].iloc[0] - 1
    texte_croissance = f"{croissance:+.0%}".replace("+", "+ ")
    libelle_croissance = f"Croissance {annuel['annee'].iloc[0]} → {annuel['annee'].iloc[-1]}"
else:
    texte_croissance, libelle_croissance = "n/a", "Croissance"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Passagers (milliers)", f"{formater(total)}k")
c2.metric("Moyenne mensuelle", f"{formater(moyenne)}k")
c3.metric("Mois record", f"{record['mois']} {record['annee']}", f"{formater(record['passengers'])} passagers", delta_color="off")
c4.metric(libelle_croissance, texte_croissance)

st.write("")

# ----------------------------------------------------------------------------
# Graphiques
# ----------------------------------------------------------------------------
GABARIT = dict(
    template="plotly_white",
    font=dict(family="IBM Plex Sans, sans-serif", color=NUIT),
    margin=dict(l=10, r=10, t=50, b=10),
    title_font=dict(family="Fraunces, serif", size=20),
)

onglet_evolution, onglet_saison, onglet_annee, onglet_donnees = st.tabs(
    ["Évolution", "Saisonnalité", "Bilan annuel", "Données"]
)

# --- Évolution --------------------------------------------------------------
with onglet_evolution:
    df_ligne = df_f.sort_values("date")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_ligne["date"],
            y=df_ligne["passengers"],
            name="Passagers",
            mode="lines+markers" if not tous_les_mois else "lines",
            line=dict(color=HORIZON, width=2),
            fill="tozeroy",
            fillcolor="rgba(46, 111, 149, 0.10)",
            hovertemplate="%{x|%B %Y}<br><b>%{y:,.0f}</b> passagers<extra></extra>",
        )
    )
    if tous_les_mois and afficher_tendance and len(df_ligne) >= 12:
        tendance = df_ligne["passengers"].rolling(12, center=True).mean()
        fig.add_trace(
            go.Scatter(
                x=df_ligne["date"],
                y=tendance,
                name="Moyenne mobile 12 mois",
                line=dict(color=BALISE, width=3),
                hovertemplate="Tendance : <b>%{y:,.0f}</b><extra></extra>",
            )
        )
    fig.update_layout(
        **GABARIT,
        title="Passagers par mois",
        yaxis_title="Passagers (milliers)",
        xaxis_title=None,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1, x=1, xanchor="right"),
    )
    st.plotly_chart(fig, width="stretch")

# --- Saisonnalité -----------------------------------------------------------
with onglet_saison:
    matrice = df_f.pivot_table(
        index="annee", columns="mois", values="passengers", observed=False
    ).reindex(columns=mois_choisis if mois_choisis else ORDRE_MOIS)
    fig = px.imshow(
        matrice,
        aspect="auto",
        color_continuous_scale=[[0, "#EAF2F8"], [0.5, CIEL], [1, NUIT]],
        labels=dict(color="Passagers", x="", y=""),
    )
    fig.update_traces(hovertemplate="%{y} · %{x}<br><b>%{z:,.0f}</b> passagers<extra></extra>")
    fig.update_layout(**GABARIT, title="Carte de chaleur : année × mois")
    fig.update_yaxes(autorange="reversed", dtick=1)
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "Les étés (juillet-août) dominent chaque année, et l'écart avec l'hiver "
        "se creuse à mesure que le trafic augmente."
    )

# --- Bilan annuel -----------------------------------------------------------
with onglet_annee:
    couleurs = [CIEL] * len(annuel)
    couleurs[-1] = HORIZON
    fig = go.Figure(
        go.Bar(
            x=annuel["annee"],
            y=annuel["passengers"],
            marker_color=couleurs,
            text=[formater(v) for v in annuel["passengers"]],
            textposition="outside",
            hovertemplate="%{x}<br><b>%{y:,.0f}</b> passagers<extra></extra>",
        )
    )
    fig.update_layout(
        **GABARIT,
        title="Total annuel de passagers",
        yaxis_title=None,
        xaxis=dict(type="category"),
        yaxis=dict(showgrid=False, showticklabels=False),
        uniformtext=dict(minsize=9, mode="hide"),
    )
    st.plotly_chart(fig, width="stretch")

# --- Données ----------------------------------------------------------------
with onglet_donnees:
    tableau = (
        df_f.sort_values("date")[["annee", "mois", "passengers"]]
        .rename(columns={"annee": "Année", "mois": "Mois", "passengers": "Passagers"})
    )
    st.dataframe(tableau, width="stretch", hide_index=True)
    st.download_button(
        "Télécharger la sélection (CSV)",
        data=tableau.to_csv(index=False).encode("utf-8"),
        file_name="trafic_aerien_selection.csv",
        mime="text/csv",
    )

# ----------------------------------------------------------------------------
# Pied de page
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="footer">
        Source : jeu de données <i>flights</i> (seaborn-data). Réalisé avec Streamlit et Plotly.<br>
        <a href="{LIEN_LINKEDIN}" target="_blank">LinkedIn</a> ·
    </div>
    """,
    unsafe_allow_html=True,
)