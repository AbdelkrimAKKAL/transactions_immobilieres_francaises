import sys
import os

# Ajouter la racine du projet au Python Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.analysis.queries import get_prix_moyen_dept, get_ventes_mensuelles, get_top_communes, get_repartition_type_bien, get_analyse_pieces

# ----------------- CONFIGURATION DE PAGE -----------------
st.set_page_config(page_title="DVF Market Intelligence", layout="wide", page_icon=":material/domain:")

# ----------------- INJECTION CSS (Design Premium) -----------------
def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        /* Font Globale */
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Cacher les éléments superflus */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Titre Header */
        .premium-title {
            font-size: 2.8rem;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
            padding-bottom: 0px;
        }
        
        .premium-subtitle {
            font-size: 1.1rem;
            color: #94a3b8;
            margin-bottom: 30px;
            margin-top: -10px;
        }
        
        /* Stylisation des KPI (Metrics) */
        div[data-testid="metric-container"] {
            background-color: rgba(30, 30, 45, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ----------------- EN-TÊTE -----------------
st.markdown('<h1 class="premium-title">DVF Market Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="premium-subtitle">Analyse professionnelle en temps réel des transactions immobilières françaises.</p>', unsafe_allow_html=True)

# ----------------- CHARGEMENT DES DONNÉES -----------------
@st.cache_data
def load_real_data():
    return {
        "nat": get_prix_moyen_dept(),
        "mensuel": get_ventes_mensuelles(),
        "top": get_top_communes(),
        "types": get_repartition_type_bien(),
        "pieces": get_analyse_pieces()
    }

with st.spinner("Analyse de la base de données MySQL et calcul des agrégations..."):
    data = load_real_data()

# ----------------- KPIS RAPIDES -----------------
total_ventes = data["nat"]['volume_ventes'].sum() if not data["nat"].empty else 0
prix_moyen_global = data["nat"]['prix_moyen_m2'].mean() if not data["nat"].empty else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Volume Total des Transactions", f"{total_ventes:,.0f}".replace(',', ' '))
col2.metric("Prix/m² Moyen National", f"{prix_moyen_global:,.0f} €".replace(',', ' '))
col3.metric("Départements Actifs", f"{len(data['nat'])}")
if not data["top"].empty:
    col4.metric("Commune la plus prisée", data["top"].iloc[0]['commune'])
else:
    col4.metric("Commune la plus prisée", "N/A")

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- THEME PLOTLY (Transparent/Épuré) -----------------
plotly_theme = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#94a3b8', family='Inter')
)

# ----------------- ONGLETS ET GRAPHIQUES -----------------
# On donne un style aux noms d'onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs([":material/map: Cartographie", ":material/calendar_month: Saisonnalité", ":material/star: Top Communes", ":material/pie_chart: Types de Biens", ":material/architecture: Analyse Pièces"])

with tab1:
    st.markdown("#### Disparité des prix par département")
    fig = px.bar(
        data["nat"], 
        x="code_departement", 
        y="prix_moyen_m2", 
        color="prix_moyen_m2",
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        **plotly_theme,
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_showscale=False # Cache la légende
    )
    # C'est ici qu'on force l'axe X à être de type 'category' (pour éviter l'axe de 0 à 900)
    fig.update_xaxes(showgrid=False, zeroline=False, type='category', title="Code Département")
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, title="Prix moyen / m² (€)")
    fig.update_traces(marker_line_width=0, opacity=0.9)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("#### Volume de transactions au fil des mois")
    fig2 = px.bar(
        data["mensuel"], 
        x="mois_nom", 
        y="volume_ventes", 
        text_auto='.2s'
    )
    fig2.update_traces(marker_color='#38bdf8', marker_line_width=0, opacity=0.85)
    fig2.update_layout(
        **plotly_theme
    )
    fig2.update_xaxes(showgrid=False, zeroline=False, type='category', title="")
    fig2.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, title="Volume de Ventes")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("#### Marchés les plus exclusifs (Top 20)")
    
    colA, colB = st.columns([1, 1.5])
    with colA:
        # Nettoyage pour un affichage parfait du tableau
        clean_df = data["top"].copy()
        clean_df['prix_moyen_m2'] = clean_df['prix_moyen_m2'].apply(lambda x: f"{x:,.0f} €".replace(',', ' '))
        clean_df.rename(columns={'commune': 'Commune', 'prix_moyen_m2': 'Prix / m²'}, inplace=True)
        st.dataframe(clean_df, hide_index=True, use_container_width=True)
        
    with colB:
        # Graphique horizontal élégant
        fig3 = px.bar(
            data["top"].sort_values('prix_moyen_m2', ascending=True), 
            y="commune", 
            x="prix_moyen_m2",
            orientation='h'
        )
        fig3.update_layout(
            **plotly_theme,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        fig3.update_xaxes(showgrid=False, zeroline=False, title="")
        fig3.update_yaxes(showgrid=False, zeroline=False, title="")
        fig3.update_traces(marker_color='#818cf8', marker_line_width=0, opacity=0.85)
        st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.markdown("#### Répartition du volume des ventes par Type de Bien")
    
    fig4 = px.pie(
        data["types"],
        values="volume_ventes",
        names="type_bien",
        hole=0.4, # Donut style
        color_discrete_sequence=['#3b82f6', '#8b5cf6', '#cbd5e1', '#38bdf8']
    )
    fig4.update_layout(
        **plotly_theme,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig4, use_container_width=True)

with tab5:
    st.markdown("#### Volume de transactions selon la taille (nombre de pièces)")
    
    colC, colD = st.columns([1.5, 1])
    with colC:
        fig5 = px.bar(
            data["pieces"],
            x="label_pieces",
            y="volume_ventes",
            text_auto=".2s"
        )
        fig5.update_layout(**plotly_theme)
        fig5.update_traces(marker_color='#38bdf8', marker_line_width=0, opacity=0.85)
        fig5.update_xaxes(showgrid=False, zeroline=False, type='category', title="")
        fig5.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, title="Volume de Ventes")
        st.plotly_chart(fig5, use_container_width=True)
        
    with colD:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("**💡 Info Marché**")
        st.info("Le marché immobilier français est le plus souvent dominé transactionnellement par les petites et moyennes surfaces (Studios au 3/4 Pièces).")
        
        # Petit tableau pour les prix moyens par nombre de pièces
        clean_pieces = data["pieces"][["label_pieces", "volume_ventes", "prix_moyen_m2"]].copy()
        clean_pieces['prix_moyen_m2'] = clean_pieces['prix_moyen_m2'].apply(lambda x: f"{x:,.0f} €" if not pd.isna(x) else "N/A")
        clean_pieces.rename(columns={'label_pieces': 'Logement', 'volume_ventes': 'Ventes', 'prix_moyen_m2': 'Prix moyen/m²'}, inplace=True)
        st.dataframe(clean_pieces, hide_index=True, use_container_width=True)

