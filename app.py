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

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Pricer Obligataire Maroc",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Pricer Obligataire Maroc")

st.markdown(
    """
    Application de valorisation obligataire :
    - Prix théorique
    - Yield To Maturity (YTM)
    - Duration de Macaulay
    - Duration modifiée
    - Convexité
    - DV01
    - Analyse de sensibilité
    """
)

# =====================================================
# CHARGEMENT COURBE
# =====================================================

@st.cache_data
def load_curve():

    df = pd.read_csv("courbe_taux.csv")

    df["tenor"] = df["tenor"].astype(float)
    df["rate"] = df["rate"].astype(float)

    return df


try:

    curve_df = load_curve()

except Exception as e:

    st.error(
        f"Erreur lors du chargement de courbe_taux.csv : {e}"
    )

    st.stop()

# =====================================================
# CONSTRUCTION COURBE ZERO
# =====================================================

curve = ZeroCurve(
    curve_df["tenor"],
    curve_df["rate"]
)

# =====================================================
# PARAMETRES
# =====================================================

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

# =====================================================
# OBLIGATION
# =====================================================

bond = Bond(
    nominal,
    coupon_rate,
    maturity,
    frequency
)

# =====================================================
# CALCULS
# =====================================================

price = bond.price(curve)

duration = macaulay_duration(
    bond,
    curve
)

mod_duration = modified_duration(
    bond,
    curve
)

conv = convexity(
    bond,
    curve
)

dv01_value = dv01(
    bond,
    curve
)

try:

    ytm = bond.ytm(
        market_price
    )

except:

    ytm = None

# =====================================================
# TABLEAU DE BORD
# =====================================================

st.subheader("Tableau de Bord")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Prix Théorique",
        f"{price:,.2f} MAD"
    )

with col2:

    st.metric(
        "Prix Marché",
        f"{market_price:,.2f} MAD"
    )

with col3:

    st.metric(
        "Ecart",
        f"{price-market_price:,.2f}"
    )

col4, col5, col6 = st.columns(3)

with col4:

    if ytm is not None:

        st.metric(
            "YTM",
            f"{ytm*100:.2f}%"
        )

with col5:

    st.metric(
        "Duration",
        f"{duration:.2f}"
    )

with col6:

    st.metric(
        "Duration Modifiée",
        f"{mod_duration:.2f}"
    )

col7, col8 = st.columns(2)

with col7:

    st.metric(
        "Convexité",
        f"{conv:.2f}"
    )

with col8:

    st.metric(
        "DV01",
        f"{dv01_value:,.2f}"
    )

# =====================================================
# COURBE DES TAUX
# =====================================================

st.subheader("Courbe Zéro Coupon")

fig_curve = px.line(
    curve_df,
    x="tenor",
    y="rate",
    markers=True
)

fig_curve.update_layout(
    xaxis_title="Maturité (années)",
    yaxis_title="Taux"
)

st.plotly_chart(
    fig_curve,
    use_container_width=True
)

# =====================================================
# ANALYSE DE SENSIBILITE
# =====================================================

st.subheader("Analyse de Sensibilité")

shocks = [
    -100,
    -50,
    0,
    50,
    100
]

results = []

for shock in shocks:

    shifted_curve = ZeroCurve(
        curve_df["tenor"],
        curve_df["rate"] + shock/10000
    )

    shocked_price = bond.price(
        shifted_curve
    )

    results.append(
        {
            "Choc (pb)": shock,
            "Prix": round(
                shocked_price,
                2
            )
        }
    )

sens_df = pd.DataFrame(
    results
)

st.dataframe(
    sens_df,
    use_container_width=True
)

fig_sens = px.line(
    sens_df,
    x="Choc (pb)",
    y="Prix",
    markers=True
)

st.plotly_chart(
    fig_sens,
    use_container_width=True
)

# =====================================================
# DONNEES COURBE
# =====================================================

with st.expander(
    "Afficher la courbe de taux"
):

    st.dataframe(
        curve_df,
        use_container_width=True
    )

# =====================================================
# EXPORT CSV
# =====================================================

csv_export = sens_df.to_csv(
    index=False
)

st.download_button(
    label="Télécharger l'analyse",
    data=csv_export,
    file_name="analyse_sensibilite.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Pricer Obligataire Maroc | Version Professionnelle"
)
