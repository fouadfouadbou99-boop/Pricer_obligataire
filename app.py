import streamlit as st
import pandas as pd
import plotly.express as px

from bond import Bond
from courbe_zero import ZeroCurve
from risque import (
    macaulay_duration,
    modified_duration,
    dv01
)

st.set_page_config(
    page_title="Pricer Obligataire Maroc",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Pricer Obligataire Maroc")
st.markdown(
    "Valorisation, mesure du risque et analyse de sensibilité des obligations."
)

# ==========================
# Paramètres
# ==========================

st.sidebar.header("Paramètres obligataires")

nominal = st.sidebar.number_input(
    "Nominal (MAD)",
    value=1_000_000
)

coupon_pct = st.sidebar.number_input(
    "Coupon annuel (%)",
    value=3.50
)

maturity = st.sidebar.number_input(
    "Maturité (années)",
    value=10
)

frequency = st.sidebar.selectbox(
    "Fréquence coupon",
    [1, 2, 4],
    index=1
)

coupon = coupon_pct / 100

# ==========================
# Courbe des taux
# ==========================

try:

    curve_df = pd.read_csv("courbe_taux.csv")

    curve = ZeroCurve(
        "courbe_taux.csv"
    )

except Exception as e:

    st.error(
        f"Erreur lors du chargement de la courbe : {e}"
    )

    st.stop()

# ==========================
# Construction obligation
# ==========================

try:

    bond = Bond(
        nominal,
        coupon,
        maturity,
        frequency
    )

except Exception as e:

    st.exception(e)

    st.stop()

# ==========================
# Calcul risques
# ==========================

try:

    duration_mac = macaulay_duration(
        bond,
        curve
    )

    taux_marche = curve.get_rate(
        maturity
    )

    duration_mod = modified_duration(
        duration_mac,
        taux_marche
    )

    dv01_value = dv01(
        nominal,
        duration_mod
    )

except Exception as e:

    st.exception(e)

    st.stop()

# ==========================
# Résultats
# ==========================

st.subheader("Indicateurs de risque")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Duration Macaulay",
        f"{duration_mac:.4f}"
    )

with col2:

    st.metric(
        "Duration Modifiée",
        f"{duration_mod:.4f}"
    )

with col3:

    st.metric(
        "DV01",
        f"{dv01_value:,.2f} MAD"
    )

# ==========================
# Diagnostic courbe
# ==========================

st.subheader("Diagnostic Courbe")

diag = pd.DataFrame({
    "Maturité": [0.25, 0.5, 1, 2, 5, 10, 15, 20, 30],
    "Taux": [
        curve.get_rate(0.25),
        curve.get_rate(0.5),
        curve.get_rate(1),
        curve.get_rate(2),
        curve.get_rate(5),
        curve.get_rate(10),
        curve.get_rate(15),
        curve.get_rate(20),
        curve.get_rate(30)
    ]
})

st.dataframe(
    diag,
    use_container_width=True
)

# ==========================
# Graphique
# ==========================

st.subheader("Courbe des taux zéro")

fig = px.line(
    curve_df,
    x="tenor",
    y="rate",
    markers=True
)

fig.update_layout(
    xaxis_title="Maturité (années)",
    yaxis_title="Taux"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# Données marché
# ==========================

with st.expander(
        "Données de marché"):

    st.dataframe(
        curve_df,
        use_container_width=True
    )
