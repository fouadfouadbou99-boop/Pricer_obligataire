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
    page_title="Portefeuille Obligataire Maroc",
    layout="wide"
)

st.title("📊 Portefeuille Obligataire Maroc")

# =========================
# Chargement portefeuille
# =========================

try:

    portefeuille = pd.read_excel(
        "RPC_bonds_data_rpc.xlsx",
        engine="openpyxl"
    )

except Exception as e:

    st.error(
        f"Erreur portefeuille : {e}"
    )

    st.stop()

# =========================
# Chargement courbe
# =========================

try:

    curve = ZeroCurve(
        "courbe_taux.csv"
    )

    curve_df = pd.read_csv(
        "courbe_taux.csv"
    )

except Exception as e:

    st.error(
        f"Erreur courbe : {e}"
    )

    st.stop()

# =========================
# KPI Portefeuille
# =========================

portfolio_nominal = portefeuille[
    "Nominal Global"
].sum()

nombre_lignes = len(
    portefeuille
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Nominal Total (MAD)",
        f"{portfolio_nominal:,.0f}"
    )

with col2:

    st.metric(
        "Nombre de lignes",
        nombre_lignes
    )

# =========================
# Courbe des taux
# =========================

st.subheader(
    "Courbe des taux zéro"
)

fig_curve = px.line(
    curve_df,
    x="tenor",
    y="rate",
    markers=True
)

fig_curve.update_layout(
    xaxis_title="Maturité",
    yaxis_title="Taux"
)

st.plotly_chart(
    fig_curve,
    use_container_width=True
)

# =========================
# Analyse obligation
# =========================

st.subheader(
    "Analyse d'une obligation"
)

nominal = st.number_input(
    "Nominal",
    value=1000000
)

coupon_pct = st.number_input(
    "Coupon (%)",
    value=3.50
)

maturity = st.number_input(
    "Maturité (années)",
    value=10
)

frequency = st.selectbox(
    "Fréquence",
    [1, 2, 4]
)

coupon = coupon_pct / 100

bond = Bond(
    nominal,
    coupon,
    maturity,
    frequency
)

duration_mac = macaulay_duration(
    bond,
    curve
)

ytm = curve.get_rate(
    maturity
)

duration_mod = modified_duration(
    duration_mac,
    ytm
)

prix_theorique = nominal

dv01_value = dv01(
    prix_theorique,
    duration_mod
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Duration Macaulay",
        round(duration_mac, 4)
    )

with col2:

    st.metric(
        "Duration Modifiée",
        round(duration_mod, 4)
    )

with col3:

    st.metric(
        "DV01",
        round(dv01_value, 2)
    )

# =========================
# Tableau positions
# =========================

st.subheader(
    "Positions du portefeuille"
)

colonnes_affichees = [
    "Code",
    "Description Titres",
    "Date Echéance",
    "Taux facial",
    "Quantité",
    "Nominal Global"
]

colonnes_existantes = [
    c for c in colonnes_affichees
    if c in portefeuille.columns
]

st.dataframe(
    portefeuille[
        colonnes_existantes
    ],
    use_container_width=True
)

# =========================
# Répartition portefeuille
# =========================

if "Nominal Global" in portefeuille.columns:

    top_positions = portefeuille.nlargest(
        10,
        "Nominal Global"
    )

    if (
        "Description Titres"
        in top_positions.columns
    ):

        st.subheader(
            "Top 10 Positions"
        )

        fig_top = px.bar(
            top_positions,
            x="Description Titres",
            y="Nominal Global"
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )

# =========================
# Synthèse
# =========================

st.subheader(
    "Synthèse"
)

resume = pd.DataFrame({

    "Indicateur": [

        "Nominal Total",
        "Nombre Positions",
        "Duration Macaulay",
        "Duration Modifiée",
        "DV01"

    ],

    "Valeur": [

        portfolio_nominal,
        nombre_lignes,
        duration_mac,
        duration_mod,
        dv01_value

    ]
})

st.dataframe(
    resume,
    use_container_width=True
)

# =========================
# Export Excel
# =========================

@st.cache_data
def to_excel(df):

    from io import BytesIO

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False
        )

    return output.getvalue()

excel_data = to_excel(
    portefeuille
)

st.download_button(
    label="📥 Télécharger Portefeuille",
    data=excel_data,
    file_name="portefeuille_analyse.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
