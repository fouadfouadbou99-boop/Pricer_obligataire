import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Portefeuille Obligataire Maroc",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Portefeuille Obligataire Maroc")

# ==================================================
# CHARGEMENT PORTEFEUILLE
# ==================================================

try:

    portefeuille = pd.read_excel(
        "RPC_bonds_data_rpc.xlsx",
        engine="openpyxl"
    )

except Exception as e:

    st.error(
        f"Erreur chargement portefeuille : {e}"
    )

    st.stop()

# ==================================================
# CHARGEMENT COURBE
# ==================================================

try:

    courbe = pd.read_csv(
        "courbe_taux.csv"
    )

except Exception as e:

    st.error(
        f"Erreur chargement courbe : {e}"
    )

    st.stop()

# ==================================================
# PREPARATION
# ==================================================

portefeuille.columns = [
    str(col).strip()
    for col in portefeuille.columns
]

# ==================================================
# KPI
# ==================================================

nominal_total = 0

if "Nominal Global" in portefeuille.columns:

    nominal_total = pd.to_numeric(
        portefeuille["Nominal Global"],
        errors="coerce"
    ).fillna(0).sum()

nombre_positions = len(
    portefeuille
)

coupon_moyen = 0

if "Taux facial" in portefeuille.columns:

    coupon_moyen = (
        pd.to_numeric(
            portefeuille["Taux facial"],
            errors="coerce"
        ).fillna(0).mean()
    ) * 100

tra_moyen = 0

if "TRA" in portefeuille.columns:

    tra_moyen = (
        pd.to_numeric(
            portefeuille["TRA"],
            errors="coerce"
        ).fillna(0).mean()
    ) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Nominal Total",
        f"{nominal_total:,.0f} MAD"
    )

with col2:

    st.metric(
        "Nombre de lignes",
        nombre_positions
    )

with col3:

    st.metric(
        "Coupon Moyen",
        f"{coupon_moyen:.2f}%"
    )

with col4:

    st.metric(
        "TRA Moyen",
        f"{tra_moyen:.2f}%"
    )

# ==================================================
# TABLEAU PORTEFEUILLE
# ==================================================

st.subheader("📁 Portefeuille")

colonnes = [
    "Code",
    "Description Titres",
    "Date Echéance",
    "Taux facial",
    "Quantité",
    "Nominal Global",
    "Spread",
    "TRA"
]

colonnes_existantes = [
    c
    for c in colonnes
    if c in portefeuille.columns
]

st.dataframe(
    portefeuille[
        colonnes_existantes
    ],
    use_container_width=True
)

# ==================================================
# COURBE DES TAUX
# ==================================================

st.subheader(
    "📈 Courbe des Taux"
)

try:

    fig = px.line(
        courbe,
        x="tenor",
        y="rate",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Maturité",
        yaxis_title="Taux"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Erreur graphique : {e}"
    )

# ==================================================
# DONNEES COURBE
# ==================================================

with st.expander(
    "Afficher les données de la courbe"
):

    st.dataframe(
        courbe,
        use_container_width=True
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Portefeuille Obligataire Maroc"
)
