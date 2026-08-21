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

# --------------------------------------------------
# Configuration de la page
# --------------------------------------------------

st.set_page_config(
    page_title="Pricer Obligataire Maroc",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Pricer Obligataire Maroc")
st.markdown(
    "Valorisation, mesure du risque et analyse de sensibilité des obligations."
)

# --------------------------------------------------
# Chargement de la courbe de taux
# --------------------------------------------------

CSV_FILE = "courbe_taux.csv"


@st.cache_data
def load_curve_data():

    try:

        df = pd.read_csv(CSV_FILE)

        required_cols = ["tenor", "rate"]

        for col in required_cols:

            if col not in df.columns:
                st.error(
                    f"Colonne manquante : {col}"
                )
                return pd.DataFrame()

        return df

    except FileNotFoundError:

        st.error(
            f"Le fichier '{CSV_FILE}' est introuvable."
        )

        return pd.DataFrame()

    except Exception as e:

        st.error(
            f"Erreur de lecture : {e}"
        )

        return pd.DataFrame()


curve_df = load_curve_data()

if curve_df.empty:

    st.stop()

# --------------------------------------------------
# Construction de la courbe zéro
# --------------------------------------------------

curve = ZeroCurve(
    curve_df["tenor"],
    curve_df["rate"]
)

# --------------------------------------------------
# Paramètres utilisateur
# --------------------------------------------------

st.sidebar.header("Paramètres de l'obligation")

nominal = st.sidebar.number_input(
    "Nominal (MAD)",
    value=1000000,
    min_value=1000,
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
    "Fréquence des coupons",
    [1, 2],
    index=1
)

market_price = st.sidebar.number_input(
    "Prix de marché (optionnel)",
    value=1000000.0,
    step=100.0
)

# --------------------------------------------------
# Création de l'obligation
# --------------------------------------------------

bond = Bond(
    nominal,
    coupon_rate,
    maturity,
    frequency
)

# --------------------------------------------------
# Calculs
# --------------------------------------------------

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

    ytm = bond.ytm(market_price)

except:

    ytm = None

# --------------------------------------------------
# Tableau de bord
# --------------------------------------------------

st.subheader("📊 Tableau de bord")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Prix théorique",
        f"{price:,.2f} MAD"
    )

with col2:

    if ytm is not None:

        st.metric(
            "YTM",
            f"{ytm*100:.2f}%"
        )

with col3:

    st.metric(
        "Écart Prix / Marché",
        f"{price - market_price:,.2f}"
    )

col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "Duration Macaulay",
        f"{duration:.2f}"
    )

with col5:

    st.metric(
        "Duration Modifiée",
        f"{mod_duration:.2f}"
    )

with col6:

    st.metric(
        "DV01",
        f"{dv01_value:,.2f}"
    )

st.metric(
    "Convexité",
    f"{conv:.2f}"
)

# --------------------------------------------------
# Courbe des taux
# --------------------------------------------------

st.subheader("📉 Courbe Zéro Coupon")

fig_curve = px.line(
    curve_df,
    x="tenor",
    y="rate",
    markers=True,
    title="Courbe des taux zéro"
)

fig_curve.update_layout(
    xaxis_title="Maturité (années)",
    yaxis_title="Taux"
)

st.plotly_chart(
    fig_curve,
    use_container_width=True
)

# --------------------------------------------------
# Analyse de sensibilité
# --------------------------------------------------

st.subheader("📈 Sensibilité aux variations de taux")

shocks = [
    -0.01,
    -0.005,
    0,
    0.005,
    0.01
]

results = []

for shock in shocks:

    shifted_curve = ZeroCurve(
        curve_df["tenor"],
        curve_df["rate"] + shock
    )

    shocked_price = bond.price(
        shifted_curve
    )

    results.append(
        {
            "Choc (pb)": shock * 10000,
            "Prix": shocked_price
        }
    )

sens_df = pd.DataFrame(results)

st.dataframe(
    sens_df,
    use_container_width=True
)

fig_sens = px.line(
    sens_df,
    x="Choc (pb)",
    y="Prix",
    markers=True,
    title="Impact d'un choc de taux sur le prix"
)

st.plotly_chart(
    fig_sens,
    use_container_width=True
)

# --------------------------------------------------
# Données de la courbe
# --------------------------------------------------

with st.expander("Afficher les données de la courbe"):

    st.dataframe(
        curve_df,
        use_container_width=True
    )

# --------------------------------------------------
# Export CSV
# --------------------------------------------------

csv_export = sens_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Télécharger l'analyse de sensibilité",
    data=csv_export,
    file_name="sensibilite_obligataire.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Pied de page
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Pricer Obligataire Maroc - Version Professionnelle"
)
