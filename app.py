import os
import zipfile

import pandas as pd
import plotly.express as px
import streamlit as st

from bond import Bond
from courbe_zero import ZeroCurve
from risque import (
    macaulay_duration,
    modified_duration,
    convexity,
    dv01
)

# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Pricer Obligataire Maroc",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Pricer Obligataire Maroc")

st.markdown(
    "Valorisation, mesure du risque et analyse de sensibilité des obligations."
)

# ==================================================
# CHARGEMENT COURBE EXCEL
# ==================================================

@st.cache_data
def load_curve():

    file_path = "courbe_taux.xlsx"

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Le fichier '{file_path}' est introuvable."
        )

    if not zipfile.is_zipfile(file_path):
        raise ValueError(
            "Le fichier courbe_taux.xlsx n'est pas un fichier Excel valide."
        )

    df = pd.read_excel(
        file_path,
        engine="openpyxl"
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    if "Taux" in df.columns:
        df.rename(
            columns={"Taux": "rate"},
            inplace=True
        )

    required_columns = ["tenor", "rate"]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Colonnes manquantes : {missing_columns}"
        )

    df["tenor"] = pd.to_numeric(
        df["tenor"],
        errors="coerce"
    )

    df["rate"] = pd.to_numeric(
        df["rate"],
        errors="coerce"
    )

    df = df.dropna()

    return df


try:

    curve_df = load_curve()

except Exception as e:

    st.error(
        f"Erreur lors du chargement de courbe_taux.xlsx : {e}"
    )

    st.write(
        "Répertoire courant :",
        os.getcwd()
    )

    st.write(
        "Fichiers détectés :",
        os.listdir(".")
    )

    st.stop()

# ==================================================
# CONSTRUCTION COURBE ZERO
# ==================================================

curve = ZeroCurve(
    curve_df["tenor"],
    curve_df["rate"]
)

# ==================================================
# AFFICHAGE COURBE DES TAUX
# ==================================================

st.subheader("Courbe des taux")

fig = px.line(
    curve_df,
    x="tenor",
    y="rate",
    markers=True,
    labels={
        "tenor": "Maturité (années)",
        "rate": "Taux"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# PARAMETRES OBLIGATION
# ==================================================

st.sidebar.header("Paramètres obligataires")

nominal = st.sidebar.number_input(
    "Nominal (MAD)",
    min_value=1000,
    value=1000000,
    step=10000
)

coupon_rate = (
    st.sidebar.number_input(
        "Coupon annuel (%)",
        value=3.50,
        step=0.10
    ) / 100
)

maturity = st.sidebar.number_input(
    "Maturité (années)",
    min_value=1,
    max_value=50,
    value=10
)

frequency = st.sidebar.selectbox(
    "Fréquence coupon",
    [1, 2],
    index=1
)

market_price = st.sidebar.number_input(
    "Prix de marché",
    value=float(nominal),
    step=1000.0
)

# ==================================================
# CREATION OBLIGATION
# ==================================================

try:

    bond = Bond(
        nominal=nominal,
        coupon_rate=coupon_rate,
        maturity=maturity,
        frequency=frequency
    )

except Exception as e:

    st.error(
        f"Erreur lors de la création de l'obligation : {e}"
    )

    st.stop()
