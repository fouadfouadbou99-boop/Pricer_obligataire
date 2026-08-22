import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Portefeuille Obligataire Maroc",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Portefeuille Obligataire Maroc")

# =====================================================
# CHARGEMENT DES DONNEES
# =====================================================

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

try:

    courbe = pd.read_csv(
        "courbe_taux.csv"
    )

except Exception as e:

    st.error(
        f"Erreur chargement courbe : {e}"
    )

    st.stop()

# =====================================================
# PREPARATION DES DONNEES
# =====================================================

portefeuille.columns = [
    str(col).strip()
    for col in portefeuille.columns
]

numeric_cols = [
    "Nominal Global",
    "Taux facial",
    "TRA"
]

for col in numeric_cols:

    if col in portefeuille.columns:

        portefeuille[col] = pd.to_numeric(
            portefeuille[col],
            errors="coerce"
        )

# =====================================================
# KPI
# =====================================================

nominal_total = portefeuille[
    "Nominal Global"
].fillna(0).sum()

nombre_positions = len(
    portefeuille
)

coupon_moyen = (
    portefeuille["Taux facial"]
    .fillna(0)
    .mean()
) * 100

tra_moyen = (
    portefeuille["TRA"]
    .fillna(0)
    .mean()
) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Nominal Total",
        f"{nominal_total:,.0f} MAD"
    )

with col2:

    st.metric(
        "Nombre Positions",
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

# =====================================================
# PORTFOLIO
# =====================================================

st.subheader("Portefeuille")

colonnes = [

    "Code",
    "Description Titres",
    "Date Eché
    )
