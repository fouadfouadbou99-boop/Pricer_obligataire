import streamlit as st
import pandas as pd
import plotly.express as px

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

    df = pd.read_excel(
        "courbe_taux.xlsx",
        engine="openpyxl"
    )

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    if "Taux" in df.columns:

        df.rename(
            columns={
                "Taux": "rate"
            },
            inplace=True
        )

    df["tenor"] = df["tenor"].astype(float)
    df["rate"] = df["rate"].astype(float)

    return df


try:

    curve_df = load_curve()

except Exception as e:

    st.error(
        f"Erreur lors du chargement de courbe_taux.xlsx : {e}"
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
# PARAMETRES OBLIGATION
# ==================================================

st.sidebar.header("Paramètres obligataires")

nominal = st.sidebar.number_input(
    "Nominal (MAD)",
    min_value=1000,
    value=1000000,
    step=10000
)

coupon_rate = st.sidebar.number_input(
    "Coupon annuel (%)",
    value=3.50,
    step=0.10
) / 100

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
# OBLIGATION
# ==================================================

bond = Bond(
)  
